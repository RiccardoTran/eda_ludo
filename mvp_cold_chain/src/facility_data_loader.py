"""
Kenya Health Facility Data Loader
Fetches facility data from various sources
"""

import pandas as pd
import requests
from typing import Dict, List, Optional
import json

class KenyaFacilityLoader:
    """
    Load health facility data for Kenya

    Data Sources:
    1. Healthsites.io API (primary - always available)
    2. Kenya Master Health Facility List (KMHFL) - if available
    """

    def __init__(self):
        self.healthsites_api = "https://healthsites.io/api/v2/facilities"

    def fetch_from_healthsites(self, country: str = "Kenya", limit: int = 1000) -> pd.DataFrame:
        """
        Fetch facilities from Healthsites.io API

        Args:
            country: Country name
            limit: Maximum number of facilities to fetch

        Returns:
            DataFrame with facility data
        """
        print(f"Fetching facilities from Healthsites.io for {country}...")

        all_facilities = []
        page = 1
        page_size = 100

        while len(all_facilities) < limit:
            params = {
                'country': country,
                'page': page,
                'page_size': page_size
            }

            try:
                response = requests.get(self.healthsites_api, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()

                if 'features' not in data or not data['features']:
                    break

                for feature in data['features']:
                    props = feature['properties']
                    coords = feature['geometry']['coordinates']

                    facility = {
                        'facility_id': f"HS_{props.get('uuid', '')}",
                        'name': props.get('name', 'Unknown'),
                        'latitude': coords[1],
                        'longitude': coords[0],
                        'facility_type': self._map_facility_type(props.get('amenity', '')),
                        'source': 'healthsites.io',
                        'completeness': props.get('completeness', 0)
                    }

                    all_facilities.append(facility)

                print(f"  Page {page}: {len(data['features'])} facilities")

                if len(data['features']) < page_size:
                    break

                page += 1

            except requests.exceptions.RequestException as e:
                print(f"Error fetching page {page}: {e}")
                break

        print(f"\nTotal facilities fetched: {len(all_facilities)}")

        return pd.DataFrame(all_facilities)

    def _map_facility_type(self, amenity: str) -> str:
        """
        Map Healthsites amenity types to standard categories

        Args:
            amenity: Amenity type from Healthsites

        Returns:
            Standard facility type
        """
        amenity_lower = amenity.lower()

        if 'hospital' in amenity_lower:
            return 'Hospital'
        elif 'clinic' in amenity_lower or 'health' in amenity_lower:
            return 'Clinic'
        elif 'center' in amenity_lower or 'centre' in amenity_lower:
            return 'Health Center'
        elif 'dispensary' in amenity_lower:
            return 'Dispensary'
        elif 'pharmacy' in amenity_lower or 'chemist' in amenity_lower:
            return 'Pharmacy'
        else:
            return 'Other'

    def load_from_csv(self, filepath: str) -> pd.DataFrame:
        """
        Load facilities from CSV file (e.g., from KMHFL download)

        Args:
            filepath: Path to CSV file

        Returns:
            DataFrame with facility data
        """
        print(f"Loading facilities from {filepath}...")

        try:
            df = pd.read_csv(filepath)
            print(f"Loaded {len(df)} facilities from CSV")
            return df

        except Exception as e:
            print(f"Error loading CSV: {e}")
            return pd.DataFrame()

    def filter_by_county(self, df: pd.DataFrame, counties: List[str]) -> pd.DataFrame:
        """
        Filter facilities by county

        Args:
            df: DataFrame with facilities
            counties: List of county names

        Returns:
            Filtered DataFrame
        """
        if 'county' not in df.columns:
            print("Warning: 'county' column not found in data")
            return df

        filtered = df[df['county'].isin(counties)].copy()
        print(f"Filtered to {len(filtered)} facilities in {counties}")

        return filtered

    def add_power_source_estimates(self, df: pd.DataFrame, electrification_data: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Estimate power source based on location and facility type

        Uses heuristics if no electrification data available:
        - Urban areas + hospitals → likely grid power
        - Rural areas + small clinics → likely no power or solar
        - Mid-tier facilities → likely diesel or solar

        Args:
            df: DataFrame with facilities
            electrification_data: Optional DataFrame with electrification rates by region

        Returns:
            DataFrame with power_source column added
        """
        df = df.copy()

        # Simple heuristic if no electrification data
        def estimate_power_source(row):
            facility_type = row.get('facility_type', 'Unknown')

            # Hospitals more likely to have power
            if facility_type == 'Hospital':
                return 'Grid'  # Assume grid power

            # Clinics/Dispensaries less likely
            elif facility_type in ['Clinic', 'Dispensary']:
                # Could refine with electrification_data
                return 'Solar'  # Conservative estimate

            # Health centers - mixed
            elif facility_type == 'Health Center':
                return 'Diesel'  # Backup generators common

            else:
                return 'None'

        df['power_source'] = df.apply(estimate_power_source, axis=1)

        print("Power source estimates added (heuristic-based)")

        return df

    def prepare_for_model(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare facility data for model training

        Ensures required columns are present:
        - facility_id
        - name
        - latitude, longitude
        - facility_type
        - power_source (estimated if needed)

        Args:
            df: Raw facility DataFrame

        Returns:
            Cleaned DataFrame ready for modeling
        """
        required_cols = ['facility_id', 'name', 'latitude', 'longitude', 'facility_type']

        # Check required columns
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            print(f"Warning: Missing required columns: {missing}")

        # Clean data
        df_clean = df.copy()

        # Remove facilities without GPS coordinates
        df_clean = df_clean.dropna(subset=['latitude', 'longitude'])

        # Remove duplicates
        df_clean = df_clean.drop_duplicates(subset=['latitude', 'longitude'])

        # Add power source if not present
        if 'power_source' not in df_clean.columns:
            df_clean = self.add_power_source_estimates(df_clean)

        print(f"\nCleaned data: {len(df_clean)} facilities ready for modeling")

        return df_clean


# Example usage
if __name__ == "__main__":
    loader = KenyaFacilityLoader()

    # Fetch from Healthsites.io
    facilities = loader.fetch_from_healthsites(country="Kenya", limit=200)

    if not facilities.empty:
        print("\nSample facilities:")
        print(facilities.head())

        print("\nFacility types:")
        print(facilities['facility_type'].value_counts())

        # Prepare for modeling
        facilities_clean = loader.prepare_for_model(facilities)

        # Save to CSV
        output_path = "../data/raw/kenya_facilities_healthsites.csv"
        facilities_clean.to_csv(output_path, index=False)
        print(f"\n✓ Saved to {output_path}")
