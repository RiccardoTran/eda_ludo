# MVP Plan 2: Temporal Cold Chain Failure Prediction

## 🎯 Upgrade: From "IF" to "WHEN & WHERE"

### MVP Plan 1 (Current):
**Question**: "Will this facility have HIGH or LOW risk in the next 7 days?"
**Output**: Binary classification (High Risk / Low Risk)
**Use case**: "Should I delay vaccine delivery this week?"

### MVP Plan 2 (This Document):
**Question**: "WHEN will failure occur and at WHICH facilities over the next 7 days?"
**Output**: Daily failure probability for each facility × 7 days
**Use case**: "Failure predicted Tuesday at Turkana Clinic → Deploy generator Monday"

---

## Problem Framing

### What We're Predicting

**For each facility, for each of the next 7 days:**
```
Facility A:
  Day 1 (Tomorrow):     10% failure probability → LOW RISK
  Day 2 (Tue):          15% failure probability → LOW RISK
  Day 3 (Wed):          72% failure probability → HIGH RISK ⚠️
  Day 4 (Thu):          65% failure probability → HIGH RISK ⚠️
  Day 5 (Fri):          28% failure probability → MODERATE RISK
  Day 6 (Sat):          12% failure probability → LOW RISK
  Day 7 (Sun):           8% failure probability → LOW RISK

Recommendation: Deploy generator on Tuesday evening (before Wed spike)
```

### Advantages Over Binary Classification

| Aspect | MVP 1 (Binary) | MVP 2 (Temporal) |
|--------|---------------|------------------|
| **Granularity** | Week-level | Day-level |
| **Lead time** | "This week" | "Tuesday at 2pm" |
| **Intervention** | Generic ("delay delivery") | Specific ("deploy generator Monday") |
| **Resource planning** | Weekly | Daily scheduling |
| **Multiple facilities** | Rank by risk | Prioritize by day |

**Example scenario MVP 2 solves better:**

```
Monday morning forecast:
- Facility A: High risk Wednesday-Thursday (heat wave)
- Facility B: High risk Friday-Saturday (power outage forecast)
- Facility C: Low risk all week

Action plan:
→ Send generator to Facility A on Tuesday (for Wed-Thu)
→ Move generator to Facility B on Thursday (for Fri-Sat)
→ One generator serves both facilities
```

---

## Model Architecture

### Approach 1: Multi-Output Classification (Recommended for MVP)

**Model**: Random Forest with 7 binary outputs

**Input features** (same as MVP 1):
- Weather forecast: Day 1 temp, Day 2 temp, ..., Day 7 temp
- Weather forecast: Day 1 clouds, Day 2 clouds, ..., Day 7 clouds
- Facility: power_source, facility_type, electrification_rate
- Temporal: month, is_dry_season

**Output**: 7 probabilities (one per day)
```python
{
  'failure_prob_day1': 0.10,
  'failure_prob_day2': 0.15,
  'failure_prob_day3': 0.72,  # High risk!
  'failure_prob_day4': 0.65,
  'failure_prob_day5': 0.28,
  'failure_prob_day6': 0.12,
  'failure_prob_day7': 0.08
}
```

**Implementation**:
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier

# Train 7 separate models (one per day)
models = []
for day in range(1, 8):
    model = RandomForestClassifier()
    model.fit(X_train, y_train[f'failure_day{day}'])
    models.append(model)

