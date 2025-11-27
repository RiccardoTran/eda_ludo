# MVP Plan: Cold Chain Failure Risk Prediction for Kenya

## Executive Summary

**Goal**: Build a working Minimum Viable Product that predicts 7-day vaccine cold chain failure risk for health facilities in Kenya, demonstrable to your professor in 4-6 weeks.

**Why Kenya**: Best data availability, active cold chain monitoring programs, English documentation, manageable size (~10,000 health facilities).

**Core MVP Question**: "Given weather forecasts and facility characteristics, can we predict which clinics have HIGH risk of cold chain failure in the next 7 days?"

---

## MVP Scope Definition

### ✅ INCLUDED (Must Have)

**Geographic Scope:**
- **One country only**: Kenya
- **Focus regions**: 3-5 counties with diverse climates (e.g., Nairobi, Turkana, Mombasa)
- **Facilities**: 50-200 health facilities (enough for statistical validity, small enough to manage)

**Prediction Task:**
- **Target**: Binary classification - "High Risk" vs "Low Risk" for next 7 days
- **Time horizon**: 7-day forecast (simplified from 24h/48h/72h)
- **Update frequency**: Weekly predictions (not daily)

**Data Inputs:**
- ✅ Weather forecast (7-day): Temperature, solar radiation, humidity
- ✅ Facility location (lat/lon)
- ✅ Facility type (clinic/health center/hospital)
- ✅ Power source (grid/solar/diesel/none)
- ✅ Historical temperature patterns (seasonal baseline)
- ✅ Month/season (temporal features)

**Model:**
- Simple classification model (Random Forest or Logistic Regression)
- Interpretable features (no deep learning)
- Baseline comparison (predict "always safe" vs your model)

**Output:**
- Risk classification: "High Risk" or "Low Risk"
- Top 3 risk factors (e.g., "Heat wave forecast", "No power source", "Dry season")
- Confidence score (0-100%)

**Validation:**
- If available: Compare predictions to historical cold chain incident reports
- If not available: Use synthetic "failures" based on extreme weather + poor infrastructure

**Deliverables for Professor:**
1. Jupyter notebook with full analysis
2. Interactive map showing facilities colored by risk level
3. 10-slide presentation explaining approach + results
4. 2-page summary report

### ❌ NOT INCLUDED (Future Work)

- ❌ Real-time IoT data integration (use facility characteristics instead)
- ❌ Multiple countries (Kenya only)
- ❌ Hourly/daily predictions (weekly only)
- ❌ Cost-benefit analysis (vaccine wastage $)
- ❌ Delivery scheduling recommendations (just show risk)
- ❌ Mobile app or API deployment (notebook demo only)
- ❌ Deep learning / complex models (keep interpretable)
- ❌ Battery state-of-charge tracking (too detailed)

---

## MVP Implementation Plan (4-6 Weeks)

### Week 1: Data Collection & Setup

**Objective**: Gather all necessary data and set up analysis environment

#### Day 1-2: Weather Data
- [x] Sign up for weather forecast API
  - **Option A**: OpenWeatherMap (free tier: 1000 calls/day) ✅ RECOMMENDED
    - URL: https://openweathermap.org/api
    - Get 7-day forecast: temp, humidity, clouds, solar radiation
  - **Option B**: Visual Crossing (free tier: 1000 records/day)
    - URL: https://www.visualcrossing.com/weather-api/
- [x] Test API with 5 sample locations in Kenya
- [x] Download historical weather data for Kenya (2023-2024)
  - NASA POWER API (you already have this in your list)

**Deliverable**: `weather_data_collection.ipynb` with working API calls

#### Day 3-4: Health Facility Data
- [x] Download Kenya health facility data
  - **Source 1**: Kenya Master Health Facility List (KMHFL)
    - URL: http://kmhfl.health.go.ke/
    - Contains: Facility name, location, type, ownership
  - **Source 2**: Healthsites.io (backup/supplement)
    - URL: https://healthsites.io/api/docs/
    - Filter for Kenya facilities
- [x] Clean and geocode facilities (ensure lat/lon)
- [x] Select 50-200 facilities across 3-5 counties

**Deliverable**: `facilities.csv` with columns:
```
facility_id, name, latitude, longitude, county, facility_type, power_source, population_density
```

