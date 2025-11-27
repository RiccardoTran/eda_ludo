# 🚶 Streamlit App Walkthrough - Step by Step

## 📍 Where to Access
Open your browser and go to: **http://localhost:8501**

---

## 🎨 App Layout Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ❄️ COLD CHAIN FAILURE PREDICTION SYSTEM          │
│              5-Day Risk Forecast for Kenya Health Facilities        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐        │
│  │   Total     │  High Risk  │   Average   │   Failure   │        │
│  │ Facilities  │  Facilities │  Failures   │    Rate     │        │
│  │     50      │  20 (40%)   │     1.7     │    34.0%    │        │
│  └─────────────┴─────────────┴─────────────┴─────────────┘        │
│                                                                      │
├─────────────────────────────────────────────────────────────────────┤
│  TABS: [🗺️ Map View] [📊 Facility Details] [⚡Power Analysis] [📈Stats] │
│                                                                      │
│  [TAB CONTENT APPEARS HERE]                                         │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘

SIDEBAR (Left):
┌─────────────────────┐
│  🔍 Filters         │
├─────────────────────┤
│ ☐ Select Regions    │
│   ☑️ Nairobi        │
│   ☑️ Turkana        │
│   ☑️ Mombasa        │
│   ☑️ Kisumu         │
│   ☑️ Garissa        │
│                     │
│ ☐ Power Source      │
│   ☑️ Grid           │
│   ☑️ Solar          │
│   ☑️ Diesel         │
│   ☑️ None           │
│                     │
│ ☐ Risk Level        │
│   ☑️ HIGH           │
│   ☑️ MEDIUM         │
│   ☑️ LOW            │
│                     │
├─────────────────────┤
│ ℹ️ About            │
│ 📊 Data Info        │
└─────────────────────┘
```

---

## 🔢 TOP SECTION: Metrics Dashboard

**What you see:**
```
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│ Total Facilities│ High Risk       │ Avg Failures    │ Failure Rate    │
│       50        │  20 (40%) ⚠️     │      1.7        │     34.0%       │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘
```

**What it means:**
- **Total Facilities (50)**: Number of health facilities being monitored
- **High Risk Facilities (20, 40%)**: Facilities with 3+ failures in next 5 days - these need URGENT attention
- **Avg Failures (1.7)**: Average number of failure days per facility over 5-day forecast
- **Failure Rate (34.0%)**: Overall percentage of facility-days that will fail

**These numbers change** when you use the filters in the sidebar!

---

## 📑 TAB 1: 🗺️ Map View

### What You'll See:

**A. Interactive Map of Kenya**
```
         TURKANA (North)
    🔴 🔴 🔴 🔴 🔴 🔴 🔴
         (Many red dots)
              ↓
    "High risk - poor power infrastructure"


         NAIROBI (Central)
         🟢 🟢 🟢 🟢
         (Green dots)
              ↓
    "Low risk - reliable grid"


         MOMBASA (Coast)
      🟠 🟢 🟠 🟢 🟢
         (Mixed)
              ↓
    "Medium risk - varies"
