"""
Automated MVP Data Collection & Model Training
Runs the complete pipeline from data collection to model training
"""

import sys
sys.path.append('src')

import pandas as pd
import numpy as np
from datetime import datetime
import time
from tqdm import tqdm
import os

from weather_api_v2 import WeatherAPI
from facility_data_loader import KenyaFacilityLoader

print("="*70)
print(" MVP PLAN 2: TEMPORAL COLD CHAIN FAILURE PREDICTION")
print("="*70)
print(f"\nStarting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================================
# STEP 1: LOAD KENYA FACILITIES
# ============================================================================
print("\n" + "="*70)
print("STEP 1: Loading Kenya Health Facilities")
print("="*70)

# Use sample data for MVP (replace with Healthsites.io API when available)
facilities = pd.read_csv('data/raw/kenya_facilities_sample.csv')

print(f"\n✓ Loaded {len(facilities)} facilities")
print(f"\nFacility types:")
print(facilities['facility_type'].value_counts())
print(f"\nPower sources:")
print(facilities['power_source'].value_counts())

# ============================================================================
# STEP 2: FETCH WEATHER FORECASTS
# ============================================================================
print("\n" + "="*70)
print("STEP 2: Fetching 5-Day Weather Forecasts")
print("="*70)
print(f"Fetching forecasts for {len(facilities)} facilities...")
print("Estimated time: 1-2 minutes\n")

weather_api = WeatherAPI()
weather_data = []
failed_facilities = []

for idx, facility in tqdm(facilities.iterrows(), total=len(facilities), desc="Fetching forecasts"):
    try:
        features = weather_api.get_forecast_features(
            lat=facility['latitude'],
            lon=facility['longitude'],
            days=5
        )

        if features:
            features['facility_id'] = facility['facility_id']
            features['facility_name'] = facility['name']
            features['latitude'] = facility['latitude']
            features['longitude'] = facility['longitude']
            features['facility_type'] = facility['facility_type']
            features['power_source'] = facility['power_source']
            weather_data.append(features)
        else:
            failed_facilities.append(facility['facility_id'])

        time.sleep(0.3)  # Rate limiting

    except Exception as e:
        print(f"\nError for {facility['name']}: {e}")
        failed_facilities.append(facility['facility_id'])

print(f"\n✓ Successfully fetched weather for {len(weather_data)} facilities")
print(f"✗ Failed: {len(failed_facilities)} facilities\n")

# ============================================================================
# STEP 3: CREATE DATASET
# ============================================================================
print("\n" + "="*70)
print("STEP 3: Creating Model Dataset")
print("="*70)

df = pd.DataFrame(weather_data)

# Add temporal features
current_month = datetime.now().month
df['month'] = current_month
df['is_dry_season'] = int(current_month in [1, 2, 3, 6, 7, 8, 9, 10])
df['is_rainy_season'] = int(current_month in [4, 5, 11, 12])

print(f"\nDataset shape: {df.shape}")
print(f"Features: {len(df.columns)}")
print(f"\nFacility types:")
print(df['facility_type'].value_counts())
print(f"\nPower sources:")
print(df['power_source'].value_counts())

# ============================================================================
# STEP 3.5: ADD POWER INFRASTRUCTURE FEATURES
# ============================================================================
print("\n" + "="*70)
print("STEP 3.5: Adding Power Infrastructure Features")
print("="*70)
print("Estimating power features based on geography and facility type...\n")

def estimate_power_features(row):
    """
    Estimate power infrastructure features based on geography
    Uses latitude as proxy for infrastructure level (rough but realistic for Kenya)
    """
    lat = row['latitude']
    power = row['power_source']
    facility_type = row['facility_type']

    # Estimate electrification based on latitude (rough proxy for Kenya)
    # Northern Kenya (Turkana) = very low, Nairobi area = high, Coastal = moderate
    if lat > 2:  # Far north (Turkana region)
        electrification_est = 25
        grid_reliability_est = 0.35
    elif lat > 0:  # Mid-north
        electrification_est = 40
        grid_reliability_est = 0.55
    elif lat > -2:  # Central (Nairobi)
        electrification_est = 80
        grid_reliability_est = 0.85
    else:  # Coastal/south (Mombasa, Garissa)
        electrification_est = 60
        grid_reliability_est = 0.70

    # Adjust for facility type (hospitals/health centers in better locations)
    if facility_type == 'Hospital':
        electrification_est += 15
        grid_reliability_est += 0.10
    elif facility_type == 'Health Center':
        electrification_est += 5
        grid_reliability_est += 0.05

    # Estimate distance to grid based on power source
    if power == 'Grid':
        distance_est = np.random.uniform(1, 15)  # Close to grid
    elif power == 'Solar':
        distance_est = np.random.uniform(15, 50)  # Farther from grid
    elif power == 'Diesel':
        distance_est = np.random.uniform(25, 60)  # Remote
    else:  # None
        distance_est = np.random.uniform(40, 80)  # Very remote

    # Calculate derived features
    electrification_final = min(electrification_est, 95)
    grid_reliability_final = min(grid_reliability_est, 0.95)
    avg_power_hours = grid_reliability_final * 24

    # Binary risk indicators
    high_outage_risk = 1 if grid_reliability_final < 0.6 else 0
    very_low_power = 1 if electrification_final < 30 else 0
    remote_from_grid = 1 if distance_est > 20 else 0

    # Composite vulnerability score (0-100, higher = more vulnerable)
    vulnerability = (
        (100 - electrification_final) * 0.4 +
        distance_est * 0.3 +
        (100 - grid_reliability_final * 100) * 0.3
    )

    return {
        'electrification_rate': electrification_final,
        'grid_reliability_score': grid_reliability_final,
        'distance_to_grid_km': round(distance_est, 1),
        'avg_power_hours_per_day': round(avg_power_hours, 1),
        'high_outage_risk': high_outage_risk,
        'very_low_power_access': very_low_power,
        'remote_from_grid': remote_from_grid,
        'power_vulnerability_score': round(vulnerability, 1),
        'avg_outage_duration_hours': round(4.5 if high_outage_risk else 1.5, 1),
        'outage_frequency_per_week': round(3.2 if high_outage_risk else 0.8, 1)
    }

# Apply power feature estimation to all facilities
power_estimates = df.apply(estimate_power_features, axis=1, result_type='expand')
df = pd.concat([df, power_estimates], axis=1)

print(f"✓ Added 10 power infrastructure features")
print(f"\nPower Infrastructure Summary:")
print(f"  • Avg electrification rate: {df['electrification_rate'].mean():.1f}%")
print(f"  • Avg grid reliability: {df['grid_reliability_score'].mean():.2f}")
print(f"  • Avg distance to grid: {df['distance_to_grid_km'].mean():.1f} km")
print(f"  • High outage risk facilities: {df['high_outage_risk'].sum()} ({df['high_outage_risk'].sum()/len(df)*100:.1f}%)")
print(f"  • Very low power access: {df['very_low_power_access'].sum()} ({df['very_low_power_access'].sum()/len(df)*100:.1f}%)")
print(f"  • Remote from grid (>20km): {df['remote_from_grid'].sum()} ({df['remote_from_grid'].sum()/len(df)*100:.1f}%)")

# ============================================================================
# STEP 4: CREATE TARGET VARIABLES (Synthetic for MVP)
# ============================================================================
print("\n" + "="*70)
print("STEP 4: Creating Synthetic Target Variables")
print("="*70)
print("Generating failure labels for each of 5 days...\n")

def predict_failure_per_day(row):
    """
    Enhanced failure prediction including power infrastructure
    Incorporates grid reliability, electrification, and distance to grid
    """
    failures = []

    # Extract power infrastructure features
    grid_reliability = row['grid_reliability_score']
    electrification = row['electrification_rate']
    distance_to_grid = row['distance_to_grid_km']
    power = row['power_source']

    for day in range(1, 6):  # 5 days
        temp = row[f'temp_max_day{day}']
        clouds = row[f'clouds_day{day}']

        failure = False

        # ========== GRID POWER FACILITIES ==========
        if power == 'Grid':
            # Rule 1: Unreliable grid + heat
            if grid_reliability < 0.6 and temp > 33:
                failure = True  # Frequent outages during hot weather

            # Rule 2: Low electrification area (proxy for poor grid)
            if electrification < 40 and temp > 30:
                failure = True  # Poor grid infrastructure can't handle load

            # Rule 3: Heat wave strains grid
            if row.get('heat_wave_indicator', 0) == 1 and grid_reliability < 0.75:
                failure = True  # Grid fails under high AC demand

        # ========== SOLAR POWER FACILITIES ==========
        elif power == 'Solar':
            # Rule 4: Cloudy + no grid backup
            if clouds > 70 and temp > 32:
                failure = True  # Battery drains, no backup

            # Rule 5: Multi-day cloudy period
            if day >= 3:
                past_clouds = [row[f'clouds_day{d}'] for d in range(max(1, day-2), day+1)]
                avg_clouds_3day = np.mean(past_clouds)
                if avg_clouds_3day > 65:
                    failure = True  # Battery fully depleted

            # Rule 6: Heat + clouds combination
            if temp > 35 and clouds > 60:
                failure = True  # High cooling load + low charging

        # ========== DIESEL BACKUP ==========
        elif power == 'Diesel':
            # Rule 7: Remote location (fuel supply issues)
            if distance_to_grid > 50 and day >= 4:
                failure = True  # Fuel runs out by day 4-5

            # Rule 8: Extreme heat (generator overload)
            if temp > 38:
                failure = True  # Generator can't keep up with cooling load

        # ========== NO POWER ==========
        elif power == 'None':
            # Rule 9: Any significant heat = failure
            if temp > 32:
                failure = True  # No refrigeration at all

        # ========== UNIVERSAL RULES (All power types) ==========

        # Rule 10: Extreme heat overwhelms any system
        if temp > 40:
            failure = True

        # Rule 11: Low electrification area + unreliable power
        if electrification < 30 and power in ['Grid', 'Diesel']:
            if temp > 30:
                failure = True  # Infrastructure too poor to support cold chain

        # Rule 12: Very remote facilities (>30km from grid)
        if distance_to_grid > 30 and power != 'Solar':
            if temp > 32 and day >= 3:
                failure = True  # Isolation + time = failure

        # Rule 13: Heat accumulation (general)
        if day >= 3:
            past_temps = [row[f'temp_max_day{d}'] for d in range(max(1, day-2), day+1)]
            avg_temp = np.mean(past_temps)
            if avg_temp > 33 and grid_reliability < 0.7:
                failure = True  # Accumulated stress + unreliable power

        failures.append(1 if failure else 0)

    return failures

# Generate targets
for day in range(1, 6):
    df[f'failure_day{day}'] = 0

for idx, row in df.iterrows():
    failures = predict_failure_per_day(row)
    for day, failure in enumerate(failures, 1):
        df.at[idx, f'failure_day{day}'] = failure

# Calculate failure statistics
failure_cols = [f'failure_day{day}' for day in range(1, 6)]
total_failures = df[failure_cols].sum().sum()
total_facility_days = len(df) * 5

print(f"Synthetic failures generated:")
print(f"  Total facility-days: {total_facility_days}")
print(f"  Predicted failures: {total_failures}")
print(f"  Failure rate: {total_failures/total_facility_days*100:.1f}%")
print(f"\nFailures by day:")
for day in range(1, 6):
    count = df[f'failure_day{day}'].sum()
    print(f"  Day {day}: {count} failures ({count/len(df)*100:.1f}% of facilities)")

# ============================================================================
# STEP 5: SAVE DATASETS
# ============================================================================
print("\n" + "="*70)
print("STEP 5: Saving Datasets")
print("="*70)

# Create directories if they don't exist
os.makedirs('data/processed', exist_ok=True)
os.makedirs('outputs/figures', exist_ok=True)

# Save complete dataset
output_path = 'data/processed/facilities_with_daily_weather_and_targets.csv'
df.to_csv(output_path, index=False)
print(f"\n✓ Saved complete dataset to: {output_path}")
print(f"  Shape: {df.shape}")

# Save facilities only
facilities_only = df[['facility_id', 'facility_name', 'latitude', 'longitude',
                      'facility_type', 'power_source']].copy()
facilities_only.to_csv('data/processed/kenya_facilities.csv', index=False)
print(f"\n✓ Saved facility list to: data/processed/kenya_facilities.csv")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("DATA COLLECTION COMPLETE! ✅")
print("="*70)

print(f"\n📊 Dataset Summary:")
print(f"  • Facilities: {len(df)}")
print(f"  • Features: {len(df.columns)}")
print(f"  • Days forecasted: 5")
print(f"  • Total facility-days: {len(df) * 5}")
print(f"  • Failure rate: {total_failures/total_facility_days*100:.1f}%")

print(f"\n🌍 Geographic Coverage:")
print(f"  • Latitude: {df['latitude'].min():.2f}° to {df['latitude'].max():.2f}°")
print(f"  • Longitude: {df['longitude'].min():.2f}° to {df['longitude'].max():.2f}°")

print(f"\n🌡️  Weather Summary (5-day forecast):")
print(f"  • Max temperature: {df['max_temp_7d'].max():.1f}°C")
print(f"  • Min temperature: {df['min_temp_7d'].min():.1f}°C")
print(f"  • Avg temperature: {df['avg_temp_7d'].mean():.1f}°C")
print(f"  • Facilities with heat wave: {df['heat_wave_indicator'].sum()}")

print(f"\n⚡ Power Infrastructure:")
for power, count in df['power_source'].value_counts().items():
    print(f"  • {power}: {count} facilities ({count/len(df)*100:.1f}%)")

print(f"\n📅 Temporal Context:")
print(f"  • Current month: {current_month}")
print(f"  • Season: {'Dry' if df['is_dry_season'].iloc[0] == 1 else 'Rainy'}")

print(f"\n✅ NEXT STEPS:")
print(f"  1. Run EDA: jupyter notebook notebooks/02_eda.ipynb")
print(f"  2. Train model: jupyter notebook notebooks/03_model_training.ipynb")
print(f"  3. Create demo: jupyter notebook notebooks/04_prediction_demo.ipynb")

print(f"\n⏱️  Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\n{'='*70}\n")

print("🚀 Ready to build the temporal prediction model!")
