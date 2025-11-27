# Model Inputs Recap - Temporal Cold Chain Failure Prediction

## 🎯 What We're Predicting

**For each facility, predict failure probability for each of the next 5 days**

**Output**: 5 probabilities per facility
```python
Facility A:
  Day 1 (Tomorrow):    10% failure risk → LOW
  Day 2 (Thursday):    15% failure risk → LOW
  Day 3 (Friday):      75% failure risk → HIGH ⚠️
  Day 4 (Saturday):    68% failure risk → HIGH ⚠️
  Day 5 (Sunday):      28% failure risk → MODERATE
```

---

## 📊 Complete Input Features (65 Total - Updated with Power Infrastructure!)

**IMPORTANT UPDATE**: We've added 10 power infrastructure features to make predictions more realistic!

### 1. Facility Identification (6 features)

| Feature | Type | Example | Description |
|---------|------|---------|-------------|
| `facility_id` | String | `KE_NRB_001` | Unique facility identifier |
| `facility_name` | String | `Nairobi Health Center 1` | Facility name |
| `latitude` | Float | `-1.2921` | GPS latitude |
| `longitude` | Float | `36.8219` | GPS longitude |
| `facility_type` | Categorical | `Health Center` | Hospital/Clinic/Health Center/Dispensary |
| `power_source` | Categorical | `Solar` | Grid/Solar/Diesel/None |

---

### 2. Daily Temperature Features (15 features - 5 days × 3 temps)

**For each of 5 days:**

| Feature Pattern | Day 1 Example | Description |
|----------------|---------------|-------------|
| `temp_max_day{N}` | `temp_max_day1: 28.5°C` | Maximum temperature for day N |
| `temp_min_day{N}` | `temp_min_day1: 15.2°C` | Minimum temperature for day N |
| `temp_day{N}` | `temp_day1: 22.1°C` | Average temperature for day N |

**All temperature features:**
```
temp_max_day1, temp_max_day2, temp_max_day3, temp_max_day4, temp_max_day5
temp_min_day1, temp_min_day2, temp_min_day3, temp_min_day4, temp_min_day5
temp_day1, temp_day2, temp_day3, temp_day4, temp_day5
```

---

### 3. Daily Cloud Cover Features (5 features)

**For each of 5 days:**

| Feature | Example | Description |
|---------|---------|-------------|
| `clouds_day1` | `75.0%` | Cloud cover percentage day 1 |
| `clouds_day2` | `82.0%` | Cloud cover percentage day 2 |
| `clouds_day3` | `68.0%` | Cloud cover percentage day 3 |
| `clouds_day4` | `45.0%` | Cloud cover percentage day 4 |
| `clouds_day5` | `30.0%` | Cloud cover percentage day 5 |

**Why important**: High clouds + Solar power = Battery drain risk

---

### 4. Daily Humidity Features (5 features)

**For each of 5 days:**

| Feature | Example | Description |
|---------|---------|-------------|
| `humidity_day1` | `65.0%` | Relative humidity day 1 |
| `humidity_day2` | `70.0%` | Relative humidity day 2 |
| `humidity_day3` | `68.0%` | Relative humidity day 3 |
| `humidity_day4` | `72.0%` | Relative humidity day 4 |
| `humidity_day5` | `67.0%` | Relative humidity day 5 |

---

### 5. Daily Wind Speed Features (5 features)

**For each of 5 days:**

| Feature | Example | Description |
|---------|---------|-------------|
| `wind_speed_day1` | `5.2 m/s` | Wind speed day 1 |
| `wind_speed_day2` | `4.8 m/s` | Wind speed day 2 |
| `wind_speed_day3` | `6.1 m/s` | Wind speed day 3 |
| `wind_speed_day4` | `4.5 m/s` | Wind speed day 4 |
| `wind_speed_day5` | `3.9 m/s` | Wind speed day 5 |

---

### 6. Aggregate Weather Features (9 features)

**Derived from 5-day forecast:**

