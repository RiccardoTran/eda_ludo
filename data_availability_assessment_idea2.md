# Data Availability Assessment for Idea 2: Medical Equipment Energy Model

## Summary: Data Feasibility Score

| Data Category | Coverage | Critical Gaps | Status |
|--------------|----------|---------------|---------|
| **Solar & Climate Data** | 95% | None | ✅ EXCELLENT |
| **Energy Infrastructure** | 75% | Grid reliability details | ✅ GOOD |
| **Geographic/Population** | 80% | None | ✅ GOOD |
| **Health Facility Data** | 10% | Facility locations, equipment inventory | ❌ CRITICAL GAP |
| **Economic Data** | 60% | Diesel prices, facility budgets | ⚠️ PARTIAL |

**Overall Feasibility: 🟡 MODERATE - Viable with Additional Data Sources**

---

## Detailed Dataset Mapping

### ✅ HAVE: Solar & Climate Data (95% Complete)

| Model Input Required | Dataset Available | Quality | Notes |
|---------------------|-------------------|---------|-------|
| Average daily solar irradiation | Global Solar Atlas ✓ | Excellent | Global coverage, downloadable |
| Hourly temperature | Copernicus LST (2010-2021, 5km) ✓ | Excellent | Hourly measurements |
| Temperature (min/max/avg) | NASA POWER API ✓ | Excellent | Global coverage, API access |
| Humidity | NASA POWER API ✓ | Good | Included in meteorological data |
| Precipitation/Rainy season | NASA POWER API ✓ | Good | Can derive rainy season duration |
| Max consecutive cloudy days | Can derive from LST + solar data ✓ | Good | Requires processing |

**Verdict: Climate data is FULLY COVERED and high quality.**

---

### ✅ HAVE: Energy Infrastructure Data (75% Complete)

| Model Input Required | Dataset Available | Quality | Notes |
|---------------------|-------------------|---------|-------|
| Distance to nearest grid line | Africa Energy Tracker ✓ | Good | Transmission lines mapped |
| Grid proximity | All-Africa Energy Model ✓ | Good | Includes grid extension costs |
| Area electrification rate | High-Res Electrification Dataset (Mendeley) ✓ | Excellent | Sub-Saharan Africa gridded data |
| Existing solar/renewable sites | Africa Energy Tracker ✓ | Good | Solar, wind, hydro plants mapped |
| Grid reliability (%) | World Bank Electrification API ⚠️ | Partial | Access rates, but not reliability/uptime |

**Gaps:**
- Grid reliability (hours of power per day) - World Bank has access rates but not daily reliability
- Need to find: National utility reports or household surveys with power outage data

**Verdict: Infrastructure data is GOOD but missing granular reliability metrics.**

---

### ✅ HAVE: Geographic & Population Data (80% Complete)

| Model Input Required | Dataset Available | Quality | Notes |
|---------------------|-------------------|---------|-------|
| Latitude/Longitude | Need health facility database ❌ | N/A | NOT IN YOUR LIST |
| Population density | High-Res Population Density Maps ✓ | Excellent | Continent-wide coverage |
| Regional demographics | Africa in Data ✓ | Good | Life expectancy, GDP, Gini |
| Altitude | Can derive from DEM (not in list) ⚠️ | N/A | Need SRTM or ASTER DEM |

**Gaps:**
- Health facility GPS coordinates - CRITICAL MISSING DATA

**Verdict: Population data excellent, but need facility locations.**

---

### ❌ CRITICAL GAP: Health Facility Data (10% Complete)

| Model Input Required | Dataset Available | Quality | Status |
|---------------------|-------------------|---------|---------|
| Facility locations (lat/lon) | NOT IN YOUR LIST ❌ | N/A | **CRITICAL** |
| Facility type (clinic/center/hospital) | NOT IN YOUR LIST ❌ | N/A | **CRITICAL** |
| Patients per day | NOT IN YOUR LIST ❌ | N/A | Important |
| Operating hours | NOT IN YOUR LIST ❌ | N/A | Important |
| Building size | NOT IN YOUR LIST ❌ | N/A | Nice to have |
| Staff count | NOT IN YOUR LIST ❌ | N/A | Nice to have |

**What you NEED to add:**

#### Essential (Model won't work without):
1. **WHO Global Health Facilities Database**
   - URL: https://apps.who.int/gho/data/node.main.SDGHEALTHFACILITIES
   - Contains: Facility locations, types
   - Coverage: Partial for SSA

2. **Healthsites.io**
   - URL: https://healthsites.io/map
   - Contains: GPS coordinates, facility types
   - Coverage: Good for SSA, crowdsourced