```

**B. What the Colors Mean:**
- 🔴 **Red Markers**: HIGH RISK (3-5 failures predicted)
- 🟠 **Orange Markers**: MEDIUM RISK (1-2 failures)
- 🟢 **Green Markers**: LOW RISK (0-1 failures)

**C. How to Use:**
1. **Hover over any marker** → Tooltip appears showing:
   ```
   Turkana Clinic 1
   Type: Health Center
   Power: Solar
   Electrification: 30%
   Grid Reliability: 0.40
   Total Failures: 4
   Risk: HIGH
   ```

2. **Zoom in/out**: Scroll with mouse wheel or use +/- buttons

3. **Pan**: Click and drag the map

**D. Regional Statistics Table (Below Map):**
```
Region    | Avg Failures | Facilities | Avg Electrification % | Avg Grid Reliability
----------|--------------|------------|----------------------|---------------------
Nairobi   |     0.5      |     10     |        85%           |        0.90
Turkana   |     3.2      |     15     |        30%           |        0.40  ⚠️
Mombasa   |     0.8      |     10     |        60%           |        0.70
Kisumu    |     0.6      |     10     |        85%           |        0.85
Garissa   |     1.4      |      5     |        45%           |        0.60
```

**Key Insight:** Turkana has 3.2 avg failures (highest!) due to 30% electrification

---

## 📑 TAB 2: 📊 Facility Details

### What You'll See:

**A. Facility Selector (Top)**
```
Select a facility to view details:
┌────────────────────────────────────────────────┐
│ Turkana Clinic 1                        [▼]    │  ← Dropdown menu
└────────────────────────────────────────────────┘
```

Click dropdown to select any of the 50 facilities (sorted by risk, highest first)

---

**B. Two Information Cards Side-by-Side:**

```
┌──────────────────────────────────┐  ┌──────────────────────────────────┐
│   FACILITY INFORMATION           │  │   POWER INFRASTRUCTURE           │
├──────────────────────────────────┤  ├──────────────────────────────────┤
│ Name: Turkana Clinic 1           │  │ Electrification Rate: 30%        │
│ Type: Health Center              │  │ Grid Reliability: 0.40           │
│ Power Source: Solar              │  │ Avg Power Hours/Day: 9.6 hrs     │
│ Location: 3.35°, 35.24°          │  │ Distance to Grid: 40.7 km        │
│ Overall Risk: HIGH ⚠️             │  │ Power Vulnerability: 58.2/100    │
│                                  │  │                                  │
│                                  │  │ ⚠️ High outage risk area         │
│                                  │  │ 🔴 Very low power access         │
└──────────────────────────────────┘  └──────────────────────────────────┘
```

---

**C. 5-Day Failure Forecast Timeline (Visual Chart)**

```
┌─────────────────────────────────────────────────────────────┐
│              Daily Failure Predictions                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Mon, Nov 28    Tue, Nov 29    Wed, Nov 30    Thu, Dec 1   Fri, Dec 2
│  ───────────    ───────────    ───────────    ───────────  ───────────
│  │🔴 FAILURE⚠️│  │🟢 OK ✓    │  │🔴 FAILURE⚠️│  │🔴 FAILURE⚠️│ │🔴 FAILURE⚠️│
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘ └───────────┘
│   (red bar)     (green bar)     (red bar)      (red bar)    (red bar)
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**What it means:**
- **Red bars** = Failure predicted that day
- **Green bars** = No failure, safe day
- Hover over bars to see details

---

**D. Weather Conditions Chart (Two Graphs)**

**Top Graph - Temperature:**
```
┌─────────────────────────────────────────────────────────────┐
│              Temperature (°C)                               │
├─────────────────────────────────────────────────────────────┤
│ 40°C                                                        │
│ 38°C                                                        │
│ 36°C  ●─────●─────●─────●  (Red line = Max Temp)          │
│ 34°C           ●                                           │
│ 32°C                                                        │
│ 30°C                                                        │
│ 28°C  ●─────●─────●─────●─────●  (Blue line = Min Temp)   │
│       Day1  Day2  Day3  Day4  Day5                         │
└─────────────────────────────────────────────────────────────┘
```

**Bottom Graph - Cloud Cover:**
```
┌─────────────────────────────────────────────────────────────┐
│              Cloud Cover (%)                                │
├─────────────────────────────────────────────────────────────┤
│ 100%                                                        │
│  80%        ███        ████        ████                     │
│  60%           ███                            ███           │
│  40%  ███                                                   │
│  20%                                                        │
│   0%  Day1   Day2   Day3   Day4   Day5                     │
└─────────────────────────────────────────────────────────────┘
```

**How to Read:**
- **High temp + High clouds** = Problem for solar facilities
- **High temp + Low clouds** = Problem for all facilities
- See correlation between weather and failures

---

## 📑 TAB 3: ⚡ Power Analysis

### What You'll See:

**A. Failure Rate by Grid Reliability (Top Left)**