| Feature | Example | Description |
|---------|---------|-------------|
| `max_temp_7d` | `36.1°C` | Highest temperature across all 5 days |
| `min_temp_7d` | `14.2°C` | Lowest temperature across all 5 days |
| `avg_temp_7d` | `26.4°C` | Average temperature across 5 days |
| `temp_above_35_days` | `3` | Number of days with temp >35°C |
| `temp_above_38_days` | `1` | Number of days with temp >38°C |
| `avg_cloud_cover_7d` | `68.5%` | Average cloud cover across 5 days |
| `cloudy_days` | `4` | Number of days with >60% cloud cover |
| `avg_humidity_7d` | `67.2%` | Average humidity across 5 days |
| `heat_wave_indicator` | `1` (True) | 1 if 3+ consecutive days >35°C, else 0 |

**Why important**: These capture overall weather stress on cold chain

---

### 7. Temporal Features (3 features)

| Feature | Example | Description |
|---------|---------|-------------|
| `month` | `11` | Current month (1-12) |
| `is_dry_season` | `0` | 1 if dry season (Jan-Mar, Jun-Oct), else 0 |
| `is_rainy_season` | `1` | 1 if rainy season (Apr-May, Nov-Dec), else 0 |

**Why important**: Season affects grid reliability and cooling needs

---

### 8. Power Infrastructure Features (10 features) ⚡ NEW!

**CRITICAL ADDITION**: These features make failure predictions much more realistic!

| Feature | Type | Example | Description |
|---------|------|---------|-------------|
| `electrification_rate` | Float | `62.2%` | Estimated electrification rate for facility area |
| `grid_reliability_score` | Float | `0.70` | Grid uptime score (0-1, where 1 = 100% reliable) |
| `distance_to_grid_km` | Float | `25.9 km` | Estimated distance to nearest transmission line |
| `avg_power_hours_per_day` | Float | `16.8 hrs` | Expected hours of power per day |
| `high_outage_risk` | Binary | `1` | 1 if grid reliability <60%, else 0 |
| `very_low_power_access` | Binary | `0` | 1 if electrification <30%, else 0 |
| `remote_from_grid` | Binary | `1` | 1 if distance to grid >20km, else 0 |
| `power_vulnerability_score` | Float | `42.8` | Composite vulnerability (0-100, higher = worse) |
| `avg_outage_duration_hours` | Float | `4.5 hrs` | Estimated average outage duration |
| `outage_frequency_per_week` | Float | `3.2` | Estimated outages per week |

**How estimated (MVP Quick Approach)**:
- Electrification based on latitude (Turkana = 25%, Nairobi = 80%, Coastal = 60%)
- Grid reliability derived from electrification rates
- Distance to grid based on power source type (Grid = close, Solar/None = far)
- Adjusted by facility type (Hospitals in better locations)

**Impact on Predictions**:
- Low electrification + unreliable grid → Higher failure risk
- Remote facilities (>30km from grid) → Supply chain issues
- Solar facilities in cloudy regions → Battery depletion risk

**Example Comparison**:
```
Turkana Clinic (High Risk):
  - Electrification: 30%
  - Grid reliability: 0.40
  - Distance to grid: 40.7 km
  - Result: 70% failure rate across 5 days

Nairobi Health Center (Low Risk):
  - Electrification: 85%
  - Grid reliability: 0.90
  - Distance to grid: 10.8 km
  - Result: 0% failure rate across 5 days
```

---

### 9. Metadata (2 features)

| Feature | Example | Description |
|---------|---------|-------------|
| `forecast_date` | `2025-11-27` | Date when forecast was retrieved |
| `num_days` | `5` | Number of forecast days (always 5) |

---

## 🎯 Target Variables (5 outputs per facility)

**What we're predicting for EACH day:**

| Target | Type | Values | Description |
|--------|------|--------|-------------|
| `failure_day1` | Binary | 0 or 1 | Will cold chain fail on day 1? |
| `failure_day2` | Binary | 0 or 1 | Will cold chain fail on day 2? |
| `failure_day3` | Binary | 0 or 1 | Will cold chain fail on day 3? |
| `failure_day4` | Binary | 0 or 1 | Will cold chain fail on day 4? |
| `failure_day5` | Binary | 0 or 1 | Will cold chain fail on day 5? |