#### Day 5-7: Baseline Data Collection
- [x] Get Kenya electrification data (from your High-Res Electrification Dataset)
- [x] Get population density (from your Africa Population Density dataset)
- [x] Create historical cold chain incident dataset (if available)
  - Search for Kenya MOH cold chain reports
  - If not available: Create synthetic failures based on extreme weather
- [x] Set up project structure:
  ```
  EDA_Ludo/
  ├── data/
  │   ├── raw/
  │   │   ├── facilities.csv
  │   │   ├── weather_historical.csv
  │   │   └── incidents.csv (if available)
  │   └── processed/
  ├── notebooks/
  │   ├── 01_data_collection.ipynb
  │   ├── 02_eda.ipynb
  │   ├── 03_model_training.ipynb
  │   └── 04_prediction_demo.ipynb
  ├── src/
  │   ├── data_loader.py
  │   ├── feature_engineering.py
  │   └── model.py
  └── outputs/
      ├── figures/
      └── reports/
  ```

**Deliverable**: Complete data folder with all necessary files

---

### Week 2: Exploratory Data Analysis (EDA)

**Objective**: Understand data patterns and identify risk factors

#### Day 8-10: Weather Pattern Analysis
- [x] Analyze historical weather patterns in Kenya
  - Identify heat wave periods (temp >35°C)
  - Identify rainy/dry seasons
  - Analyze solar radiation variability (cloudy periods)
- [x] Create visualizations:
  - Temperature distribution by county
  - Seasonal patterns (monthly averages)
  - Extreme weather event frequency

**Deliverable**: `02_eda.ipynb` with weather analysis

#### Day 11-12: Facility Infrastructure Analysis
- [x] Map facility locations (interactive map)
- [x] Analyze facility characteristics:
  - Distribution by type (clinic/center/hospital)
  - Power source distribution
  - Distance from grid infrastructure
  - Population density around facilities
- [x] Create visualizations:
  - Map of facilities colored by power source
  - Electrification rate vs facility density

**Deliverable**: Interactive map + infrastructure analysis

#### Day 13-14: Risk Factor Identification
- [x] Define "high risk" scenarios (synthetic if no incident data):
  - Temperature >35°C + No power source = High Risk
  - Temperature >38°C + Solar power + Cloudy forecast = High Risk
  - Dry season + Grid area with <50% reliability = High Risk
- [x] Analyze correlation between:
  - Extreme weather ↔ Facility infrastructure
  - Season ↔ Power reliability
  - Population density ↔ Patient load (proxy)
- [x] Create risk score formula (manual, for validation):
  ```python
  Risk_Score =
    (Temperature - 30) * 2 +           # Heat stress
    (Cloud_Cover / 10) * 1 +           # Solar reduction
    (No_Power_Source) * 20 +           # Infrastructure gap
    (Dry_Season) * 5                   # Seasonal risk
  ```

**Deliverable**: Risk factor analysis + preliminary risk scoring

---

### Week 3: Model Development

**Objective**: Build and train classification model

#### Day 15-17: Feature Engineering
- [x] Create model features:

**Weather Features (7-day forecast):**
```python
- max_temp_7d: Maximum temperature in next 7 days
- avg_temp_7d: Average temperature in next 7 days
- temp_above_35_days: Number of days >35°C
- temp_above_38_days: Number of days >38°C
- min_solar_radiation_7d: Minimum solar radiation
- avg_cloud_cover_7d: Average cloud cover (%)
- heat_wave_indicator: Boolean (3+ consecutive days >35°C)
```

**Facility Features:**
```python
- facility_type_encoded: One-hot encoding (clinic/center/hospital)
- power_source_encoded: One-hot encoding (grid/solar/diesel/none)
- has_backup_power: Boolean (solar/diesel present)
- electrification_rate: Area electrification % (from dataset)
- population_density: People per km²
- distance_to_grid: Distance to nearest transmission line (km)
```

**Temporal Features:**
```python
- month: Integer (1-12)
- is_dry_season: Boolean (Jan-Mar, Jun-Oct)
- is_rainy_season: Boolean (Apr-May, Nov-Dec)
```

**Target Variable:**
```python
- high_risk: Boolean (1 = High Risk, 0 = Low Risk)
```

