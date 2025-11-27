"""
Create sample Kenya facility data for MVP testing
"""

import pandas as pd
import numpy as np
import os

# Create sample facilities across Kenya
# Using real Kenya coordinates but fictional facility names

facilities = []

# Nairobi region (capital, more infrastructure)
for i in range(10):
    facilities.append({
        'facility_id': f'KE_NRB_{i:03d}',
        'name': f'Nairobi Health Center {i+1}',
        'latitude': -1.2921 + np.random.uniform(-0.3, 0.3),
        'longitude': 36.8219 + np.random.uniform(-0.3, 0.3),
        'facility_type': np.random.choice(['Hospital', 'Health Center', 'Clinic'], p=[0.2, 0.5, 0.3]),
        'power_source': np.random.choice(['Grid', 'Solar', 'Diesel'], p=[0.7, 0.2, 0.1])
    })

# Turkana region (northern, hot, less infrastructure)
for i in range(15):
    facilities.append({
        'facility_id': f'KE_TUR_{i:03d}',
        'name': f'Turkana Clinic {i+1}',
        'latitude': 3.1167 + np.random.uniform(-0.5, 0.5),
        'longitude': 35.5978 + np.random.uniform(-0.5, 0.5),
        'facility_type': np.random.choice(['Clinic', 'Dispensary', 'Health Center'], p=[0.5, 0.3, 0.2]),
        'power_source': np.random.choice(['Solar', 'None', 'Diesel'], p=[0.5, 0.3, 0.2])
    })

# Mombasa region (coastal)
for i in range(10):
    facilities.append({
        'facility_id': f'KE_MBA_{i:03d}',
        'name': f'Mombasa Health Facility {i+1}',
        'latitude': -4.0435 + np.random.uniform(-0.2, 0.2),
        'longitude': 39.6682 + np.random.uniform(-0.2, 0.2),
        'facility_type': np.random.choice(['Hospital', 'Health Center', 'Clinic'], p=[0.3, 0.4, 0.3]),
        'power_source': np.random.choice(['Grid', 'Solar', 'Diesel'], p=[0.6, 0.3, 0.1])
    })

# Kisumu region (western)
for i in range(10):
    facilities.append({
        'facility_id': f'KE_KIS_{i:03d}',
        'name': f'Kisumu Dispensary {i+1}',
        'latitude': -0.0917 + np.random.uniform(-0.3, 0.3),
        'longitude': 34.7680 + np.random.uniform(-0.3, 0.3),
        'facility_type': np.random.choice(['Clinic', 'Health Center', 'Dispensary'], p=[0.4, 0.4, 0.2]),
        'power_source': np.random.choice(['Grid', 'Solar', 'Diesel'], p=[0.5, 0.4, 0.1])
    })

# Garissa region (eastern, hot)
for i in range(5):
    facilities.append({
        'facility_id': f'KE_GAR_{i:03d}',
        'name': f'Garissa Clinic {i+1}',
        'latitude': -0.4569 + np.random.uniform(-0.2, 0.2),
        'longitude': 39.6582 + np.random.uniform(-0.2, 0.2),
        'facility_type': np.random.choice(['Clinic', 'Dispensary'], p=[0.6, 0.4]),
        'power_source': np.random.choice(['Solar', 'Diesel', 'None'], p=[0.5, 0.3, 0.2])
    })

# Create DataFrame
df = pd.DataFrame(facilities)

print(f"Created {len(df)} sample facilities")
print(f"\nFacility types:")
print(df['facility_type'].value_counts())
print(f"\nPower sources:")
print(df['power_source'].value_counts())
print(f"\nGeographic spread:")
print(f"  Latitude: {df['latitude'].min():.2f}° to {df['latitude'].max():.2f}°")
print(f"  Longitude: {df['longitude'].min():.2f}° to {df['longitude'].max():.2f}°")

# Save to CSV
os.makedirs('data/raw', exist_ok=True)
output_path = 'data/raw/kenya_facilities_sample.csv'
df.to_csv(output_path, index=False)
print(f"\n✓ Saved to: {output_path}")