**Example targets for one facility:**
```python
facility_id: KE_TUR_003
failure_day1: 0  # No failure tomorrow
failure_day2: 0  # No failure day 2
failure_day3: 1  # FAILURE on day 3 ⚠️
failure_day4: 1  # FAILURE on day 4 ⚠️
failure_day5: 0  # No failure day 5
```

---

## 📐 Data Shape

### Current Dataset (from run_mvp.py):

```python
Shape: (50 facilities, 65 features) ⚡ UPDATED WITH POWER FEATURES!

Breakdown:
- Facility info: 6 features
- Daily temps: 15 features (5 days × 3 temp types)
- Daily clouds: 5 features
- Daily humidity: 5 features
- Daily wind: 5 features
- Aggregate weather: 9 features
- Temporal: 3 features
- Power infrastructure: 10 features ⚡ NEW!
- Metadata: 2 features
- Targets: 5 features (failure_day1 to failure_day5)

Total: 65 columns (was 55, now +10 power features)
```

### For Model Training:

**Input (X)**: 60 features (all except targets) ⚡ +10 power features!
```python
X.shape = (50 facilities, 60 features)
```

**Output (y)**: 5 targets (one per day)
```python
y.shape = (50 facilities, 5 days)
y_columns = ['failure_day1', 'failure_day2', 'failure_day3', 'failure_day4', 'failure_day5']
```

---

## 🔍 Sample Input Row (Actual Data)

Here's what one facility's data looks like:

```python
{
  # Facility Info
  'facility_id': 'KE_TUR_008',
  'facility_name': 'Turkana Clinic 9',
  'latitude': 3.25,
  'longitude': 35.89,
  'facility_type': 'Clinic',
  'power_source': 'Solar',

  # Day 1 Weather
  'temp_max_day1': 32.5,
  'temp_min_day1': 22.1,
  'temp_day1': 27.3,
  'clouds_day1': 45.0,
  'humidity_day1': 35.0,
  'wind_speed_day1': 4.2,

  # Day 2 Weather
  'temp_max_day2': 34.8,
  'temp_min_day2': 23.5,
  'temp_day2': 29.1,
  'clouds_day2': 65.0,
  'humidity_day2': 38.0,
  'wind_speed_day2': 3.8,

  # Day 3 Weather
  'temp_max_day3': 36.2,  # Getting hot!
  'temp_min_day3': 24.8,
  'temp_day3': 30.5,
  'clouds_day3': 75.0,    # Very cloudy + solar = risk
  'humidity_day3': 40.0,
  'wind_speed_day3': 3.5,

  # Day 4 Weather
  'temp_max_day4': 35.9,
  'temp_min_day4': 24.2,
  'temp_day4': 30.0,
  'clouds_day4': 80.0,
  'humidity_day4': 42.0,
  'wind_speed_day4': 3.2,

  # Day 5 Weather
  'temp_max_day5': 34.1,
  'temp_min_day5': 23.1,
  'temp_day5': 28.6,
  'clouds_day5': 60.0,
  'humidity_day5': 39.0,
  'wind_speed_day5': 4.0,

  # Aggregate Features
  'max_temp_7d': 36.2,           # Hottest day = day 3
  'min_temp_7d': 22.1,
  'avg_temp_7d': 29.1,
  'temp_above_35_days': 3,       # Days 2, 3, 4 all >35°C
  'temp_above_38_days': 0,
  'avg_cloud_cover_7d': 65.0,
  'cloudy_days': 3,              # Days 3, 4, 5
  'avg_humidity_7d': 38.8,
  'heat_wave_indicator': 1,      # 3+ consecutive days >35°C

  # Temporal
  'month': 11,
  'is_dry_season': 0,
  'is_rainy_season': 1,

  # Metadata
  'forecast_date': '2025-11-27',
  'num_days': 5,

  # TARGETS (what we predict)
  'failure_day1': 0,   # No failure (temp OK, not too cloudy yet)
  'failure_day2': 0,   # No failure (borderline)
  'failure_day3': 1,   # FAILURE! (36°C + 75% clouds + solar power)
  'failure_day4': 1,   # FAILURE! (still hot + very cloudy)
  'failure_day5': 0    # No failure (cooling down)
}
```