# Or use MultiOutputClassifier
multi_model = MultiOutputClassifier(RandomForestClassifier())
multi_model.fit(X_train, y_train_all_days)
```

### Approach 2: Time Series Forecasting (More Complex)

**Model**: LSTM or GRU (recurrent neural network)

**Input**: Sequence of weather forecasts (7 days)
**Output**: Sequence of failure probabilities (7 days)

**Pros**: Captures temporal dependencies (if Day 1 fails → Day 2 higher risk)
**Cons**: Requires more data, harder to interpret, longer training

**Recommendation for MVP**: Start with Approach 1, upgrade to Approach 2 if needed

### Approach 3: Regression (Time-to-Failure)

**Model**: Regression to predict "hours until failure"

**Output**: Single number: "Failure expected in 52 hours"

**Pros**: Very specific timing
**Cons**: Harder to validate without real-time monitoring data

---

## Data Requirements

### Target Variable Creation (Synthetic)

For MVP (without real incident data), create synthetic failures based on rules:

```python
def predict_failure_per_day(facility, weather_forecast):
    """
    Generate synthetic failure indicator for each day
    """
    failures = []

    for day in range(1, 8):
        temp = weather_forecast[f'temp_day{day}']
        clouds = weather_forecast[f'clouds_day{day}']
        power = facility['power_source']

        # Failure rules (increasingly strict by day to show temporal variation)
        failure = False

        # Rule 1: Extreme heat + no power
        if temp > 38 and power == 'None':
            failure = True

        # Rule 2: High heat + solar power + cloudy (battery drain)
        if temp > 35 and power == 'Solar' and clouds > 70:
            failure = True

        # Rule 3: Heat wave accumulation (gets worse over time)
        if day >= 3:  # By day 3, heat accumulates
            avg_temp_past_3_days = mean([weather_forecast[f'temp_day{d}'] for d in range(max(1, day-2), day+1)])
            if avg_temp_past_3_days > 35 and power != 'Grid':
                failure = True

        # Rule 4: Dry season + unreliable grid
        if facility['is_dry_season'] and power == 'Grid' and facility['electrification_rate'] < 40:
            if temp > 33:  # Lower threshold in dry season
                failure = True

        failures.append(1 if failure else 0)

    return failures
```

**Result**: Each facility gets 7 binary labels (failure on day 1, day 2, ..., day 7)

```
facility_id,failure_day1,failure_day2,failure_day3,failure_day4,failure_day5,failure_day6,failure_day7
TZ_001,0,0,1,1,0,0,0  # Failures on Wed-Thu
TZ_002,0,0,0,0,1,1,0  # Failures on Fri-Sat
TZ_003,0,0,0,0,0,0,0  # No failures
```

### Input Features (Per Day)

**Weather features** (7 values per feature):
```python
features = {
    # Temperature
    'temp_day1': 28.5, 'temp_day2': 29.0, ..., 'temp_day7': 26.0,

    # Cloud cover
    'clouds_day1': 30, 'clouds_day2': 45, ..., 'clouds_day7': 60,

    # Humidity
    'humidity_day1': 65, 'humidity_day2': 70, ..., 'humidity_day7': 75,

    # Solar radiation (derived from clouds + latitude)
    'solar_day1': 5.2, 'solar_day2': 4.8, ..., 'solar_day7': 4.0
}
```

**Facility features** (constant):
```python
{
    'power_source_grid': 0,
    'power_source_solar': 1,
    'power_source_diesel': 0,
    'power_source_none': 0,
    'facility_type_hospital': 0,
    'facility_type_clinic': 1,
    'electrification_rate': 45.0,
    'population_density': 120,
    'distance_to_grid': 23.5
}
```

**Temporal features**:
```python
{
    'month': 4,  # April
    'is_dry_season': 1,
    'is_rainy_season': 0
}
```

**Total features**: ~35-40 (7 days × 4 weather vars + 10 facility/temporal)

---

## Model Training

### Step 1: Data Preparation

```python
import pandas as pd
import numpy as np

# Load facilities + weather forecasts
df = pd.read_csv('facilities_with_weather.csv')

# Create 7 target variables
for day in range(1, 8):
    df[f'failure_day{day}'] = df.apply(
        lambda row: predict_failure_day(row, day),
        axis=1
    )

# Create feature matrix (X)
weather_features = []
for day in range(1, 8):
    weather_features += [f'temp_day{day}', f'clouds_day{day}', f'humidity_day{day}']

facility_features = ['power_source_grid', 'power_source_solar', 'electrification_rate', ...]

X = df[weather_features + facility_features]

# Create target matrix (y) - 7 columns
y = df[[f'failure_day{day}' for day in range(1, 8)]]

