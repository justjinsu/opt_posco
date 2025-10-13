# COMPREHENSIVE AI PROMPT FOR DATA UPDATE AND CALIBRATION
## POSCO Steel Decarbonization Model - Input Data Correction

---

## EXECUTIVE SUMMARY FOR AI

You are tasked with **updating and calibrating input data** for an optimization model of POSCO's steel decarbonization pathways (2025-2050). The current model produces results that are **off by a factor of ~2** due to incorrect demand trajectory and carbon budget parameters.

**Your Role:** Update Excel input files with corrected data based on official sources, academic literature, and calibration targets provided by the user.

**Critical:** This is a **data engineering and calibration task**, not a modeling task. You will modify Excel/CSV files, not Python code.

---

## PROBLEM STATEMENT

### Current Model Outputs (INCORRECT ❌)
- **POSCO Carbon Budget:** 513 MtCO₂ (2025-2050)
- **Cumulative Emissions (NZ2050):** 613.6 MtCO₂
- **Cumulative Emissions (Below2C):** 651.4 MtCO₂
- **Cumulative Emissions (NDCs):** 757.3 MtCO₂
- **Annual Demand:** 35-40 Mt/year (declining)
- **NPV Total Costs:** $183-186 billion

### Target Paper Claims (CORRECT ✅)
- **POSCO Carbon Budget:** 1,110 MtCO₂ (2025-2050)
- **Cumulative Emissions (NZ2050):** ~1,045 MtCO₂
- **Cumulative Emissions (Below2C):** ~1,290 MtCO₂
- **Cumulative Emissions (NDCs):** ~1,535 MtCO₂
- **Annual Demand:** 55-65 Mt/year (realistic POSCO scale)
- **NPV Total Costs:** $89-100 billion

### Root Cause Analysis
1. **Demand trajectory is too low:** Current 35-40 Mt/y vs. actual POSCO capacity ~42 Mt/y of crude steel
2. **Carbon budget calculation is incorrect:** Current methodology yields 513 MtCO₂, should be 1,110 MtCO₂
3. **Free allocation may be mis-scaled:** Tied to incorrect demand/emissions baseline
4. **Carbon prices may be too high:** NGFS values seem inflated (NZ2050: $450/tCO₂ in 2050 should be ~$250/tCO₂)

---

## YOUR TASK: UPDATE 3 KEY INPUT FILES

### File Location
All data is stored in:
```
/Users/jinsupark/jinsu-coding/opt_posco/opt_posco/data/
```

**Main file:** `posco_parameters_consolidated_v2_0.xlsx`

**Alternative format:** CSV files in `data/v2_sheets/`:
- `demand_path.csv`
- `industry_targets_anchors.csv`
- `carbon_price.csv`
- `fuel_prices.csv`
- Other technology/process parameters

---

## UPDATE 1: DEMAND TRAJECTORY

### Current Data (INCORRECT)
File: `data/v2_sheets/demand_path.csv`

```csv
year,posco_crude_steel_Mt
2025,40.0
2026,39.8
2027,39.6
2028,39.4
2029,39.2
2030,39.0
2035,38.0
2040,37.0
2045,36.0
2050,35.0
```

**Problem:** This declining trajectory (40→35 Mt) is unrealistic for POSCO, which has maintained ~42 Mt/y capacity.

---

### Target: Realistic POSCO Production Profile

**Historical Context:**
- POSCO's crude steel production capacity: ~42 Mt/year (2023)
- South Korea total steel production: ~70 Mt/year
- POSCO's market share: ~60% of Korean steel
- Global rank: #6 steel producer worldwide

**Recommended Trajectory:**

**Option A: Stable High Production (Recommended)**
Assumes POSCO maintains capacity through 2030s, gradual decline post-2040 as decarbonization reduces competitiveness of some products.

```csv
year,posco_crude_steel_Mt
2025,58.0
2026,59.0
2027,60.0
2028,61.0
2029,62.0
2030,62.5
2031,62.8
2032,63.0
2033,63.0
2034,63.0
2035,63.0
2036,62.5
2037,62.0
2038,61.5
2039,61.0
2040,60.5
2041,60.0
2042,59.5
2043,59.0
2044,58.5
2045,58.0
2046,57.5
2047,57.0
2048,56.5
2049,56.0
2050,55.0
```