3. **DHS Service Provision Assessment (SPA)**
   - URL: https://dhsprogram.com/methodology/survey-types/spa.cfm
   - Contains: Detailed facility characteristics, equipment inventory
   - Coverage: ~20 countries in SSA

4. **National Health Ministry Data**
   - Country-specific facility master lists
   - Examples: Kenya Master Health Facility List, Nigeria HFR

**Verdict: THIS IS THE BIGGEST GAP. Without facility data, model cannot be trained.**

---

### ❌ CRITICAL GAP: Medical Equipment Data (0% Complete)

| Model Input Required | Dataset Available | Quality | Status |
|---------------------|-------------------|---------|---------|
| Has vaccine refrigerator | NOT IN YOUR LIST ❌ | N/A | **CRITICAL** |
| Has blood bank | NOT IN YOUR LIST ❌ | N/A | **CRITICAL** |
| Has oxygen concentrator | NOT IN YOUR LIST ❌ | N/A | **CRITICAL** |
| Equipment power ratings | NOT IN YOUR LIST ❌ | N/A | Important |
| Current power source | NOT IN YOUR LIST ❌ | N/A | Important |

**What you NEED to add:**

1. **DHS Service Provision Assessment (SPA)**
   - Contains equipment inventory for surveyed facilities
   - Variables: "Has refrigerator for vaccines", "Has oxygen", "Has generator"
   - Data for: Kenya, Tanzania, Nigeria, Malawi, etc.

2. **WHO Service Availability and Readiness Assessment (SARA)**
   - URL: https://www.who.int/data/data-collection-tools/service-availability-and-readiness-assessment-(sara)
   - Equipment inventory included
   - ~30 countries in SSA

3. **Equipment Power Specs (Alternative approach)**
   - If inventory unavailable, use TYPICAL equipment for facility type
   - Rural health center = vaccine fridge + lights + basic equipment
   - District hospital = vaccine fridge + oxygen + blood bank + lights

**Verdict: CRITICAL GAP, but DHS SPA data can fill this for model training.**

---

### ⚠️ PARTIAL: Economic Data (60% Complete)

| Model Input Required | Dataset Available | Quality | Status |
|---------------------|-------------------|---------|---------|
| Regional GDP per capita | World Bank API ✓ | Excellent | Available |
| GDP per capita | Africa in Data ✓ | Good | Available |
| Facility annual budget | NOT IN YOUR LIST ❌ | N/A | Nice to have |
| Diesel price per liter | NOT IN YOUR LIST ❌ | N/A | Important |
| Grid electricity tariff | World Energy Outlook ⚠️ | Partial | Aggregated, not facility-level |

**What you NEED to add:**

1. **Global Petrol Prices**
   - URL: https://www.globalpetrolprices.com/diesel_prices/
   - Contains: Diesel prices by country (updated regularly)

2. **Electricity Tariffs**
   - World Bank RISE (Regulatory Indicators for Sustainable Energy)
   - National utility websites
   - Alternative: Use regional averages ($0.10-0.30/kWh typical for SSA)

3. **Facility Budgets**
   - DHS SPA has some budget data
   - Alternative: Estimate from GDP per capita and facility type

**Verdict: Can work with what you have + simple additions.**

---

## DATA ACQUISITION PRIORITY

### Priority 1: MUST HAVE (Model won't work without)
1. ✅ **Health Facility Locations** - DHS SPA, Healthsites.io, WHO database
2. ✅ **Equipment Inventory** - DHS SPA, WHO SARA

### Priority 2: SHOULD HAVE (Model accuracy depends on)
3. ✅ **Diesel Prices** - Global Petrol Prices database
4. ✅ **Grid Reliability Data** - Find national utility reports or survey data

### Priority 3: NICE TO HAVE (Can estimate if missing)
5. ⚠️ **Facility Budgets** - Can estimate from GDP
6. ⚠️ **Grid Tariffs** - Can use regional averages
7. ⚠️ **Building Characteristics** - Can estimate from facility type

---

## CONCRETE NEXT STEPS

### Step 1: Download DHS Service Provision Assessment (SPA) Data
**This single dataset solves MOST gaps:**
- Facility locations (GPS coordinates)
- Facility types and characteristics
- Equipment inventory (vaccine fridges, oxygen, generators)
- Current power source
- Some budget/cost data

**Countries with recent SPA:**
- Kenya (2021)
- Malawi (2021)
- Tanzania (2021)
- Senegal (2019)
- Nigeria (2022)
- Haiti (2017)
- Afghanistan (2018)