print(f"X shape: {X.shape}")  # (n_facilities, ~40 features)
print(f"y shape: {y.shape}")  # (n_facilities, 7 days)
```

### Step 2: Train Multi-Output Model

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train multi-output model
base_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    min_samples_split=5,
    random_state=42
)

model = MultiOutputClassifier(base_model)
model.fit(X_train, y_train)

print("✓ Model trained on 7-day outputs")
```

### Step 3: Predict Daily Probabilities

```python
# Predict failure probabilities for each day
y_pred_proba = model.predict_proba(X_test)

# y_pred_proba is a list of 7 arrays (one per day)
# Each array has shape (n_samples, 2) for [prob_no_failure, prob_failure]

# Extract failure probabilities
failure_probs = np.array([proba[:, 1] for proba in y_pred_proba]).T

# Result: (n_samples, 7) - failure probability for each facility × day
print(failure_probs[:5])  # First 5 facilities
```

**Example output**:
```
Facility 1: [0.12, 0.18, 0.75, 0.68, 0.32, 0.15, 0.09]  # High risk Day 3-4
Facility 2: [0.08, 0.10, 0.13, 0.15, 0.65, 0.72, 0.28]  # High risk Day 5-6
Facility 3: [0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11]  # Low risk all week
```

---

## Visualization: Daily Risk Heatmap

### Heatmap: Facilities × Days

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Create heatmap of failure probabilities
fig, ax = plt.subplots(figsize=(10, 12))

sns.heatmap(
    failure_probs,
    cmap='YlOrRd',
    vmin=0, vmax=1,
    cbar_kws={'label': 'Failure Probability'},
    xticklabels=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    yticklabels=[f'Facility {i}' for i in range(len(failure_probs))],
    ax=ax
)

ax.set_title('7-Day Cold Chain Failure Risk Forecast', fontsize=14, fontweight='bold')
ax.set_xlabel('Day', fontsize=12)
ax.set_ylabel('Facility', fontsize=12)

plt.tight_layout()
plt.savefig('outputs/figures/daily_risk_heatmap.png', dpi=300)
plt.show()
```

**Output**: Heatmap showing red cells = high risk days

### Interactive Map with Daily Timeline

```python
import folium
from folium.plugins import Timeline, TimestampedGeoJson

# Create base map
m = folium.Map(location=[-1.2921, 36.8219], zoom_start=6)

# Add facilities with daily risk
for idx, facility in facilities.iterrows():
    # Get failure probabilities for this facility
    probs = failure_probs[idx]

    # Determine worst day
    worst_day = np.argmax(probs) + 1
    max_prob = probs[worst_day - 1]

    # Color by max risk
    color = 'red' if max_prob > 0.6 else 'orange' if max_prob > 0.3 else 'green'

    # Create popup with daily breakdown
    popup_html = f"""
    <b>{facility['name']}</b><br>
    <b>Worst day:</b> Day {worst_day} ({max_prob*100:.0f}% risk)<br>
    <br>
    <b>Daily forecast:</b><br>
    Mon: {probs[0]*100:.0f}%<br>
    Tue: {probs[1]*100:.0f}%<br>
    Wed: {probs[2]*100:.0f}%<br>
    Thu: {probs[3]*100:.0f}%<br>
    Fri: {probs[4]*100:.0f}%<br>
    Sat: {probs[5]*100:.0f}%<br>
    Sun: {probs[6]*100:.0f}%<br>
    """

    folium.CircleMarker(
        location=[facility['latitude'], facility['longitude']],
        radius=8,
        popup=folium.Popup(popup_html, max_width=250),
        color=color,
        fill=True,
        fillOpacity=0.7
    ).add_to(m)

m.save('outputs/maps/daily_risk_map.html')
print("✓ Interactive map saved")
```

---

## Use Cases Enabled by Temporal Prediction

### Use Case 1: Generator Deployment Scheduling

**Problem**: Limited generators, multiple facilities at risk

**MVP 1 solution**:
- "Facilities A, B, C at HIGH risk this week"
- Deploy 3 generators for whole week

**MVP 2 solution**:
```
Facility A: High risk Wed-Thu (deploy Tue, retrieve Fri)
Facility B: High risk Fri-Sat (deploy Thu, retrieve Sun)
Facility C: High risk Mon-Tue (deploy Sun, retrieve Wed)