**How to create target (if no incident data):**
```python
high_risk = 1 if (
  (max_temp_7d > 35 AND power_source == "none") OR
  (max_temp_7d > 38 AND power_source == "solar" AND avg_cloud_cover > 60) OR
  (temp_above_35_days >= 3 AND electrification_rate < 30) OR
  (is_dry_season AND electrification_rate < 20)
) else 0
```

**Deliverable**: `feature_engineering.py` + feature dataset

#### Day 18-20: Model Training
- [x] Split data: 70% train, 15% validation, 15% test
- [x] Train baseline model: "Always predict Low Risk"
- [x] Train candidate models:
  - **Logistic Regression** (simple, interpretable)
  - **Random Forest** (handles non-linear relationships)
  - **Gradient Boosting** (XGBoost or LightGBM)
- [x] Hyperparameter tuning (GridSearchCV)
- [x] Feature importance analysis

**Metrics to track:**
```python
- Accuracy: Overall correct predictions
- Precision (High Risk): When model says High, how often correct?
- Recall (High Risk): Of actual High Risk cases, how many caught?
- F1-Score: Balance of precision/recall
- ROC-AUC: Overall classification performance
```

**Target Performance:**
- Precision (High Risk) >70%
- Recall (High Risk) >80%
- Better than baseline by >30%

**Deliverable**: `03_model_training.ipynb` with trained models

#### Day 21: Model Interpretation
- [x] Extract feature importances
- [x] Create SHAP values (explains individual predictions)
- [x] Identify top risk factors:
  - Which features most predict High Risk?
  - Example: "Temperature >38°C accounts for 40% of High Risk predictions"
- [x] Validate model logic (sanity checks):
  - Facilities with no power → high risk?
  - Heat waves → high risk?
  - Cool weather + grid power → low risk?

**Deliverable**: Feature importance plots + interpretation

---

### Week 4: MVP Demo & Validation

**Objective**: Create demonstrable product and validate results

#### Day 22-24: Build Prediction Pipeline
- [x] Create end-to-end prediction script:
  ```python
  # predict_risk.py
  def predict_facility_risk(facility_id, forecast_date):
      # 1. Get facility characteristics
      # 2. Fetch 7-day weather forecast (API call)
      # 3. Engineer features
      # 4. Run model prediction
      # 5. Return: risk_level, confidence, top_factors
      return {
          "facility_id": facility_id,
          "facility_name": "Turkana Health Center",
          "forecast_date": "2024-12-15",
          "risk_level": "High Risk",
          "confidence": 85,
          "top_risk_factors": [
              "Heat wave forecast (38°C for 4 days)",
              "No backup power source",
              "Dry season (low grid reliability)"
          ],
          "recommendation": "Consider delaying vaccine delivery until Dec 22"
      }
  ```

- [x] Test on 10 sample facilities
- [x] Create prediction output CSV:
  ```
  facility_id, facility_name, county, risk_level, confidence, factor_1, factor_2, factor_3
  ```

**Deliverable**: `predict_risk.py` + sample predictions

#### Day 25-26: Create Interactive Demo
- [x] Build interactive map using Folium or Plotly:
  - Red markers: High Risk facilities
  - Green markers: Low Risk facilities
  - Click marker → show facility details + risk factors
- [x] Create dashboard-style visualization:
  - Summary stats: "15 of 100 facilities at High Risk this week"
  - Risk distribution by county
  - Weather forecast overlay (heat map of temperature)
- [x] Export to HTML for easy sharing

**Deliverable**: `risk_map.html` (interactive map)

#### Day 27-28: Validation & Results Analysis
- [x] If incident data available:
  - Compare predictions to actual cold chain breaks
  - Calculate precision/recall on real incidents
- [x] If synthetic data:
  - Validate model logic with extreme cases
  - Test: Does model predict high risk for obvious scenarios?
    - Example: 40°C heat wave + no power → should be High Risk
- [x] Calculate impact estimate:
  - "If 20% of High Risk facilities delay deliveries → save X vaccines"
- [x] Identify limitations and future work

**Deliverable**: Validation results + impact analysis

---

### Week 5-6: Documentation & Presentation

**Objective**: Prepare materials for professor presentation

#### Week 5: Create Deliverables

