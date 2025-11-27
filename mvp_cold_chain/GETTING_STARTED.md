# Getting Started with Cold Chain MVP

## 🎯 What We've Built So Far

### ✅ Project Structure
```
mvp_cold_chain/
├── README.md                          # Full project documentation
├── GETTING_STARTED.md                 # This file - quick start guide
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore rules
├── data/                              # Data storage
│   ├── raw/                           # Original data files
│   ├── processed/                     # Cleaned data
│   └── external/                      # External datasets
├── notebooks/                         # Jupyter notebooks
│   └── 00_country_risk_ranking.ipynb  # ✅ COMPLETE - Kenya justification
├── src/                               # Python modules
│   ├── weather_api.py                 # ✅ COMPLETE - Weather forecast fetching
│   └── facility_data_loader.py        # ✅ COMPLETE - Kenya facility data
├── outputs/                           # Results
│   ├── figures/                       # Charts and plots
│   ├── maps/                          # Interactive maps
│   └── reports/                       # Final deliverables
└── config/                            # Configuration files
```

### ✅ Completed Components

1. **Country Risk Ranking** (`00_country_risk_ranking.ipynb`)
   - Ranks 30 SSA countries by cold chain risk
   - Kenya ranks #8-10 (moderate-high risk)
   - Justifies Kenya selection for MVP

2. **Weather API Module** (`src/weather_api.py`)
   - Fetches 7-day forecasts from OpenWeatherMap
   - Calculates aggregate features (max temp, cloud cover, heat waves)
   - Supports batch processing for multiple facilities

3. **Facility Data Loader** (`src/facility_data_loader.py`)
   - Fetches Kenya health facilities from Healthsites.io API
   - Cleans and prepares data for modeling
   - Estimates power sources (grid/solar/diesel/none)

---

## 🚀 Quick Start (Next 30 Minutes)

### Step 1: Install Dependencies (5 minutes)

```bash
cd mvp_cold_chain

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Get OpenWeatherMap API Key (5 minutes)

1. Go to: https://openweathermap.org/api
2. Click "Sign Up" (free)
3. Verify email
4. Go to "API keys" tab
5. Copy your API key

### Step 3: Configure Environment (2 minutes)

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your API key:
# OPENWEATHER_API_KEY=your_actual_api_key_here
```

### Step 4: Test Weather API (5 minutes)

```bash
cd src
python weather_api.py
```

**Expected output:**
```
Fetching 7-day forecast for Nairobi...

Forecast Features:
  max_temp_7d: 28.5
  avg_temp_7d: 24.2
  temp_above_35_days: 0
  heat_wave_indicator: False
  ...
```

### Step 5: Fetch Kenya Facilities (10 minutes)

```bash
python facility_data_loader.py
```

**Expected output:**
```
Fetching facilities from Healthsites.io for Kenya...
  Page 1: 100 facilities
  Page 2: 100 facilities
Total facilities fetched: 200

✓ Saved to ../data/raw/kenya_facilities_healthsites.csv
```

### Step 6: Run Country Ranking Notebook (5 minutes)

```bash
cd ../notebooks
jupyter notebook 00_country_risk_ranking.ipynb
```

Run all cells. You should see:
- Kenya ranks #8-9 in cold chain risk
- Charts showing risk factors
- Justification for Kenya selection

---

## 📋 Next Steps (This Week)

### 1. Data Collection (Today - Tomorrow)

**Goal**: Get 50-100 Kenya facilities with weather forecasts

**Tasks**:
- [x] ✅ Set up weather API
- [x] ✅ Set up facility data loader
- [ ] Create `01_data_collection.ipynb`
- [ ] Fetch facilities for 5 diverse counties (Nairobi, Turkana, Mombasa, Kisumu, Garissa)
- [ ] Fetch 7-day weather forecasts for all facilities
- [ ] Save to `data/processed/facilities_with_weather.csv`

### 2. Add Infrastructure Data (Tomorrow)

**Goal**: Enrich facility data with electrification and population

**Tasks**:
- [ ] Load electrification data (from your High-Res Electrification Dataset)
- [ ] Load population density data
- [ ] Calculate distance to grid for each facility
- [ ] Add features to facility dataset

### 3. Exploratory Data Analysis (Day 3-4)

**Goal**: Understand patterns in Kenya cold chain risk

**Tasks**:
- [ ] Create `02_eda.ipynb`
- [ ] Analyze weather patterns (temperature, solar, seasons)
- [ ] Map facility locations and infrastructure
- [ ] Identify risk factors (heat waves + no power = high risk)
- [ ] Create visualizations

### 4. Feature Engineering (Day 5)

**Goal**: Create model-ready features

**Tasks**:
- [ ] Define target variable (high_risk: Boolean)
- [ ] Create weather features (temp_above_35_days, heat_wave_indicator)
- [ ] Encode facility features (facility_type, power_source)
- [ ] Add temporal features (month, season)
- [ ] Split train/validation/test sets

### 5. Model Training (Week 2)

**Goal**: Build working classification model

**Tasks**:
- [ ] Create `03_model_training.ipynb`
- [ ] Train baseline (always predict "Low Risk")
- [ ] Train Random Forest, XGBoost
- [ ] Tune hyperparameters
- [ ] Evaluate: Precision ≥70%, Recall ≥75%