→ Only need 1 generator (move between facilities)
→ 67% cost savings
```

### Use Case 2: Vaccination Campaign Scheduling

**Problem**: Mass vaccination planned for District X

**MVP 1 solution**:
- "District X at HIGH risk this week → reschedule"

**MVP 2 solution**:
```
Mon-Tue: Low risk → Proceed with campaign
Wed-Thu: High risk → Pause campaign
Fri-Sun: Moderate risk → Resume with caution

→ Campaign proceeds on safe days only
→ No total cancellation needed
```

### Use Case 3: Vaccine Delivery Routing

**Problem**: Delivery truck visits 10 facilities over 5 days

**MVP 1 solution**:
- "3 facilities HIGH risk → skip all 3"

**MVP 2 solution**:
```
Route optimization:
Day 1: Visit Facilities 1, 2, 3 (all low risk Mon)
Day 2: Visit Facilities 4, 5 (low risk Tue)
Day 3: Skip Facilities 6, 7 (high risk Wed)
Day 4: Visit Facilities 6, 7 (risk drops Thu)
Day 5: Visit Facilities 8, 9, 10 (low risk Fri)

→ All facilities served, optimal timing
```

### Use Case 4: Emergency Resource Prioritization

**Problem**: Heat wave forecast, 50 facilities, 5 emergency cooling units

**MVP 1 solution**:
- "Rank top 5 by risk → deploy cooling units"

**MVP 2 solution**:
```
Priority Matrix:
  Mon Tue Wed Thu Fri Sat Sun
A  L   L   H   H   M   L   L  → Deploy Wed morning
B  M   M   M   H   H   H   M  → Deploy Thu morning
C  L   L   L   L   L   M   H  → Deploy Sat morning
D  H   H   M   L   L   L   L  → Deploy Mon morning
E  M   H   H   H   M   M   L  → Deploy Tue morning

→ 5 units cover 5 facilities with temporal rotation
→ vs static deployment covering only 5 all week
```

---

## Model Evaluation

### Metrics (Per Day)

For each of the 7 days:
- Precision: Of days predicted HIGH risk, % that actually failed
- Recall: Of days that failed, % we predicted
- F1-Score: Harmonic mean of precision/recall
- AUROC: Area under ROC curve

**Target performance**:
- Per-day Precision ≥ 65%
- Per-day Recall ≥ 70%
- Overall F1 ≥ 0.65

### Temporal Metrics (New)

**Early Warning Lead Time**:
- "How many days in advance do we detect high-risk periods?"
- Measure: Average days between prediction and failure
- Target: ≥2 days lead time

**Consecutive Day Accuracy**:
- "Do we correctly identify 2-3 day failure windows?"
- Measure: Precision on consecutive failure days
- Target: ≥70% for multi-day events

**Peak Day Identification**:
- "Do we correctly identify the WORST day in a high-risk period?"
- Measure: % of time argmax(predicted) == argmax(actual)
- Target: ≥75%

### Confusion Matrix (Example: Day 3)

```
                Predicted Failure Day 3
                NO          YES
Actual    NO    750 (TN)    50 (FP)    Precision = 60/(60+50) = 55%
Failure   YES   20 (FN)     60 (TP)    Recall = 60/(60+20) = 75%

