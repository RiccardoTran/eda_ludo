# Cold Chain Failure Risk Prediction - MVP

## Project Overview
Predict 7-day vaccine cold chain failure risk for health facilities in Kenya using weather forecasts and facility characteristics.

**Goal**: Demonstrate that weather forecasts + facility infrastructure data can predict cold chain failures, enabling proactive delivery scheduling decisions.

**Timeline**: 6 weeks (MVP)
**Target Accuracy**: 75%+ precision, 80%+ recall on High Risk predictions

## Problem Statement
- 25-30% of vaccines wasted in Sub-Saharan Africa due to cold chain failures
- Existing IoT monitoring (reactive, only 10% of facilities)
- Gap: No predictive tool for 24-72h delivery scheduling decisions

## Approach
**Input**: Health facility + 7-day weather forecast
**Output**: Risk level (High/Low) + Top 3 risk factors + Confidence score
**Model**: Random Forest classifier (interpretable, robust)

## Quick Start

### 1. Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. API Keys Setup
Create `.env` file in project root:
```
OPENWEATHER_API_KEY=your_key_here
```

Sign up for free: https://openweathermap.org/api

### 3. Run Data Collection
```bash
jupyter notebook notebooks/01_data_collection.ipynb
```

### 4. Run Analysis
```bash
jupyter notebook notebooks/02_eda.ipynb
jupyter notebook notebooks/03_model_training.ipynb
jupyter notebook notebooks/04_prediction_demo.ipynb
```

## Project Structure
```
mvp_cold_chain/
├── README.md
├── requirements.txt
├── .env (create this - not in git)
├── data/
│   ├── raw/              # Original data files
│   ├── processed/        # Cleaned, feature-engineered data
│   └── external/         # External datasets (electrification, population)
├── notebooks/
│   ├── 00_country_risk_ranking.ipynb    # Why Kenya?
│   ├── 01_data_collection.ipynb         # Fetch facilities + weather
│   ├── 02_eda.ipynb                     # Exploratory analysis
│   ├── 03_model_training.ipynb          # Build & train model
│   └── 04_prediction_demo.ipynb         # Interactive demo
├── src/
│   ├── data_loader.py         # Load facilities, weather, infrastructure
│   ├── feature_engineering.py # Create model features
│   ├── model.py               # Train/predict functions
│   └── visualization.py       # Maps, plots
├── outputs/
│   ├── figures/    # EDA plots, feature importance
│   ├── maps/       # Interactive risk maps (HTML)
│   └── reports/    # Final presentation, report
└── config/
    └── config.yaml # Model parameters, API endpoints
```

## Data Sources

### Health Facilities (100 facilities)
- **Primary**: Kenya Master Health Facility List (KMHFL)
  - URL: http://kmhfl.health.go.ke/
  - Data: GPS, facility type, ownership
- **Backup**: Healthsites.io API
  - URL: https://healthsites.io/api/docs/

### Weather Forecasts (7-day)
- **OpenWeatherMap API** (free tier: 1000 calls/day)
  - URL: https://openweathermap.org/api/one-call-3
  - Data: Temperature, clouds, humidity, solar radiation

### Infrastructure Data
- **Electrification**: High-res gridded dataset (Mendeley)
- **Population**: High-res population density (HumData)
- **Grid proximity**: Africa Energy Tracker

## Model Features

### Weather Features (7-day forecast)
- `max_temp_7d`: Maximum temperature in next 7 days
- `avg_temp_7d`: Average temperature
- `temp_above_35_days`: Days with temp >35°C
- `temp_above_38_days`: Days with temp >38°C
- `min_solar_radiation_7d`: Minimum solar radiation
- `avg_cloud_cover_7d`: Average cloud cover (%)
- `heat_wave_indicator`: 3+ consecutive days >35°C

### Facility Features
- `facility_type`: Clinic/Health Center/Hospital
- `power_source`: Grid/Solar/Diesel/None
- `has_backup_power`: Boolean
- `electrification_rate`: Area electrification %
- `population_density`: People per km²
- `distance_to_grid`: Distance to transmission line (km)

### Temporal Features
- `month`: 1-12
- `is_dry_season`: Boolean (Jan-Mar, Jun-Oct)
- `is_rainy_season`: Boolean (Apr-May, Nov-Dec)

### Target Variable
- `high_risk`: Boolean (1 = High Risk, 0 = Low Risk)

## Success Criteria

### Technical
- [ ] 50+ facilities with complete data
- [ ] 7-day weather forecasts fetched successfully
- [ ] Model: Precision ≥70%, Recall ≥75%
- [ ] Beats baseline by ≥30%

### Deliverables
- [ ] Jupyter notebook (runs end-to-end)
- [ ] Interactive risk map (HTML)
- [ ] 10-slide presentation
- [ ] 2-page summary report

## Timeline

### Week 1: Data Collection
- Country risk ranking (justify Kenya)
- Weather API setup
- Kenya facility data (50-100 facilities)
- Infrastructure data integration

### Week 2: EDA
- Weather pattern analysis
- Facility infrastructure analysis
- Risk factor identification

### Week 3: Model Development
- Feature engineering
- Model training (Random Forest, XGBoost)
- Feature importance analysis

### Week 4: Demo & Validation
- Prediction pipeline
- Interactive map
- Validation with synthetic/real incidents

### Week 5-6: Documentation
- Clean notebooks
- Create presentation
- Write summary report
- Practice demo

## Team & Roles
[Add your team members and responsibilities here]

## Contact
[Your contact information]

## License
MIT License (or specify your license)

## Acknowledgments
- Kenya Ministry of Health (facility data)
- OpenWeatherMap (weather API)
- NASA POWER (historical climate data)
- World Bank (infrastructure data)