---

## 🧪 Testing Your Setup

### Test 1: Python Environment

```bash
python -c "import pandas, sklearn, plotly, folium; print('✓ All packages installed')"
```

### Test 2: Weather API

```python
from src.weather_api import WeatherAPI
api = WeatherAPI()
forecast = api.get_forecast_features(-1.2921, 36.8219)  # Nairobi
print("✓ Weather API working" if forecast else "✗ API key issue")
```

### Test 3: Facility Data

```python
from src.facility_data_loader import KenyaFacilityLoader
loader = KenyaFacilityLoader()
facilities = loader.fetch_from_healthsites(country="Kenya", limit=10)
print(f"✓ Fetched {len(facilities)} facilities")
```

### Test 4: Jupyter Notebooks

```bash
jupyter notebook notebooks/00_country_risk_ranking.ipynb
# Run all cells - should complete without errors
```

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Ensure virtual environment is activated and packages installed
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Weather API key not found"
**Solution**: Check .env file exists and contains valid key
```bash
cat .env  # Should show: OPENWEATHER_API_KEY=abc123...
```

### Issue: "No facilities fetched"
**Solution**: Healthsites.io API might be slow or down
- Try again later (API is free and sometimes rate-limited)
- Or manually download Kenya facilities from http://kmhfl.health.go.ke/

### Issue: "Jupyter notebook won't open"
**Solution**:
```bash
pip install --upgrade jupyter
jupyter notebook --generate-config
```

---

## 📊 Current Progress

### Week 1: Data Collection (In Progress)

| Task | Status | Time |
|------|--------|------|
| Project structure | ✅ Done | 30 min |
| Country risk ranking | ✅ Done | 1 hour |
| Weather API setup | ✅ Done | 1 hour |
| Facility data loader | ✅ Done | 1 hour |
| **→ Fetch Kenya facilities** | 🔄 Next | 2 hours |
| **→ Fetch weather forecasts** | ⏳ Pending | 3 hours |
| **→ Add infrastructure data** | ⏳ Pending | 2 hours |

**Total completed: ~3.5 hours / 42 hours (8%)**

---

## 🎓 Learning Resources

### For Understanding the Code

1. **Weather API**:
   - OpenWeatherMap docs: https://openweathermap.org/api/one-call-3
   - Tutorial: How to read weather JSON

2. **Geospatial Data**:
   - GeoPandas intro: https://geopandas.org/getting_started.html
   - Folium maps: https://python-visualization.github.io/folium/

3. **Machine Learning**:
   - Scikit-learn classification: https://scikit-learn.org/stable/supervised_learning.html
   - Imbalanced classification: https://imbalanced-learn.org/

### For Cold Chain Context

1. **WHO Guidelines**:
   - Vaccine storage: https://apps.who.int/iris/handle/10665/183583
   - Temperature monitoring: https://extranet.who.int/prequal/immunization-devices/e006

2. **Research Papers** (see `idea_1_prior_work_analysis.md`):
   - AI for vaccine cold chain
   - Predictive analytics for cold chain management

---

## 🤝 Getting Help

### If You Get Stuck

1. **Check the code comments**: All modules have detailed docstrings
2. **Run test functions**: Each module has `if __name__ == "__main__"` test code
3. **Review example notebooks**: `00_country_risk_ranking.ipynb` shows complete workflow
4. **Check error messages**: Python errors usually point to the exact problem

### Common Questions

**Q: How many facilities do I need?**
A: Minimum 50, target 100-200. More is better for model training.

**Q: How often can I call the weather API?**
A: Free tier = 1000 calls/day. For 100 facilities = 100 calls. Can fetch once per week.

**Q: What if I can't get real incident data?**
A: Use synthetic validation (rule-based failures during heat waves + power outages). Still valid for MVP.

**Q: Do I need GPU for model training?**
A: No. Random Forest and XGBoost run fine on CPU for this dataset size.

---

## ✅ Definition of Done (Week 1)

By end of Week 1, you should have:

- [ ] 50-100 Kenya health facilities with GPS coordinates
- [ ] 7-day weather forecasts for all facilities
- [ ] Electrification and population data added
- [ ] Data saved to `data/processed/facilities_with_weather.csv`
- [ ] EDA notebook started with initial visualizations
- [ ] Risk factors identified (e.g., "heat wave + no power = high risk")

**If you have this, you're on track for MVP success!**

---

## 🎯 Week 2 Preview

Next week we'll build the prediction model:
1. Feature engineering
2. Model training (Random Forest, XGBoost)
3. Hyperparameter tuning
4. Model evaluation
5. Feature importance analysis

**Goal**: 75%+ precision, 80%+ recall on High Risk predictions

---

## 📞 Need More Detail?

- Full documentation: See `README.md`
- MVP plan: See `MVP_plan_cold_chain_prediction.md` (in parent directory)
- Kenya justification: Run `notebooks/00_country_risk_ranking.ipynb`
- Prior work analysis: See `idea_1_prior_work_analysis.md` (in parent directory)

**Ready to start? Run the tests above, then move to Task 1: Fetch Kenya Facilities!**