F1 = 2 × (0.55 × 0.75) / (0.55 + 0.75) = 0.63
```

Repeat for all 7 days, then average.

---

## Implementation Timeline

### Week 1: Data Collection (Same as MVP 1)
- Fetch facilities + weather
- Already complete from MVP 1 foundation

### Week 2: Feature Engineering for Temporal Model
**Day 8-9**: Restructure data for daily predictions
- Create 7 weather feature sets (day 1, day 2, ..., day 7)
- Create 7 target variables (failure day 1, ..., day 7)

**Day 10**: Create synthetic daily failures
- Implement `predict_failure_per_day()` function
- Generate training data with temporal variation

**Day 11**: Train/test split
- Split facilities 70/15/15 (train/val/test)
- Ensure same facility not in multiple sets

### Week 3: Model Training
**Day 12-14**: Train multi-output model
- RandomForest with MultiOutputClassifier
- Hyperparameter tuning (per-day or global)
- Feature importance per day

### Week 4: Visualization & Demo
**Day 15-16**: Create visualizations
- Daily risk heatmap
- Interactive map with daily breakdown
- Timeline view

**Day 17**: Build prediction pipeline
- Input: Facility + 7-day forecast
- Output: 7 daily failure probabilities + recommendations

**Day 18**: Validation
- Test on extreme cases (heat waves, power outages)
- Calculate temporal metrics

### Week 5-6: Documentation & Presentation
**Day 19-24**: Same as MVP 1
- Clean notebooks
- Create presentation
- Practice demo

---

## Deliverables for Professor

### 1. Interactive Daily Risk Map
- Click facility → see 7-day forecast
- Color-coded by worst day risk
- Timeline slider (Day 1 → Day 7)

### 2. Facility Risk Report (Example)

```
TURKANA HEALTH CENTER - 7-Day Forecast
Generated: 2024-12-09 09:00 AM

        Day    Risk    Temp   Clouds  Power    Recommendation
Mon  1  2024-12-10  12%    32°C   30%    Solar    ✓ Safe - Proceed
Tue  2  2024-12-11  18%    34°C   45%    Solar    ✓ Safe - Monitor
Wed  3  2024-12-12  75%    38°C   65%    Solar    ⚠ HIGH - Deploy backup
Thu  4  2024-12-13  68%    37°C   70%    Solar    ⚠ HIGH - Maintain backup
Fri  5  2024-12-14  32%    35°C   55%    Solar    △ Moderate - Monitor
Sat  6  2024-12-15  15%    33°C   40%    Solar    ✓ Safe - Retrieve backup
Sun  7  2024-12-16  10%    31°C   35%    Solar    ✓ Safe - Normal ops

PRIORITY ACTIONS:
1. Deploy generator by Tuesday evening (before Wed spike)
2. Maintain backup power Wed-Thu (48-hour window)
3. Retrieve generator Friday evening (risk subsides)
4. Next vaccine delivery: Monday 12/16 (low risk)

RISK FACTORS:
- Heat wave forecast Wed-Thu (38°C, 37°C)
- High cloud cover → Solar battery stress
- Dry season → Grid unreliability in area
```

### 3. District-Level Dashboard

**Aggregated view for district health officer:**

```
DISTRICT: Turkana County
Week of: Dec 9-15, 2024

HIGH-RISK FACILITIES (>60% any day):
  Facility A: Wednesday (75%)
  Facility B: Friday (68%)
  Facility C: Thursday (65%)

RESOURCE NEEDS:
  - 2 generators needed Wed-Thu
  - 1 cooling unit needed Fri-Sat
  - Fuel delivery: Tuesday (before spike)

DELIVERY SCHEDULE RECOMMENDATIONS:
  ✓ Safe days: Monday, Tuesday, Saturday, Sunday
  ⚠ Avoid: Wednesday, Thursday
  △ Caution: Friday

WEATHER SUMMARY:
  - Heat wave: Wed-Thu (38°C)
  - High cloud cover: Wed-Fri (60-70%)
  - Cooling trend: Fri-Sun (35°C → 31°C)