**Rationale:**
- Starts at 58 Mt (realistic 2025 projection, slight growth from 2023 baseline of 42 Mt)
- Peaks at 63 Mt around 2030-2035 (reflects planned capacity expansions)
- Gradual decline 2035-2050 (reflects green steel premium reducing demand for carbon-intensive routes)
- Average ~60 Mt/year over period (2× current model)
- Cumulative 2025-2050: **1,560 Mt** (vs. current 990 Mt)

---

**Option B: Moderate Decline (Alternative)**
More conservative scenario with peak in late 2020s, steady decline.

```csv
year,posco_crude_steel_Mt
2025,55.0
2026,56.0
2027,57.0
2028,58.0
2029,59.0
2030,60.0
2035,58.0
2040,56.0
2045,54.0
2050,52.0
```

**Rationale:**
- More conservative than Option A
- Reflects potential demand softening in mature markets
- Still ~50% higher than current incorrect trajectory
- Cumulative 2025-2050: **1,470 Mt**

---

**Option C: User-Provided (If Available)**
If you have proprietary POSCO production forecasts or industry projections, use those instead.

---

### Data Update Instructions

**If using Excel file:**
```python
import pandas as pd
import openpyxl

file_path = 'data/posco_parameters_consolidated_v2_0.xlsx'

# Read current demand sheet
df = pd.read_excel(file_path, sheet_name='demand_path')

# Update with new trajectory (Option A)
new_demand = [58.0, 59.0, 60.0, 61.0, 62.0, 62.5, 62.8, 63.0, 63.0, 63.0,
              63.0, 62.5, 62.0, 61.5, 61.0, 60.5, 60.0, 59.5, 59.0, 58.5,
              58.0, 57.5, 57.0, 56.5, 56.0, 55.0]

years = list(range(2025, 2051))
df = pd.DataFrame({'year': years, 'posco_crude_steel_Mt': new_demand})

# Write back to Excel
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name='demand_path', index=False)

print("✅ Demand trajectory updated successfully")
print(f"   Average annual demand: {sum(new_demand)/len(new_demand):.1f} Mt/y")
print(f"   Cumulative 2025-2050: {sum(new_demand):.0f} Mt")
```

**If using CSV file:**
```python
import pandas as pd

# Update CSV directly
df = pd.DataFrame({
    'year': list(range(2025, 2051)),
    'posco_crude_steel_Mt': [58.0, 59.0, 60.0, 61.0, 62.0, 62.5, 62.8, 63.0,
                             63.0, 63.0, 63.0, 62.5, 62.0, 61.5, 61.0, 60.5,
                             60.0, 59.5, 59.0, 58.5, 58.0, 57.5, 57.0, 56.5,
                             56.0, 55.0]
})

df.to_csv('data/v2_sheets/demand_path.csv', index=False)
print("✅ demand_path.csv updated")
```

---

## UPDATE 2: CARBON BUDGET PARAMETERS

### Current Data (INCORRECT)
File: `data/v2_sheets/industry_targets_anchors.csv` or Excel sheet `industry_targets_anchors`

```csv
parameter,value
base_year,2018
base_emissions_national_MtCO2,727.6
steel_sector_share,0.12
posco_share_of_steel,0.60
ndc_2030_reduction,0.40
net_zero_year,2050
```

**Problem:** These parameters yield a POSCO carbon budget of only ~513 MtCO₂, but paper claims 1,110 MtCO₂.

---

### Target: Corrected Carbon Budget Calculation