**1. Jupyter Notebook (Master Analysis)**
- Combined notebook: `MVP_Cold_Chain_Kenya.ipynb`
- Sections:
  1. Introduction & Problem Statement
  2. Data Collection & Processing
  3. Exploratory Data Analysis
  4. Feature Engineering
  5. Model Training & Evaluation
  6. Predictions & Risk Map
  7. Validation & Results
  8. Limitations & Future Work
- Include all visualizations inline
- Clear markdown explanations between code cells

**2. 2-Page Summary Report (PDF)**
Structure:
```
Page 1:
- Problem: 25-30% vaccine wastage in SSA due to cold chain failures
- Objective: Predict 7-day failure risk for Kenya health facilities
- Approach: ML model using weather forecasts + facility data
- Data: 100 facilities, 7-day weather forecasts, infrastructure data

Page 2:
- Results:
  - Model achieves 78% precision, 85% recall on High Risk
  - Identified 15 high-risk facilities this week
  - Top risk factors: Heat waves (40%), No power (30%), Dry season (20%)
- Impact: Potential 20-25% reduction in vaccine wastage
- Next Steps: Expand to more countries, integrate IoT data, pilot deployment
```

**3. Slide Deck (10 slides)**
```
Slide 1: Title
- Cold Chain Failure Risk Prediction for Kenya
- [Your names, date]

Slide 2: Problem Statement
- 25-30% vaccine wastage in Sub-Saharan Africa
- Existing solutions: IoT monitoring (only 10% facilities)
- Gap: 90% of facilities lack predictive tools

Slide 3: Our Approach
- Predict 7-day cold chain failure risk
- Use free weather forecasts + facility data
- Target: Clinic staff delivery scheduling decisions

Slide 4: Data Sources
- Kenya health facilities: 100 facilities across 5 counties
- Weather forecasts: OpenWeatherMap API (7-day)
- Infrastructure: Electrification data, population density
- Validation: [Historical incidents OR synthetic scenarios]

Slide 5: How It Works (Flow Diagram)
- Input: Facility + 7-day weather forecast
- Features: Temperature, solar, power source, season
- Model: Random Forest classifier
- Output: High/Low Risk + top factors

Slide 6: Feature Importance
- Bar chart showing top predictive features
- Max temperature (40%), Power source (25%), Cloud cover (20%), etc.

Slide 7: Risk Map (Interactive)
- Screenshot of Kenya map with red/green facility markers
- "15 high-risk facilities identified this week"

Slide 8: Model Performance
- Confusion matrix
- Metrics: Precision 78%, Recall 85%, F1 81%
- Comparison to baseline: +35% improvement

Slide 9: Example Prediction
- Case study: Turkana Health Center
- Risk: High (85% confidence)
- Factors: Heat wave (38°C), No backup power, Dry season
- Recommendation: Delay delivery 5 days

Slide 10: Impact & Next Steps
- Impact: 20-25% potential vaccine wastage reduction
- Limitations: Synthetic validation, Kenya only, weekly updates
- Future: Expand to 10 countries, integrate IoT, deploy as mobile app
```

**4. GitHub Repository (Code Sharing)**
- Clean, documented code
- README.md with setup instructions
- requirements.txt for dependencies
- Sample data files (anonymized if needed)

#### Week 6: Practice & Polish

**Day 36-40: Rehearsal**
- [x] Practice 15-minute presentation
- [x] Prepare for questions:
  - "How did you validate without incident data?"
  - "What's the accuracy of your weather forecasts?"
  - "Why Kenya specifically?"
  - "How much would this cost to deploy?"
  - "What if facilities don't follow recommendations?"
- [x] Refine visualizations for clarity
- [x] Proofread all documents

**Day 41-42: Buffer Days**
- Handle any last-minute issues
- Final quality check
- Prepare demo environment (test that notebook runs end-to-end)

---

## MVP Success Criteria

### Technical Criteria

✅ **Data Collection**
- [ ] 50+ health facilities with complete data (location, type, power source)
- [ ] 7-day weather forecasts successfully fetched for all facilities
- [ ] Historical weather patterns analyzed (1+ year of data)

