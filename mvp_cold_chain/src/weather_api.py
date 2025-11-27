"""
Weather API Module
Handles fetching weather forecasts from OpenWeatherMap API
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherAPI:
    """
    Wrapper for OpenWeatherMap API

    Free tier limitations:
    - 1,000 calls/day
    - 7-day forecast available
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Weather API client

        Args:
            api_key: OpenWeatherMap API key (or set OPENWEATHER_API_KEY in .env)
        """
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY')

        if not self.api_key:
            raise ValueError(
                "OpenWeatherMap API key not found. "
                "Set OPENWEATHER_API_KEY in .env file or pass as argument."
            )

        self.base_url = "https://api.openweathermap.org/data/2.5"

    def get_7day_forecast(self, lat: float, lon: float) -> Dict:
        """
        Fetch 7-day weather forecast for a location

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Dictionary with forecast data
        """
        # Use One Call API 3.0 for 7-day forecast
        url = f"{self.base_url}/onecall"

        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric',  # Celsius
            'exclude': 'minutely,hourly,alerts'  # Only need daily forecast
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather for ({lat}, {lon}): {e}")
            return None

    def parse_forecast(self, forecast_data: Dict) -> pd.DataFrame:
        """
        Parse forecast JSON into DataFrame

        Args:
            forecast_data: Raw forecast JSON from API

        Returns:
            DataFrame with daily forecast
        """
        if not forecast_data or 'daily' not in forecast_data:
            return pd.DataFrame()

        daily_data = []

        for day in forecast_data['daily'][:7]:  # 7-day forecast
            daily_data.append({
                'date': datetime.fromtimestamp(day['dt']).date(),
                'temp_min': day['temp']['min'],
                'temp_max': day['temp']['max'],
                'temp_day': day['temp']['day'],
                'temp_night': day['temp']['night'],
                'feels_like_day': day['feels_like']['day'],
                'pressure': day['pressure'],
                'humidity': day['humidity'],
                'dew_point': day['dew_point'],
                'wind_speed': day['wind_speed'],
                'clouds': day['clouds'],  # Cloud cover %
                'uvi': day['uvi'],  # UV index
                'weather_main': day['weather'][0]['main'],
                'weather_description': day['weather'][0]['description']
            })

        return pd.DataFrame(daily_data)

    def get_forecast_features(self, lat: float, lon: float) -> Dict:
        """
        Get aggregated forecast features for model input

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Dictionary with 7-day summary features
        """
        forecast_data = self.get_7day_forecast(lat, lon)

        if not forecast_data:
            return None

        df = self.parse_forecast(forecast_data)

        if df.empty:
            return None

        # Calculate aggregate features
        features = {
            'max_temp_7d': df['temp_max'].max(),
            'min_temp_7d': df['temp_min'].min(),
            'avg_temp_7d': df['temp_day'].mean(),
            'temp_above_35_days': (df['temp_max'] > 35).sum(),
            'temp_above_38_days': (df['temp_max'] > 38).sum(),
            'temp_below_20_days': (df['temp_min'] < 20).sum(),
            'avg_humidity_7d': df['humidity'].mean(),
            'max_humidity_7d': df['humidity'].max(),
            'avg_cloud_cover_7d': df['clouds'].mean(),
            'max_cloud_cover_7d': df['clouds'].max(),
            'cloudy_days': (df['clouds'] > 60).sum(),  # Days with >60% cloud cover
            'avg_wind_speed_7d': df['wind_speed'].mean(),
            'heat_wave_indicator': self._detect_heat_wave(df),
            'forecast_date': datetime.now().date()
        }

        return features

    def _detect_heat_wave(self, df: pd.DataFrame, threshold: float = 35.0, days: int = 3) -> bool:
        """
        Detect if there's a heat wave in the forecast

        Heat wave = 3+ consecutive days with temp > threshold

        Args:
            df: DataFrame with temperature data
            threshold: Temperature threshold (°C)
            days: Minimum consecutive days

        Returns:
            True if heat wave detected
        """
        high_temps = (df['temp_max'] > threshold).astype(int)

        # Find consecutive sequences
        consecutive = 0
        max_consecutive = 0

        for is_high in high_temps:
            if is_high:
                consecutive += 1
                max_consecutive = max(max_consecutive, consecutive)
            else:
                consecutive = 0

        return max_consecutive >= days

    def batch_forecast(self, locations: List[Dict]) -> pd.DataFrame:
        """
        Fetch forecasts for multiple locations

        Args:
            locations: List of dicts with 'facility_id', 'lat', 'lon'

        Returns:
            DataFrame with forecast features for all locations
        """
        results = []

        for i, loc in enumerate(locations):
            print(f"Fetching forecast {i+1}/{len(locations)}: {loc.get('facility_id', 'Unknown')}")

            features = self.get_forecast_features(loc['lat'], loc['lon'])

            if features:
                features['facility_id'] = loc.get('facility_id')
                features['lat'] = loc['lat']
                features['lon'] = loc['lon']
                results.append(features)

            # Rate limiting: avoid exceeding API limits
            # Free tier: 1000 calls/day ≈ 1 call every 90 seconds safe
            # For 100 facilities: ~3 hours to fetch all
            # Can batch weekly (only 100 calls/week)

        return pd.DataFrame(results)


# Example usage
if __name__ == "__main__":
    # Test API
    api = WeatherAPI()

    # Test with Nairobi coordinates
    nairobi_lat = -1.2921
    nairobi_lon = 36.8219

    print("Fetching 7-day forecast for Nairobi...")
    forecast = api.get_forecast_features(nairobi_lat, nairobi_lon)

    if forecast:
        print("\nForecast Features:")
        for key, value in forecast.items():
            print(f"  {key}: {value}")
    else:
        print("Failed to fetch forecast")