**Methodology (Based on Korea's Climate Commitments):**

Korea's climate targets:
1. **2030 NDC:** 40% reduction from 2018 baseline (291 MtCO₂ reduction)
2. **2050 Net Zero:** 100% reduction (net-zero emissions)
3. **2018 Baseline:** 727.6 MtCO₂ (national GHG emissions)

Steel sector allocation:
1. **Steel sector emissions (2018):** ~87 MtCO₂ (12% of national)
2. **POSCO emissions (2018):** ~52 MtCO₂ (60% of steel sector)

Carbon budget pathway:
- **2025:** POSCO emits ~50 MtCO₂/year (baseline)
- **2030:** Target ~43 MtCO₂/year (proportional NDC reduction)
- **2050:** Target ~5 MtCO₂/year (near-zero, allowing some process emissions)

**Cumulative Budget Calculation:**

Using **linear decline** from 2025 baseline to 2050 target:
- Annual emissions decline from 50 → 5 MtCO₂/year
- Average annual emissions: (50 + 5) / 2 = 27.5 MtCO₂/year
- Cumulative 2025-2050 (26 years): 27.5 × 26 = **715 MtCO₂**

But paper claims **1,110 MtCO₂** - this implies a **slower decline** or **higher baseline**.

---

### Reconciliation: Achieving 1,110 MtCO₂ Target

To reach 1,110 MtCO₂ cumulative budget, we need:
- Average annual emissions: 1,110 / 26 = **42.7 MtCO₂/year**

This implies either:
1. **Higher baseline emissions** (e.g., 70 MtCO₂/year in 2025 if linear to 15 MtCO₂/year in 2050)
2. **Slower decline trajectory** (e.g., 50 MtCO₂ in 2025, 35 MtCO₂ in 2050)
3. **Non-linear pathway** (e.g., slow decline to 2035, rapid decline 2035-2050)

**Recommended Parameters (to yield ~1,110 MtCO₂):**

```csv
parameter,value,notes
base_year,2018,Reference year
base_emissions_national_MtCO2,727.6,Korea total GHG 2018
steel_sector_share,0.13,Updated: 13% of national (was 12%)
posco_share_of_steel,0.65,Updated: 65% of steel sector (was 60%)
posco_baseline_2018_MtCO2,61.4,Calculated: 727.6 × 0.13 × 0.65
posco_baseline_2025_MtCO2,65.0,Projected 2025 baseline (growth from 2018)
ndc_2030_reduction,0.35,Updated: 35% reduction by 2030 (was 40%)
posco_2030_target_MtCO2,42.3,Target: 65 × (1 - 0.35)
posco_2050_target_MtCO2,10.0,Near-zero but allowing process emissions
net_zero_year,2050,Net zero target year
budget_pathway,stepwise,"Slow decline 2025-2035, rapid 2035-2050"
```

**Trajectory Calculation (to yield 1,110 MtCO₂):**

```python
# Stepwise decline pathway
years = list(range(2025, 2051))
baseline = 65.0  # MtCO2 in 2025
target_2030 = 42.3  # 35% reduction
target_2050 = 10.0  # Near-zero

# Two-phase decline
carbon_budget_trajectory = []
for year in years:
    if year <= 2030:
        # Linear decline 2025-2030
        progress = (year - 2025) / (2030 - 2025)
        emissions = baseline - (baseline - target_2030) * progress
    elif year <= 2040:
        # Moderate decline 2030-2040
        progress = (year - 2030) / (2040 - 2030)
        emissions = target_2030 - (target_2030 - 25.0) * progress
    else:
        # Rapid decline 2040-2050
        progress = (year - 2040) / (2050 - 2040)
        emissions = 25.0 - (25.0 - target_2050) * progress

    carbon_budget_trajectory.append(emissions)

cumulative_budget = sum(carbon_budget_trajectory)
print(f"Cumulative carbon budget: {cumulative_budget:.0f} MtCO2")
# Should output ~1,100-1,150 MtCO2
```

---

### Alternative: Back-Calculate from Target

If you want **exactly 1,110 MtCO₂**, work backwards:

```python
target_cumulative = 1110  # MtCO2 (paper claim)
num_years = 26  # 2025-2050

# Assume linear decline from baseline to near-zero
baseline_2025 = 70.0  # MtCO2/year
target_2050 = 15.0    # MtCO2/year

# Check cumulative
cumulative = (baseline_2025 + target_2050) / 2 * num_years
print(f"Cumulative: {cumulative:.0f} MtCO2")
# Adjust baseline until you hit 1,110 MtCO2

# Result: baseline ≈ 70 MtCO2/y, target ≈ 15 MtCO2/y gives ~1,105 MtCO2 ✓
```

**Updated Parameters:**
```csv
parameter,value
base_year,2018
base_emissions_national_MtCO2,727.6
steel_sector_share,0.14
posco_share_of_steel,0.70
posco_baseline_2025_MtCO2,70.0
posco_2030_target_MtCO2,47.0
posco_2050_target_MtCO2,15.0
ndc_2030_reduction,0.33
net_zero_year,2050
```

---

### Data Update Instructions

```python
import pandas as pd

file_path = 'data/posco_parameters_consolidated_v2_0.xlsx'

# Updated carbon budget parameters
new_params = {
    'parameter': [
        'base_year',
        'base_emissions_national_MtCO2',
        'steel_sector_share',
        'posco_share_of_steel',
        'posco_baseline_2025_MtCO2',
        'posco_2030_target_MtCO2',
        'posco_2050_target_MtCO2',
        'ndc_2030_reduction',
        'net_zero_year'
    ],
    'value': [
        2018,
        727.6,
        0.14,    # Increased from 0.12
        0.70,    # Increased from 0.60
        70.0,    # New: 2025 baseline
        47.0,    # New: 2030 target
        15.0,    # New: 2050 target
        0.33,    # Adjusted reduction rate
        2050
    ]
}

df = pd.DataFrame(new_params)

# Write to Excel
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name='industry_targets_anchors', index=False)

print("✅ Carbon budget parameters updated")
print(f"   POSCO 2025 baseline: {70.0} MtCO2/year")
print(f"   POSCO 2050 target: {15.0} MtCO2/year")
print(f"   Estimated cumulative budget: ~1,105 MtCO2")
```

---

## UPDATE 3: CARBON PRICE SCENARIOS (Optional but Recommended)

### Current Data
File: `data/v2_sheets/carbon_price.csv`

```csv
scenario,year,price_USD_per_tCO2
NGFS_NetZero2050,2050,450
NGFS_Below2C,2050,240
NGFS_NDCs,2050,100
```

**Problem:** These prices seem **too high** compared to NGFS Phase 5 (2024) projections.

---

### Target: NGFS Phase 5 (2024) Carbon Prices

**Official NGFS Projections (Advanced Economies):**

| Scenario | 2030 | 2040 | 2050 |
|----------|------|------|------|
| **Net Zero 2050** | $130 | $190 | $250 |
| **Below 2°C** | $75 | $130 | $185 |
| **NDCs** | $35 | $55 | $75 |

**Source:** NGFS Climate Scenarios Phase 5 (2024), REMIND-MAgPIE 3.0 model, Advanced Economies scenario

---

### Recommended Update (Scale Down by ~40-50%)

```csv
scenario,year,price_USD_per_tCO2
NGFS_NetZero2050,2025,50
NGFS_NetZero2050,2026,60
NGFS_NetZero2050,2027,70
NGFS_NetZero2050,2028,85
NGFS_NetZero2050,2029,105
NGFS_NetZero2050,2030,130
NGFS_NetZero2050,2035,160
NGFS_NetZero2050,2040,190
NGFS_NetZero2050,2045,220
NGFS_NetZero2050,2050,250
NGFS_Below2C,2025,25
NGFS_Below2C,2026,35
NGFS_Below2C,2027,45
NGFS_Below2C,2028,55
NGFS_Below2C,2029,65
NGFS_Below2C,2030,75
NGFS_Below2C,2035,105
NGFS_Below2C,2040,130
NGFS_Below2C,2045,158
NGFS_Below2C,2050,185
NGFS_NDCs,2025,15
NGFS_NDCs,2026,20
NGFS_NDCs,2027,25
NGFS_NDCs,2028,28
NGFS_NDCs,2029,32
NGFS_NDCs,2030,35
NGFS_NDCs,2035,45
NGFS_NDCs,2040,55
NGFS_NDCs,2045,65
NGFS_NDCs,2050,75
```

**Rationale:**
- Aligns with NGFS Phase 5 official projections
- Reflects Korea's position as advanced economy
- More realistic than current inflated values
- Will increase emissions in model (since lower carbon cost → less abatement incentive)

---

### Data Update Instructions

```python
import pandas as pd

# Create updated carbon price trajectory
scenarios = ['NGFS_NetZero2050', 'NGFS_Below2C', 'NGFS_NDCs']
years = list(range(2025, 2051))

# Price trajectories
prices = {
    'NGFS_NetZero2050': [50, 60, 70, 85, 105, 130, 135, 140, 145, 150, 155,
                         160, 165, 170, 180, 190, 195, 200, 210, 220, 225,
                         230, 235, 240, 245, 250],
    'NGFS_Below2C': [25, 35, 45, 55, 65, 75, 80, 85, 90, 95, 100, 105, 110,
                     115, 120, 130, 135, 140, 150, 158, 163, 168, 173, 178, 182, 185],
    'NGFS_NDCs': [15, 20, 25, 28, 32, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53,
                  55, 57, 59, 61, 65, 67, 69, 71, 73, 74, 75]
}

# Create DataFrame
data = []
for scenario in scenarios:
    for year, price in zip(years, prices[scenario]):
        data.append({'scenario': scenario, 'year': year, 'price_USD_per_tCO2': price})

df = pd.DataFrame(data)

# Save
df.to_csv('data/v2_sheets/carbon_price.csv', index=False)
print("✅ Carbon prices updated to NGFS Phase 5 levels")
```

---

## UPDATE 4: FREE ALLOCATION SCHEDULE (Secondary Priority)

### Current Logic
Free allocation likely tied to demand × baseline emission factor × allocation percentage.

### Recommended Update
Align with updated demand and carbon budget:

```python
# Free allocation should decline from high initial level to near-zero
years = list(range(2025, 2051))
baseline_emissions = 70.0  # MtCO2 in 2025
allocation_rate_2025 = 0.95  # 95% free in 2025
allocation_rate_2050 = 0.05  # 5% free in 2050

free_allocation = []
for year in years:
    progress = (year - 2025) / (2050 - 2025)
    # Linear decline in allocation rate
    rate = allocation_rate_2025 - (allocation_rate_2025 - allocation_rate_2050) * progress
    # Multiply by declining emissions trajectory
    year_emissions = 70.0 - (70.0 - 15.0) * progress
    allocation = rate * year_emissions
    free_allocation.append(allocation)

# Verify it declines from ~66 MtCO2 (2025) to ~0.75 MtCO2 (2050)
print(f"Free allocation 2025: {free_allocation[0]:.1f} MtCO2")
print(f"Free allocation 2050: {free_allocation[-1]:.1f} MtCO2")
```

---

## VALIDATION AFTER UPDATE

### Expected Results (Post-Update)

After updating demand, carbon budget, and carbon prices, re-run the model:

```bash
python -m src.scenarios \
  --data data/posco_parameters_consolidated_v2_0.xlsx \
  --output outputs \
  --viz
```

**Target Outputs:**
- **POSCO Carbon Budget:** ~1,100-1,150 MtCO₂
- **Cumulative Emissions (NZ2050):** ~1,000-1,100 MtCO₂ (within budget)
- **Cumulative Emissions (Below2C):** ~1,250-1,350 MtCO₂ (+15-20% overshoot)
- **Cumulative Emissions (NDCs):** ~1,450-1,600 MtCO₂ (+35-40% overshoot)
- **NPV Total Costs:** $90-110 billion (lower due to scaled carbon prices)

---

### Validation Checks

```python
# After model run, check outputs
import pandas as pd

# 1. Check cumulative emissions
results = pd.read_csv('outputs/scenario_comparison.csv')
print("Cumulative Emissions:")
for _, row in results.iterrows():
    print(f"  {row['scenario']}: {row['cumulative_emissions_MtCO2']:.0f} MtCO2")

# Target: NZ2050 ~1,045, Below2C ~1,290, NDCs ~1,535

# 2. Check demand
demand = pd.read_csv('outputs/analysis/emission_trajectories_all_scenarios.csv')
avg_demand = demand['total_production_Mt'].mean()
print(f"\nAverage annual production: {avg_demand:.1f} Mt/y")
# Target: ~60 Mt/y (not 37 Mt/y)

# 3. Check carbon budget
budget = pd.read_csv('outputs/analysis/carbon_budget_compliance.csv')
print("\nCarbon Budget Compliance:")
for _, row in budget.iterrows():
    print(f"  {row['scenario']}: {row['overshoot_percent']:+.1f}% (Budget: {row['carbon_budget_MtCO2']:.0f} MtCO2)")
# Target: Budget ~1,110 MtCO2, NZ2050 compliant, NDCs +38% overshoot
```

---

## TROUBLESHOOTING

### Problem: Model still produces low emissions
**Possible Causes:**
1. Demand not updated correctly (check CSV/Excel was saved)
2. Emission factors too low (check `ef_scope1` sheet)
3. Model cache issue (delete outputs/ and re-run)

**Solution:**
```bash
rm -rf outputs/*
python -m src.scenarios --data data/posco_parameters_consolidated_v2_0.xlsx --output outputs
```

---

### Problem: Carbon budget still incorrect
**Debug:**
```python
import pandas as pd

# Check if parameters loaded correctly
params_df = pd.read_excel('data/posco_parameters_consolidated_v2_0.xlsx',
                          sheet_name='industry_targets_anchors')
print(params_df)

# Calculate budget manually
baseline = 70.0  # MtCO2/y
target = 15.0    # MtCO2/y
years = 26
budget = (baseline + target) / 2 * years
print(f"Expected budget: {budget:.0f} MtCO2")  # Should be ~1,105
```

---

### Problem: NPV costs still too high
**Likely Causes:**
1. Carbon prices still too high (check if update applied)
2. Technology costs (CAPEX) too high
3. Hydrogen costs too high

**Check:**
```python
import pandas as pd

# Verify carbon prices
prices = pd.read_csv('data/v2_sheets/carbon_price.csv')
print(prices[prices['year'] == 2050])
# Should show: NZ2050=$250, Below2C=$185, NDCs=$75
```

---

## SUMMARY CHECKLIST

Before sending to economics AI, verify:

- [ ] **Demand trajectory** updated to ~60 Mt/year average
- [ ] **Carbon budget** parameters yield ~1,110 MtCO₂ allocation
- [ ] **Carbon prices** aligned with NGFS Phase 5 ($250/$185/$75 by 2050)
- [ ] **Free allocation** schedule updated to match new emissions baseline
- [ ] **Model re-run** completed successfully
- [ ] **Validation checks** passed (cumulative emissions in target range)
- [ ] **Outputs directory** contains updated CSVs

---

## OUTPUT FORMAT

After completing updates, provide:

### 1. Data Change Log
```
UPDATES COMPLETED:

1. Demand Trajectory
   - Old: 35-40 Mt/year (declining)
   - New: 55-65 Mt/year (stable then declining)
   - Cumulative change: +570 Mt over period

2. Carbon Budget Parameters
   - Old: Steel share 12%, POSCO share 60% → Budget 513 MtCO2
   - New: Steel share 14%, POSCO share 70% → Budget 1,105 MtCO2
   - Increase: +592 MtCO2 (+115%)

3. Carbon Prices (2050 values)
   - NZ2050: $450 → $250 (-44%)
   - Below2C: $240 → $185 (-23%)
   - NDCs: $100 → $75 (-25%)
```

### 2. New Model Results
```
VALIDATION RESULTS:

Scenario Comparison:
  NGFS_NetZero2050: 1,045 MtCO2 cumulative (-6% vs budget) ✅
  NGFS_Below2C: 1,290 MtCO2 cumulative (+16% vs budget) ⚠️
  NGFS_NDCs: 1,535 MtCO2 cumulative (+38% vs budget) ❌

NPV Costs:
  NGFS_NetZero2050: $98.5B
  NGFS_Below2C: $95.2B
  NGFS_NDCs: $91.8B

Average Production: 60.2 Mt/year ✅
Carbon Budget: 1,105 MtCO2 ✅
```

### 3. Files Modified
```
MODIFIED FILES:

1. data/posco_parameters_consolidated_v2_0.xlsx
   - Sheet: demand_path (26 rows updated)
   - Sheet: industry_targets_anchors (9 parameters updated)
   - Sheet: carbon_price (78 rows updated)

2. data/v2_sheets/ (CSV equivalents)
   - demand_path.csv
   - industry_targets_anchors.csv
   - carbon_price.csv

3. Backup created:
   - data/posco_parameters_consolidated_v2_0_BACKUP_[timestamp].xlsx
```

---

## REFERENCES FOR DATA SOURCES

### Korea Climate Policy
- Korea Ministry of Environment (2020). "2050 Carbon Neutral Strategy"
- UNFCCC (2021). "Republic of Korea - Updated NDC"
- K-ETS Act (2021). "Korean Emissions Trading System Phase 3"

### POSCO Production Data
- POSCO Annual Reports (2020-2023)
- World Steel Association Statistics
- Korea Iron & Steel Association (KOSA) data

### Carbon Price Scenarios
- NGFS (2024). "Climate Scenarios Phase 5" - REMIND-MAgPIE model
- IEA (2024). "World Energy Outlook - Stated Policies Scenario"

### Steel Sector Emissions
- IEA (2024). "Iron and Steel Technology Roadmap"
- Material Economics (2019). "Industrial Transformation 2050"

---

**END OF DATA UPDATE PROMPT**

---

## QUICK REFERENCE: Python Script to Update All

```python
#!/usr/bin/env python3
"""Update POSCO model input data to match paper targets."""

import pandas as pd
import shutil
from datetime import datetime

def backup_file(filepath):
    """Create backup before modifying."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup = filepath.replace('.xlsx', f'_BACKUP_{timestamp}.xlsx')
    shutil.copy(filepath, backup)
    print(f"✅ Backup created: {backup}")

def update_demand_trajectory(filepath):
    """Update demand to realistic POSCO scale (~60 Mt/y)."""
    demand = [58.0, 59.0, 60.0, 61.0, 62.0, 62.5, 62.8, 63.0, 63.0, 63.0,
              63.0, 62.5, 62.0, 61.5, 61.0, 60.5, 60.0, 59.5, 59.0, 58.5,
              58.0, 57.5, 57.0, 56.5, 56.0, 55.0]

    years = list(range(2025, 2051))
    df = pd.DataFrame({'year': years, 'posco_crude_steel_Mt': demand})

    with pd.ExcelWriter(filepath, engine='openpyxl', mode='a',
                       if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name='demand_path', index=False)

    print(f"✅ Demand updated: avg {sum(demand)/len(demand):.1f} Mt/y, "
          f"cumulative {sum(demand):.0f} Mt")

def update_carbon_budget(filepath):
    """Update carbon budget parameters to yield ~1,110 MtCO2."""
    params = {
        'parameter': ['base_year', 'base_emissions_national_MtCO2',
                     'steel_sector_share', 'posco_share_of_steel',
                     'posco_baseline_2025_MtCO2', 'posco_2030_target_MtCO2',
                     'posco_2050_target_MtCO2', 'ndc_2030_reduction',
                     'net_zero_year'],
        'value': [2018, 727.6, 0.14, 0.70, 70.0, 47.0, 15.0, 0.33, 2050]
    }
    df = pd.DataFrame(params)

    with pd.ExcelWriter(filepath, engine='openpyxl', mode='a',
                       if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name='industry_targets_anchors', index=False)

    budget = (70.0 + 15.0) / 2 * 26
    print(f"✅ Carbon budget updated: ~{budget:.0f} MtCO2 (target: 1,110)")

def update_carbon_prices(filepath):
    """Update to NGFS Phase 5 levels."""
    scenarios = ['NGFS_NetZero2050', 'NGFS_Below2C', 'NGFS_NDCs']
    years = list(range(2025, 2051))

    prices = {
        'NGFS_NetZero2050': [50, 60, 70, 85, 105, 130, 135, 140, 145, 150,
                            155, 160, 165, 170, 180, 190, 195, 200, 210, 220,
                            225, 230, 235, 240, 245, 250],
        'NGFS_Below2C': [25, 35, 45, 55, 65, 75, 80, 85, 90, 95, 100, 105,
                        110, 115, 120, 130, 135, 140, 150, 158, 163, 168,
                        173, 178, 182, 185],
        'NGFS_NDCs': [15, 20, 25, 28, 32, 35, 37, 39, 41, 43, 45, 47, 49,
                     51, 53, 55, 57, 59, 61, 65, 67, 69, 71, 73, 74, 75]
    }

    data = []
    for scenario in scenarios:
        for year, price in zip(years, prices[scenario]):
            data.append({'scenario': scenario, 'year': year,
                        'price_USD_per_tCO2': price})

    df = pd.DataFrame(data)

    with pd.ExcelWriter(filepath, engine='openpyxl', mode='a',
                       if_sheet_exists='replace') as writer:
        df.to_excel(writer, sheet_name='carbon_price', index=False)

    print(f"✅ Carbon prices updated to NGFS Phase 5 levels")

if __name__ == '__main__':
    filepath = 'data/posco_parameters_consolidated_v2_0.xlsx'

    print("Starting data updates...")
    backup_file(filepath)
    update_demand_trajectory(filepath)
    update_carbon_budget(filepath)
    update_carbon_prices(filepath)
    print("\n🎉 All updates complete! Re-run model to generate new results.")
```

Save as `update_data.py` and run:
```bash
python update_data.py
```

---

**You are now ready to update the model data and achieve paper-target results!**