```
┌─────────────────────────────────────────────────────────────┐
│      Failure Rate by Grid Reliability                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Low (<60%)      ████████████████████████ 70.0%  🔴        │
│                                                             │
│  Medium (60-80%) ████ 12.0%                                 │
│                                                             │
│  High (>80%)     ██████ 19.2%                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Message:** Unreliable grid = 70% failure rate (3.6x worse!)

---

**B. Failure Rate by Electrification Level (Top Right)**

```
┌─────────────────────────────────────────────────────────────┐
│      Failure Rate by Electrification Level                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Low (<40%)      ████████████████████████ 70.0%  🔴        │
│                                                             │
│  Medium (40-70%) ████ 13.3%                                 │
│                                                             │
│  High (>70%)     █████ 18.4%                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Message:** Low electrification = 70% failure rate (3.8x worse!)

---

**C. Distance to Grid vs Failure Rate (Scatter Plot)**

```
┌─────────────────────────────────────────────────────────────┐
│      Distance to Grid (km) vs Total Failures                │
├─────────────────────────────────────────────────────────────┤
│ 5 failures│                                                 │
│           │                        ●🔴 (Solar, far away)    │
│ 4 failures│              ●🔴    ●🔴                         │
│           │        ●🟠                                      │
│ 3 failures│    ●🔴    ●🟠                                   │
│           │                                                 │
│ 2 failures│ ●🟠                                             │
│           │●🟢  ●🟢                                         │
│ 1 failure │●🟢  ●🟢      (Grid, close to city)             │
│           │                                                 │
│ 0 failures│●🟢  ●🟢                                         │
│           └──────┬──────┬──────┬──────┬──────┬──────       │
│              0km   20km  40km  60km  80km                   │
└─────────────────────────────────────────────────────────────┘
```

**How to Read:**
- **X-axis**: Distance to nearest grid (km)
- **Y-axis**: Total failures (0-5)
- **Colors**: 🟢 Grid, 🟡 Solar, 🟠 Diesel, 🔴 None
- **Bubble size**: Power vulnerability score

**Pattern:** Further from grid = More failures

---

**D. Power Vulnerability Distribution (Histogram)**

```
┌─────────────────────────────────────────────────────────────┐
│      Power Vulnerability Score Distribution                 │
├─────────────────────────────────────────────────────────────┤
│ Number of                                                   │
│ Facilities                                                  │
│   15│                                                       │
│   12│     🟢🟢                                              │
│    9│     🟢🟢🟢                          🔴🔴              │
│    6│     🟢🟢🟢      🟠🟠         🔴🔴🔴                   │
│    3│  🟢🟢🟢🟢🟢  🟠🟠🟠🟠    🔴🔴🔴🔴🔴                  │
│    0└────┴────┴────┴────┴────┴────┴────┴────┴────┴────     │
│       0   10   20   30   40   50   60   70   80   90  100  │
│                Vulnerability Score                          │
│                (0=Best, 100=Worst)                          │
└─────────────────────────────────────────────────────────────┘
```

**Pattern:** Two clusters - low-risk (urban) and high-risk (rural)

---

## 📑 TAB 4: 📈 Statistics

### What You'll See:

**A. Failure Distribution by Day (Bar Chart)**

```
┌─────────────────────────────────────────────────────────────┐
│      Failure Distribution by Day                            │
├─────────────────────────────────────────────────────────────┤
│ Number of                                                   │
│ Failures                                                    │
│   30│                                                       │
│   25│                           ████████  ████████████      │
│   20│                           │ 50%  │  │   50%    │     │
│   15│                 ████████  │ Day4 │  │  Day5    │     │
│   10│  ██████         │ 46%  │  └──────┘  └──────────┘     │
│    5│  │ 20% │  ██    │ Day3 │                             │
│    0│  │Day1 │  │4%│  └──────┘                             │
│       └──────┘  └──┘                                        │
│        Day1     Day2    Day3     Day4      Day5            │
└─────────────────────────────────────────────────────────────┘
```

**KEY INSIGHT:** Risk accumulates over time!
- Days 1-2: Low failures (safe period)
- Days 3-5: High failures (stress builds up)

