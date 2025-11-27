# Idea 2 Expanded: Critical Medical Equipment Energy Reliability Scoring

## Problem Statement
Predict the optimal energy solution for rural health facilities in Sub-Saharan Africa to reliably power critical medical equipment 24/7.

## Critical Questions Addressed

### 1. Why Solar vs. Other Sources?
**Solar isn't always best - it's a cost/feasibility comparison:**
- **Grid extension**: $500-5,000 per household + years of bureaucracy. For facilities >20km from grid, often not viable for 5-10 years
- **Diesel generators**: $0.30-0.80/kWh fuel cost, supply chain issues, high maintenance. Rural clinics can't afford $200-500/month fuel costs
- **Battery storage only**: No generation, just shifts the problem
- **Solar + battery**: $0.05-0.15/kWh after initial investment, 20-year lifespan, minimal maintenance

**The model answers**: "Given this clinic's location, load requirements, and budget - which energy source is most reliable AND affordable?"

### 2. Where Are These Facilities?
**Data sources for facility locations:**
- WHO Global Health Facilities Database
- Healthsites.io (open-source map with GPS coordinates)
- DHS Program (demographic health surveys)
- National health ministries facility master lists

**Typical profile:**
- Rural health centers serving 5,000-50,000 people
- >10km from grid infrastructure
- Located in areas with <50% electrification rate
- Examples: Northern Nigeria, rural Tanzania, South Sudan, DRC, rural Ethiopia

**Filtering criteria:**
- Facilities in areas with <30% electrification
- >20km from nearest transmission line
- Population density 50-500 people/km²

### 3. What Happens at Night?
**Night-time loads for critical equipment:**
- Vaccine refrigerators: 24/7 operation (40-80W continuous)
- Blood refrigerators: 24/7 operation (60-100W continuous)
- Oxygen concentrators: 24/7 availability (120-300W when running)
- Medical lights: Peak evening hours (20-100W)

**Solar + battery sizing must account for:**
- 3-5 days of autonomy (cloudy weather)
- Night-time consumption (8-12 hours of battery power)
- Battery depth of discharge (only use 50-80% capacity)

**Success metric**: System provides 24/7 power for critical loads even during worst-case weather (3 consecutive cloudy days).

### 4. Success Measurement Outcomes

**Primary outcome metric:**
"% of days per year the system delivers minimum required power for critical equipment (24/7)"

**Specific measurable outcomes:**

| Equipment Type | Success Metric | Data to Measure |
|----------------|----------------|-----------------|
| Vaccine refrigerator | 0 cold chain breaks per year (temp stays 2-8°C continuously) | Temperature logs + power availability hours |
| Blood bank | 365 days/year at 2-6°C | Temperature logs |
| Oxygen concentrator | Available within 5 minutes when needed (95% of requests) | Power uptime during clinic hours |
| Medical lights | Functioning during 100% of night-time emergencies | Power availability 6pm-6am |

**Secondary outcomes:**
- Cost per reliable kWh
- Clinic service continuity (% of scheduled days at full capacity)
- Vaccine wastage reduction (doses saved × cost per dose)
- Lives impacted (patients served continuously)

### 5. Validation Variables for Clustering

**Cluster validation:**
```
Cluster 1: "Solar highly viable"
- Solar irradiation >5 kWh/m²/day
- <45 consecutive cloudy days/year
- Temperature 15-35°C most of year

Cluster 2: "Solar viable with larger battery"
- Solar irradiation 4-5 kWh/m²/day
- 45-90 cloudy days/year (rainy season)

Cluster 3: "Solar + diesel hybrid needed"
- Solar irradiation 3-4 kWh/m²/day
- >90 cloudy days/year
- High critical loads

Cluster 4: "Grid/diesel more viable"
- Very cloudy climate (<3 kWh/m²/day)
- OR very close to grid (<5km)
- OR extremely high loads
```

**Validation metrics:**
- Silhouette score >0.5
- Ground truth: Do existing solar installations match "viable" clusters?
- Cost validation: Predicted cost within 20% of actual quotes?
- Reliability validation: Do facilities report <2 failures/year?

---

## MODEL SPECIFICATION

### Input Features

#### 1. Geographic & Location
- Latitude, Longitude
- Country/Region
- Altitude (meters)

#### 2. Solar & Climate
- Average daily solar irradiation (kWh/m²/day)
- Min monthly solar irradiation
- Max consecutive cloudy days per year
- Average daytime temperature (°C)
- Max/Min temperature (°C)
- Rainy season duration (months)
- Humidity (%)

#### 3. Energy Infrastructure
- Distance to nearest grid line (km)
- Grid reliability in area (%)
- Area electrification rate (%)
- Nearest town with fuel supply (km)

