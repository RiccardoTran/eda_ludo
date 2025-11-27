"""
Weather API Module - FREE TIER VERSION
Uses 5-day/3-hour forecast (free) instead of One Call API
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
    Wrapper for OpenWeatherMap API - FREE TIER

    Uses 5 Day / 3 Hour Forecast API (completely free, no payment needed)
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

        # Use free tier forecast endpoint
        self.base_url = "https://api.openweathermap.org/data/2.5/forecast"

    def get_5day_forecast(self, lat: float, lon: float) -> Dict:
        """
        Fetch 5-day / 3-hour weather forecast for a location (FREE TIER)

        Args:
            lat: Latitude
            lon: Longitude

        Returns:
            Dictionary with forecast data
        """
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric',  # Celsius
            'cnt': 40  # 5 days × 8 forecasts per day = 40 data points
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather for ({lat}, {lon}): {e}")
            return None

    def parse_forecast_to_daily(self, forecast_data: Dict) -> pd.DataFrame:
        """
        Parse 3-hour forecast into daily summaries

        Args:
            forecast_data: Raw forecast JSON from API

        Returns:
            DataFrame with daily forecast (up to 5 days)
        """
        if not forecast_data or 'list' not in forecast_data:
            return pd.DataFrame()

        # Group 3-hour forecasts by day
        daily_data = {}

        for item in forecast_data['list']:
            dt = datetime.fromtimestamp(item['dt'])
            date = dt.date()

            if date not in daily_data:
                daily_data[date] = {
                    'temps': [],
                    'clouds': [],
                    'humidity': [],
                    'wind_speed': [],
                    'weather_main': [],
                    'pressure': []
                }

            daily_data[date]['temps'].append(item['main']['temp'])
            daily_data[date]['clouds'].append(item['clouds']['all'])
            daily_data[date]['humidity'].append(item['main']['humidity'])
            daily_data[date]['wind_speed'].append(item['wind']['speed'])
            daily_data[date]['weather_main'].append(item['weather'][0]['main'])
            daily_data[date]['pressure'].append(item['main']['pressure'])

        # Convert to daily summaries
        daily_summaries = []
        for date, data in sorted(daily_data.items())[:5]:  # Max 5 days
            daily_summaries.append({
                'date': date,
                'temp_min': min(data['temps']),
                'temp_max': max(data['temps']),
                'temp_day': sum(data['temps']) / len(data['temps']),
                'clouds': sum(data['clouds']) / len(data['clouds']),
                'humidity': sum(data['humidity']) / len(data['humidity']),
                'wind_speed': sum(data['wind_speed']) / len(data['wind_speed']),
                'pressure': sum(data['pressure']) / len(data['pressure']),
                'weather_main': max(set(data['weather_main']), key=data['weather_main'].count)
            })

        return pd.DataFrame(daily_summaries)

    def get_forecast_features(self, lat: float, lon: float, days: int = 5) -> Dict:
        """
        Get aggregated forecast features for model input

        Args:
            lat: Latitude
            lon: Longitude
            days: Number of days to include (max 5)

        Returns:
            Dictionary with daily and aggregate features
        """
        forecast_data = self.get_5day_forecast(lat, lon)

        if not forecast_data:
            return None

        df = self.parse_forecast_to_daily(forecast_data)

        if df.empty:
            return None

        # Ensure we have exactly 'days' rows (pad with last day if needed)
        while len(df) < days:
            last_row = df.iloc[-1].copy()
            last_row['date'] = last_row['date'] + timedelta(days=1)
            df = pd.concat([df, pd.DataFrame([last_row])], ignore_index=True)

        df = df.head(days)

        # Calculate features
        features = {
            'forecast_date': datetime.now().date(),
            'num_days': len(df),

            # Aggregate features
            'max_temp_7d': df['temp_max'].max(),
            'min_temp_7d': df['temp_min'].min(),
            'avg_temp_7d': df['temp_day'].mean(),
            'temp_above_35_days': (df['temp_max'] > 35).sum(),
            'temp_above_38_days': (df['temp_max'] > 38).sum(),
            'avg_cloud_cover_7d': df['clouds'].mean(),
            'cloudy_days': (df['clouds'] > 60).sum(),
            'avg_humidity_7d': df['humidity'].mean(),
            'heat_wave_indicator': self._detect_heat_wave(df)
        }

        # Add daily features (for temporal model)
        for i, row in df.iterrows():
            day_num = i + 1
            features[f'temp_max_day{day_num}'] = row['temp_max']
            features[f'temp_min_day{day_num}'] = row['temp_min']
            features[f'temp_day{day_num}'] = row['temp_day']
            features[f'clouds_day{day_num}'] = row['clouds']
            features[f'humidity_day{day_num}'] = row['humidity']
            features[f'wind_speed_day{day_num}'] = row['wind_speed']

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

        consecutive = 0
        max_consecutive = 0

        for is_high in high_temps:
            if is_high:
                consecutive += 1
                max_consecutive = max(max_consecutive, consecutive)
            else:
                consecutive = 0

        return max_consecutive >= days


# Example usage
if __name__ == "__main__":
    # Test API
    api = WeatherAPI()

    # Test with Nairobi coordinates
    nairobi_lat = -1.2921
    nairobi_lon = 36.8219

    print("Fetching 5-day forecast for Nairobi (FREE TIER API)...")
    forecast = api.get_forecast_features(nairobi_lat, nairobi_lon)

    if forecast:
        print("\n✓ Weather API working!")
        print("\nForecast Features:")
        for key, value in forecast.items():
            if isinstance(value, (int, float)):
                print(f"  {key}: {value:.2f}")
            else:
                print(f"  {key}: {value}")
    else:
        print("\n✗ Failed to fetch forecast")
        print("Check your API key or internet connection")