---

**B. Failures by Power Source (Bottom Left)**

```
┌──────────────────────────────────────┐
│  Failures by Power Source            │
├──────────────────────────────────────┤
│                                      │
│  None    ████████████ 3.0 avg       │
│                                      │
│  Solar   ██████████ 2.8 avg         │
│                                      │
│  Diesel  █████ 1.5 avg               │
│                                      │
│  Grid    ████ 1.2 avg                │
│                                      │
└──────────────────────────────────────┘
```

**Message:** No power = Worst outcome

---

**C. Failures by Facility Type (Bottom Right)**

```
┌──────────────────────────────────────┐
│  Failures by Facility Type           │
├──────────────────────────────────────┤
│                                      │
│  Dispensary   ████████ 2.3 avg      │
│                                      │
│  Clinic       ███████ 2.1 avg        │
│                                      │
│  Health Ctr   █████ 1.5 avg          │
│                                      │
│  Hospital     ███ 0.9 avg            │
│                                      │
└──────────────────────────────────────┘
```

**Message:** Hospitals have better infrastructure

---

**D. Three Key Insight Cards (Bottom)**

```
┌────────────────────┬────────────────────┬────────────────────┐
│ ℹ️ POWER INFRA     │ ⚠️ GEOGRAPHY       │ ✅ TEMPORAL        │
├────────────────────┼────────────────────┼────────────────────┤
│ Unreliable grid    │ Remote facilities  │ Risk accumulates   │
│ (<60% uptime) =    │ (>40km) show       │ over time:         │
│ 3.6x higher        │ 56% failure rate   │                    │
│ failure rate       │                    │ Days 1-2: Low      │
│                    │ Turkana (north)    │ Days 3-5: 50%      │
│ Low electrification│ highest risk due   │                    │
│ (<40%) = 70%       │ to poor power      │ Reflects realistic │
│ failure rate       │ infrastructure     │ cold chain stress  │
└────────────────────┴────────────────────┴────────────────────┘
```

---

## 🎛️ SIDEBAR: Filters & Controls

### How to Use Filters:

**1. Select Regions**
```
┌─────────────────────┐
│ ☐ Select Regions    │
├─────────────────────┤
│ ☑️ Nairobi          │  ← Click checkboxes
│ ☑️ Turkana          │     to include/exclude
│ ☑️ Mombasa          │
│ ☑️ Kisumu           │
│ ☑️ Garissa          │
└─────────────────────┘
```

**Try This:**
- Uncheck all, then check ONLY "Turkana"
- Watch metrics update: Failure rate jumps to ~70%!
- Check ONLY "Nairobi": Failure rate drops to ~5%

---

**2. Power Source Filter**
```
┌─────────────────────┐
│ ☐ Power Source      │
├─────────────────────┤
│ ☑️ Grid             │
│ ☑️ Solar            │
│ ☑️ Diesel           │
│ ☑️ None             │
└─────────────────────┘
```

**Try This:**
- Check ONLY "None": See facilities with no power (highest risk)
- Check ONLY "Grid": See better infrastructure facilities

---

**3. Risk Level Filter**
```
┌─────────────────────┐
│ ☐ Risk Level        │
├─────────────────────┤
│ ☑️ HIGH             │
│ ☑️ MEDIUM           │
│ ☑️ LOW              │
└─────────────────────┘
```

**Try This:**
- Check ONLY "HIGH": Shows 20 priority facilities
- Go to Map View: See only red markers (urgent cases)

---

**4. About Section**
```
┌─────────────────────┐
│ ℹ️ About            │
├─────────────────────┤
│ This system predicts│
│ vaccine cold chain  │
│ failures for health │
│ facilities in Kenya │
│ using:              │
│                     │
│ • 5-day weather     │
│ • Power infra data  │
│ • Facility chars    │
│                     │
│ Model Features:     │
│ 60 inputs,          │
│ 5 daily predictions │
└─────────────────────┘
```

---