✅ **Model Performance**
- [ ] Precision (High Risk) ≥ 70%
- [ ] Recall (High Risk) ≥ 75%
- [ ] Model beats baseline by ≥ 30%
- [ ] Feature importance makes logical sense

✅ **Visualization & Demo**
- [ ] Interactive map showing risk levels works
- [ ] Can generate predictions for any facility in <30 seconds
- [ ] Prediction explanations (top 3 factors) are human-readable

✅ **Documentation**
- [ ] Jupyter notebook runs end-to-end without errors
- [ ] Code is commented and readable
- [ ] README explains how to reproduce results

### Presentation Criteria

✅ **Clarity**
- [ ] Professor understands problem within 2 minutes
- [ ] Approach is clearly explained (no jargon overload)
- [ ] Results are visually compelling (map + charts)

✅ **Rigor**
- [ ] Data sources are credible and cited
- [ ] Model validation is reasonable (even if synthetic)
- [ ] Limitations are acknowledged

✅ **Impact**
- [ ] Clear connection to real-world problem (vaccine wastage)
- [ ] Quantified potential impact (% wastage reduction)
- [ ] Feasible next steps identified

---

## Data Sources Summary

### 1. Health Facility Data
**Primary Source: Kenya Master Health Facility List (KMHFL)**
- URL: http://kmhfl.health.go.ke/
- Data: ~10,000 facilities with GPS, type, ownership
- Format: CSV download or API
- Cost: FREE

**Backup: Healthsites.io**
- URL: https://healthsites.io/api/docs/
- Filter: `country=Kenya`
- Cost: FREE

### 2. Weather Forecast Data
**Primary: OpenWeatherMap**
- URL: https://openweathermap.org/api
- Free tier: 1,000 calls/day (enough for 100 facilities updated weekly)
- Data: 7-day forecast (temp, humidity, clouds, pressure)
- Cost: FREE

**Historical Weather: NASA POWER**
- URL: https://power.larc.nasa.gov/
- Data: Historical temperature, solar radiation (1981-present)
- Cost: FREE

### 3. Infrastructure Data (You Already Have)
- **Electrification**: High-Resolution Gridded Dataset (Mendeley)
- **Population**: High-Res Population Density Maps (HumData)
- **Energy Infrastructure**: Africa Energy Tracker (grid lines)

### 4. Validation Data (If Available)
**Search for:**
- Kenya Ministry of Health cold chain reports
- WHO Kenya immunization program data
- Temperature logger data from UNICEF programs

**If unavailable:** Use synthetic validation (rule-based failures)

---

## Risk Mitigation Plan

### Risk 1: Can't Find Health Facility Data
**Mitigation:**
- Use Healthsites.io (open data, 100% available)
- Manually collect from Kenya MOH website
- Reduce scope to 30-50 facilities instead of 100

### Risk 2: Weather API Limits
**Mitigation:**
- OpenWeatherMap free tier = 1000 calls/day (plenty for 100 facilities)
- If exceeded: Use Visual Crossing (separate 1000 limit)
- Fallback: Use historical weather averages instead of real forecasts

### Risk 3: No Incident Data for Validation
**Mitigation:**
- Use synthetic validation (rule-based failures)
- Validate on extreme cases (heat waves should = high risk)
- Frame as "proof-of-concept" pending real validation

### Risk 4: Model Performance Poor
**Mitigation:**
- Simplify to easier problem: Predict "extreme risk" only (temp >38°C)
- Use rule-based system if ML underperforms
- Focus on feature analysis instead of prediction accuracy

### Risk 5: Time Constraints
**Mitigation:**
- Week 1-2 are critical (data collection) - start immediately
- Week 3 can be simplified (basic model instead of tuning)
- Week 6 is buffer - can skip if needed

---

## MVP Presentation Outline (15 minutes)

### Part 1: Problem & Motivation (3 min)
- Cold chain failures waste 25-30% of vaccines in Africa
- Existing solutions (IoT) only cover 10% of facilities
- Our approach: Predictive tool using free weather data

### Part 2: Data & Methods (4 min)
- Kenya health facilities (100 facilities, 5 counties)
- 7-day weather forecasts (temperature, solar, clouds)
- Random Forest model (temperature + power source + season → risk)
- Show data collection process + EDA highlights