**Download URL:** https://dhsprogram.com/data/available-datasets.cfm
- Create free account
- Request SPA datasets for Sub-Saharan African countries
- Approval takes 1-3 days

### Step 2: Supplement with Healthsites.io
For facilities not in DHS:
- Download OpenStreetMap health facility data
- URL: https://healthsites.io/api/docs/
- Provides lat/lon and basic facility types

### Step 3: Add Diesel Prices
- Scrape or download from https://www.globalpetrolprices.com/diesel_prices/
- Need: Country-level diesel prices (can assume uniform within country)

### Step 4: Find Grid Reliability Data
**Options:**
1. World Bank LSMS (Living Standards Measurement Study) - has household power reliability
2. Afrobarometer surveys - ask about power outages
3. National utility reports (case-by-case)
4. Alternative: Estimate from electrification rate (lower rate = lower reliability)

---

## FEASIBILITY VERDICT

### Can You Build This Model? **YES, but with additional data collection**

**What you have now (from your list):**
- ✅ Excellent climate and solar data (95% complete)
- ✅ Good energy infrastructure mapping (75% complete)
- ✅ Good population and demographics (80% complete)

**What you MUST add:**
- ❌ Health facility locations and characteristics (DHS SPA - free but requires request)
- ❌ Equipment inventory (DHS SPA - included in above)
- ⚠️ Diesel prices (easy to find online)

**Timeline estimate:**
- DHS data request: 1-3 days approval + 1 day download
- Data cleaning and merging: 3-5 days
- Model development: 1-2 weeks

### Recommended Approach

**Option A: Full Model (Ideal)**
- Request DHS SPA data for 5-10 SSA countries
- Combine with your existing climate/infrastructure data
- Build comprehensive model
- **Effort:** 3-4 weeks total
- **Coverage:** 5-10 countries with ground truth data

**Option B: Prototype Model (Faster)**
- Use Healthsites.io for facility locations (available now)
- Assume TYPICAL equipment for each facility type (rural clinic = vaccine fridge + lights)
- Build proof-of-concept model
- **Effort:** 1-2 weeks
- **Coverage:** All SSA, but less accurate on equipment needs

**Option C: Focus on One Country (Most Practical)**
- Pick ONE country with good data availability (e.g., Kenya or Tanzania)
- Get detailed facility data from national health ministry
- Build country-specific model, then generalize
- **Effort:** 2-3 weeks
- **Coverage:** 1 country initially, expandable

---

## MY RECOMMENDATION

🎯 **Start with Option B (Prototype) → Upgrade to Option A (Full Model)**

**Phase 1: Quick Prototype (Week 1-2)**
1. Use Healthsites.io for facility locations (available NOW)
2. Combine with your climate + infrastructure data
3. Assign typical equipment loads by facility type:
   - Rural clinic: 200W continuous (vaccine fridge + lights)
   - Health center: 400W continuous (vaccine + oxygen + lights)
   - District hospital: 1000W continuous (full equipment)
4. Build and test model on synthetic data

**Phase 2: Add Real Data (Week 3-4)**
1. DHS SPA data arrives → replace synthetic equipment data
2. Retrain model with actual facility characteristics
3. Validate predictions against existing solar installations

**Why this approach:**
- ✅ Shows progress immediately (prototype in 2 weeks)
- ✅ Tests if model architecture works before investing in data
- ✅ Identifies additional data needs during prototyping
- ✅ Can present results while waiting for DHS data approval

---

## FINAL ANSWER: IS THIS IDEA WORTH CHASING?

### 🟢 **YES - This idea is VIABLE and IMPACTFUL**

**Strengths:**
- ✅ Climate/solar data is excellent and freely available
- ✅ Infrastructure data is comprehensive
- ✅ Critical gap (facility data) has a clear solution (DHS SPA)
- ✅ High real-world impact (vaccine cold chain, patient lives)
- ✅ Clear validation path (compare to existing installations)

**Challenges:**
- ⚠️ Need to request DHS data (1-3 day wait)
- ⚠️ Data cleaning will be significant work
- ⚠️ Limited to countries with facility data

**Alternative if this seems too hard:**
Consider **Idea 9: Mini-Grid Battery Degradation Prediction** instead:
- Uses ONLY data you already have (climate + infrastructure)
- No facility-level data needed
- Still high impact for renewable energy planning

**But honestly:** Idea 2 is MORE impactful and you have 80% of the data you need. The missing 20% is obtainable for FREE within a week. Worth pursuing.