```

### 4. Presentation Additions (vs MVP 1)

**New slides**:
- Slide 6: "Daily Risk Forecast (7-Day Breakdown)"
  - Show heatmap: Facilities × Days
  - Highlight temporal patterns

- Slide 7: "Use Case: Generator Deployment Scheduling"
  - Show how 1 generator serves 3 facilities
  - Cost savings: 67%

- Slide 8: "Model Performance - Temporal Metrics"
  - Per-day precision/recall
  - Early warning lead time: 2.3 days average
  - Peak day identification: 78% accuracy

---

## Comparison: MVP 1 vs MVP 2

| Feature | MVP 1 (Binary) | MVP 2 (Temporal) |
|---------|---------------|------------------|
| **Prediction** | High/Low risk (week) | Daily probabilities (7 days) |
| **Granularity** | Coarse | Fine |
| **Visualization** | Risk map (static) | Heatmap + timeline |
| **Intervention** | "Delay delivery" | "Deploy generator Tuesday" |
| **Resource planning** | Weekly allocation | Daily scheduling |
| **Model complexity** | Single classifier | Multi-output (7 classifiers) |
| **Training time** | ~5 minutes | ~15 minutes |
| **Interpretation** | Simple | Moderate |
| **Data requirements** | Same | Same (but 7 targets) |
| **Implementation time** | 6 weeks | +1 week (7 weeks total) |
| **Impact** | 20-25% wastage reduction | 25-35% wastage reduction |

**Recommendation**: Build MVP 1 first (6 weeks), then upgrade to MVP 2 (1 additional week)

---

## Quick Start: Upgrading from MVP 1 to MVP 2

### If You Already Completed MVP 1:

**Step 1: Modify feature engineering (2 hours)**
```python
# Change from aggregate to daily features
# Instead of: max_temp_7d = max(temps)
# Use: temp_day1, temp_day2, ..., temp_day7

features = []
for day in range(1, 8):
    features.append({
        f'temp_day{day}': weather_forecast[day]['temp'],
        f'clouds_day{day}': weather_forecast[day]['clouds'],
        f'humidity_day{day}': weather_forecast[day]['humidity']
    })
```

**Step 2: Create 7 target variables (1 hour)**
```python
# Instead of: high_risk = 1 if any_day_fails else 0
# Use: failure_day1, failure_day2, ..., failure_day7

for day in range(1, 8):
    df[f'failure_day{day}'] = predict_failure_on_day(facility, day)
```

**Step 3: Train multi-output model (1 hour)**
```python
from sklearn.multioutput import MultiOutputClassifier

y_columns = [f'failure_day{day}' for day in range(1, 8)]
y = df[y_columns]

model = MultiOutputClassifier(RandomForestClassifier())
model.fit(X_train, y_train)
```

**Step 4: Update visualizations (3 hours)**
- Create heatmap (Facilities × Days)
- Update map with daily breakdown popup
- Add timeline view

**Total upgrade time: 1 week (7 hours active coding + testing)**

---

## Final Recommendation

### For Your MVP:

**Option A: MVP 1 Only (6 weeks)**
- Simpler, faster to complete
- Still demonstrates core concept
- Good for tight deadline

**Option B: MVP 1 → MVP 2 (7 weeks)**
- More impressive demo
- Stronger publication potential
- Shows temporal forecasting skill

**Option C: MVP 2 Only (6 weeks)**
- Skip binary classification entirely
- Go straight to daily predictions
- More ambitious but doable

**My recommendation**:
1. Build MVP 1 first (weeks 1-6)
2. Demo to professor
3. IF professor is impressed and wants more → upgrade to MVP 2 (week 7)
4. IF time is tight → submit MVP 1 as-is

This way you have a working MVP on time, with clear path to enhance it.

---

## Questions to Consider

**Before choosing MVP 2:**

1. **Do you have 7 weeks instead of 6?**
   - MVP 2 adds ~1 week to timeline
   - Can you afford the extra time?

2. **Is temporal granularity valuable for your presentation?**
   - Does professor care about "when" vs just "if"?
   - Are you targeting deployment with daily scheduling needs?

3. **Are you comfortable with multi-output models?**
   - Slightly more complex than binary classification
   - More hyperparameters to tune

4. **Do you want to showcase advanced skills?**
   - MVP 2 shows time-series thinking
   - Better for job applications / publications

**If all answers are YES → Go for MVP 2**
**If any answer is NO → Stick with MVP 1, upgrade later if time permits**

---

## Ready to Start?

**If building MVP 2 from scratch:**
Follow the same Week 1 setup as MVP 1 (already complete!), then use this plan for Weeks 2-7.

**If upgrading from MVP 1:**
Start at "Modify feature engineering" above.

**Either way, you now have a complete roadmap! 🚀**