### Part 3: Results (5 min)
- Model performance: 78% precision, 85% recall
- Interactive risk map demo (show live predictions)
- Example prediction: "Turkana Health Center - High Risk"
- Feature importance: Temperature most predictive

### Part 4: Impact & Next Steps (3 min)
- Potential 20-25% reduction in vaccine wastage
- Next steps: Expand to 10 countries, integrate IoT, pilot study
- Acknowledge limitations: Synthetic validation, Kenya only
- Q&A

---

## Recommended Tech Stack

**Languages & Core Tools:**
- Python 3.9+
- Jupyter Notebook

**Data Processing:**
- pandas (data manipulation)
- numpy (numerical operations)
- geopandas (geospatial analysis)

**Visualization:**
- matplotlib, seaborn (static plots)
- plotly or folium (interactive maps)

**Machine Learning:**
- scikit-learn (Random Forest, Logistic Regression)
- xgboost or lightgbm (Gradient Boosting)
- shap (model interpretation)

**API & Data Collection:**
- requests (API calls)
- json (data parsing)

**Geospatial:**
- geopy (distance calculations)
- shapely (geospatial operations)

**Requirements.txt:**
```
pandas==2.1.0
numpy==1.25.0
scikit-learn==1.3.0
xgboost==2.0.0
matplotlib==3.7.1
seaborn==0.12.2
plotly==5.16.0
folium==0.14.0
geopandas==0.13.2
requests==2.31.0
shap==0.42.1
jupyter==1.0.0
```

---

## Quick Start Checklist (First 3 Days)

### Day 1: Environment Setup
- [ ] Create new conda environment or venv
- [ ] Install required packages (requirements.txt)
- [ ] Set up project folder structure
- [ ] Create GitHub repo (optional but recommended)

### Day 2: API Access
- [ ] Sign up for OpenWeatherMap API (free tier)
- [ ] Get API key and test with 3 sample coordinates
- [ ] Verify 7-day forecast endpoint works
- [ ] Document API response format

### Day 3: Facility Data
- [ ] Download Kenya facility data from KMHFL or Healthsites.io
- [ ] Load into pandas DataFrame
- [ ] Check data quality (missing lat/lon, duplicates)
- [ ] Select 50-100 facilities across diverse counties
- [ ] Export to `data/raw/facilities.csv`

**If these 3 days go well, you're on track for MVP success!**

---

## Estimated Effort Distribution

| Phase | Time | Complexity | Importance |
|-------|------|------------|------------|
| Data Collection | 7 days | Medium | CRITICAL |
| EDA | 7 days | Low | High |
| Model Development | 7 days | Medium-High | CRITICAL |
| Demo & Validation | 7 days | Medium | High |
| Documentation | 10 days | Low | High |
| Buffer | 4 days | - | - |
| **TOTAL** | **42 days (6 weeks)** | - | - |

**Minimum viable timeline:** 4 weeks (cut buffer + reduce EDA depth)

---

## What Success Looks Like

### For Your Professor:
✅ "I can see the problem is real and important"
✅ "The approach is technically sound and well-executed"
✅ "The results are promising and visualizations are clear"
✅ "This could be expanded into a larger project"

### For You:
✅ Working end-to-end ML pipeline (data → model → predictions)
✅ Interactive demo you can show to others
✅ Foundation for expanding to full 10-idea comparison
✅ Portfolio piece for job applications
✅ Potential publication in conference/journal

### For Real-World Impact:
✅ Proof-of-concept that weather forecasts can predict cold chain risk
✅ Demonstration that low-cost solutions can work without IoT
✅ Foundation for pilot deployment with Kenya Ministry of Health
✅ Basis for grant applications (Gavi, WHO, Bill & Melinda Gates Foundation)

---

## Next Immediate Steps (This Week)

1. **TODAY: Review this plan**
   - Agree on scope (Kenya, 7-day, 100 facilities, 6 weeks)
   - Assign responsibilities if working in a team

2. **Tomorrow: Start data collection**
   - Sign up for OpenWeatherMap API
   - Download Kenya facility data
   - Test API with 5 sample locations

3. **This week: Complete Week 1 tasks**
   - Facility data cleaned and ready
   - Weather API working reliably
   - Project structure set up
   - First EDA notebook started

**Want me to help you start any of these steps right now?**