#### 4. Facility Characteristics
- Facility type (clinic/health center/dispensary)
- Average patients per day
- Operating hours
- Number of staff
- Building size (m²)

#### 5. Critical Equipment Load Requirements
- Has vaccine refrigerator (Boolean)
- Vaccine fridge power (W)
- Has blood bank refrigerator (Boolean)
- Blood bank power (W)
- Has oxygen concentrator (Boolean)
- Oxygen concentrator power (W)
- Number of lights
- Lighting load (W)
- Other equipment load (W)
- **Total continuous load (W)** - Calculated
- **Peak load (W)** - Calculated
- **Daily energy requirement (kWh/day)** - Calculated

#### 6. Economic Data
- Regional GDP per capita (PPP)
- Facility annual budget (USD)
- Diesel price per liter (USD)
- Grid electricity tariff (USD/kWh)

### Output Predictions

#### 1. Energy Solution Recommendation
**Recommended_Solution**: Categorical
- "Solar Only"
- "Solar + Diesel Backup"
- "Diesel Primary"
- "Grid Connection"
- "Hybrid Solar-Grid"
- "Not Feasible"

#### 2. Solar System Sizing (if applicable)
- **Solar_Panel_Capacity_kW**: Float
- **Battery_Capacity_kWh**: Float
- **Inverter_Size_kW**: Float
- **Backup_Generator_kW**: Float (0 if not needed)

#### 3. Reliability Score
- **Expected_Uptime_Percent**: Float (%)
- **Expected_Coldchain_Breaks_Per_Year**: Float
- **Risk_Level**: Categorical ("Low", "Medium", "High")

#### 4. Cost Analysis
- **Initial_Investment_USD**: Integer
- **Annual_Operating_Cost_USD**: Integer
- **10_Year_Total_Cost_USD**: Integer
- **Cost_Per_kWh_USD**: Float

#### 5. Comparison Metrics
- **Solar_vs_Diesel_Cost_Difference_USD**: Integer
- **Grid_Extension_Cost_USD**: Integer
- **Payback_Period_Years**: Float

#### 6. Interpretation (Secondary)
- **Solar_Viability_Score**: Float (0-1)
- **Critical_Constraints**: List[String]
- **Recommended_Next_Steps**: String

---

## EXAMPLE: Sample Prediction

### Input: Rural Health Center in Tanzania
```python
{
  "latitude": -6.7924,
  "longitude": 39.2083,
  "country": "Tanzania",
  "avg_solar_irradiation_kWh_m2_day": 5.2,
  "min_monthly_solar_irradiation": 3.8,
  "max_consecutive_cloudy_days": 5,
  "distance_to_grid_km": 23.5,
  "grid_reliability_percent": 0,
  "patients_per_day": 85,
  "has_vaccine_fridge": True,
  "vaccine_fridge_W": 60,
  "has_oxygen_concentrator": True,
  "oxygen_concentrator_W": 120,
  "daily_energy_kWh": 3.2
}
```

### Output:
```python
{
  "Recommended_Solution": "Solar + Diesel Backup",
  "Solar_Panel_Capacity_kW": 2.5,
  "Battery_Capacity_kWh": 12.0,
  "Inverter_Size_kW": 1.5,
  "Backup_Generator_kW": 3.0,
  "Expected_Uptime_Percent": 98.5,
  "Expected_Coldchain_Breaks_Per_Year": 0.5,
  "Risk_Level": "Low",
  "Initial_Investment_USD": 8500,
  "Annual_Operating_Cost_USD": 450,
  "10_Year_Total_Cost_USD": 13000,
  "Payback_Period_Years": 3.2,
  "Solar_Viability_Score": 0.85,
  "Recommended_Next_Steps": "Install 2.5kW solar + 12kWh battery. Add 3kW diesel generator for 10-15 days/year backup during cloudy periods."
}
```

---

## MODEL VALIDATION

**Success criteria:**
1. **Cost predictions within 20%** of actual solar installation quotes
2. **Reliability predictions match reality**: Model uptime predictions ±3% of facility logs
3. **Clustering makes sense**: >90% of "Solar Highly Viable" facilities have successful installations
4. **Economic predictions accurate**: Payback period within 1 year of actual

---

## Why This Matters

**Impact:**
- 1 in 4 health facilities in Sub-Saharan Africa lack electricity
- $500 million in vaccines wasted annually due to cold chain failures
- Oxygen, blood storage, and emergency lighting all depend on reliable power
- Wrong energy system sizing = $10k+ failed investments OR preventable patient deaths

**This model prevents:**
- Undersized systems that fail during emergencies
- Oversized systems that waste 30-50% of capital
- Wrong technology choice (solar where diesel is better, or vice versa)