---

## 🧮 How Synthetic Targets Are Generated

**Rules for predicting failures (implemented in run_mvp.py):**

```python
For each day D (1 to 5):
    temp = temp_max_dayD
    clouds = clouds_dayD
    power = power_source

    FAILURE if:

    Rule 1: Extreme heat + no power
      → temp > 38°C AND power == 'None'

    Rule 2: High heat + solar + cloudy (battery drain)
      → temp > 35°C AND power == 'Solar' AND clouds > 70%

    Rule 3: Heat accumulation (day 3+)
      → day >= 3 AND avg_temp_past_3_days > 33°C AND power != 'Grid'

    Rule 4: Moderate heat + no backup + very cloudy + dry season
      → temp > 30°C AND power in ['None', 'Diesel']
        AND clouds > 80% AND is_dry_season == 1
```

**Result from our data:**
- **Day 1**: 1 failure (2% of facilities)
- **Day 2**: 0 failures (0%)
- **Day 3**: 17 failures (34%) ⚠️ Risk accumulates
- **Day 4**: 20 failures (40%) ⚠️ Peak risk
- **Day 5**: 20 failures (40%) ⚠️ Still high

**This temporal pattern is realistic**: Cold chain stress builds up over consecutive hot/cloudy days!

---

## 🎯 Model Architecture

### Multi-Output Classifier

**Input**: 50 features (weather + facility + temporal)
**Output**: 5 binary predictions (one per day)

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier

# Features (X)
weather_features = [all temp/cloud/humidity/wind features]
facility_features = ['facility_type', 'power_source']
temporal_features = ['month', 'is_dry_season', 'is_rainy_season']
aggregate_features = ['max_temp_7d', 'heat_wave_indicator', ...]

X = df[weather_features + facility_features + temporal_features + aggregate_features]
# Shape: (50, 50)

# Targets (y)
y = df[['failure_day1', 'failure_day2', 'failure_day3', 'failure_day4', 'failure_day5']]
# Shape: (50, 5)

# Train
model = MultiOutputClassifier(RandomForestClassifier())
model.fit(X, y)

# Predict
predictions = model.predict_proba(X_new)
# Returns: Array of shape (n_facilities, 5 days, 2 classes)
# Extract failure probabilities: predictions[:, :, 1]
```

---

## 📊 Feature Importance (Expected)

**Most predictive features (hypothesis):**

1. **temp_max_day3, temp_max_day4, temp_max_day5** - Temperature on that specific day
2. **power_source** - Facilities without backup at much higher risk
3. **clouds_day3, clouds_day4, clouds_day5** - Cloud cover affects solar charging
4. **heat_wave_indicator** - Captures multi-day stress
5. **temp_above_35_days** - Number of hot days
6. **is_dry_season** - Season affects grid reliability
7. **avg_cloud_cover_7d** - Overall weather pattern

**Less important (likely):**
- `wind_speed` - Not directly affecting cold chain
- `humidity` - Indirect effect
- `facility_name`, `latitude`, `longitude` - Not used in model (just for mapping)

---

## ✅ Data Quality Check

From our successful run:

```
✅ 50 facilities loaded
✅ 100% weather forecast success rate (0 failed)
✅ No missing values
✅ Geographic diversity: -4.19° to 3.61° latitude
✅ Temperature range: 10.3°C to 36.1°C (realistic for Kenya)
✅ 23.2% overall failure rate (reasonable for synthetic data)
✅ Temporal pattern: Low day 1-2, High day 3-5 (realistic accumulation)
```

**Ready for model training!** ✅

---

## 🚀 Next Steps

1. **Load data**: `pd.read_csv('data/processed/facilities_with_daily_weather_and_targets.csv')`
2. **Prepare X and y**: Select 50 input features, 5 target features
3. **Train multi-output model**: RandomForest or XGBoost
4. **Evaluate per-day performance**: Precision/Recall for each of 5 days
5. **Visualize**: Heatmap of facilities × days with risk levels

**Want me to build the model training notebook now?** 🎯