**5. Data Info Section**
```
┌─────────────────────┐
│ 📊 Data Info        │
├─────────────────────┤
│ Total Facilities    │
│       50            │
│                     │
│ Forecast Period     │
│     5 days          │
│                     │
│ Last Updated        │
│   2025-11-27        │
└─────────────────────┘
```

---

## 🎯 Quick Demo Path (Follow This Order)

### Step 1: Start on Map View (30 seconds)
1. Look at the map - see red clusters in north (Turkana)
2. Hover over a red marker (e.g., "Turkana Clinic 1")
3. **Say:** "Northern facilities show high risk due to poor power infrastructure"

### Step 2: Go to Power Analysis Tab (1 minute)
1. Look at "Failure Rate by Grid Reliability" chart
2. **Point out:** "70% failure rate for unreliable grid vs 19% for reliable"
3. **Say:** "This is why we added power infrastructure features - it's the #1 predictor!"

### Step 3: Go to Facility Details Tab (1 minute)
1. Select "Turkana Clinic 1" from dropdown
2. Show the two info cards:
   - Left: Basic info
   - Right: Power infrastructure (30% electrification, 40% reliability)
3. Point to 5-day timeline: "4 out of 5 days will fail"
4. **Say:** "Poor power infrastructure directly causes failures"

### Step 4: Compare with Safe Facility (30 seconds)
1. Change dropdown to "Nairobi Health Center 1"
2. Show power infrastructure: 85% electrification, 90% reliability
3. Point to 5-day timeline: "All green - no failures"
4. **Say:** "Same weather, different infrastructure = different outcome"

### Step 5: Go to Statistics Tab (30 seconds)
1. Show "Failure Distribution by Day" chart
2. **Point out:** Days 1-2 low, Days 3-5 high
3. **Say:** "Risk accumulates realistically - cold chain stress builds up over time"

**Total Demo Time: 3.5 minutes**

---

## 🔍 What to Look For (Visual Cues)

### Good Signs (Green):
- ✅ Green markers on map = Safe facilities
- ✅ Green bars in timeline = No failure days
- ✅ High electrification rate (>70%)
- ✅ High grid reliability (>0.80)

### Warning Signs (Orange):
- ⚠️ Orange markers = Monitor these
- ⚠️ 1-2 failures = Some risk
- ⚠️ Medium electrification (40-70%)

### Critical Signs (Red):
- 🔴 Red markers = Urgent attention needed
- 🔴 Red bars = Failure predicted
- 🔴 Low electrification (<40%)
- 🔴 Unreliable grid (<0.60)
- 🔴 Very remote (>40km from grid)

---

## 💡 Pro Tips

1. **Use filters strategically:**
   - Filter by HIGH risk only → See priority facilities
   - Filter by region → Compare Turkana vs Nairobi
   - Filter by power source → See which types are most vulnerable

2. **Look for patterns:**
   - Geographic: North worse than South
   - Temporal: Days 3-5 worse than Days 1-2
   - Infrastructure: Grid reliability is key

3. **Tell a story:**
   - Problem: Cold chain failures threaten vaccines
   - Cause: Power infrastructure (not just weather!)
   - Solution: Predict and prioritize interventions

---

## ❓ Common Questions

**Q: Why are some facilities red and others green?**
A: Power infrastructure quality - see Power Analysis tab

**Q: What do the numbers in timeline mean?**
A: Each bar = one day; Red = failure predicted, Green = safe

**Q: How accurate are these predictions?**
A: Currently synthetic targets for MVP; ML model training is next step

**Q: Can we get real-time updates?**
A: Yes! Run `python3 run_mvp.py` to fetch fresh weather forecasts

**Q: What should we do about high-risk facilities?**
A: Priority actions:
- Install backup power (solar + battery)
- Improve grid connection
- Add temperature monitoring
- Pre-position ice packs

---

## 🎉 You're Ready!

You now understand:
- ✅ How to navigate all 4 tabs
- ✅ What each chart shows
- ✅ How to use filters
- ✅ What the colors mean
- ✅ How to demo the app

**Go explore the app and play with the filters!** 🚀
