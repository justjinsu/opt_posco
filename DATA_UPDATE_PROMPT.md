# Data Update Instructions for POSCO Steel Decarbonization Model

**Target AI/Assistant**: This prompt guides you to update the POSCO optimization model's input data to align with the academic paper requirements.

---

## OBJECTIVE

Update the input data file `data/posco_parameters_consolidated.xlsx` to ensure the optimization model produces results that match the academic paper's claims and analysis.

---

## CURRENT STATE SUMMARY

### Current Model Results (INCORRECT)
- **POSCO Carbon Budget**: 513 MtCO2 (2025-2050)
- **NZ2050 Cumulative Emissions**: 613.6 MtCO2
- **Below2C Cumulative Emissions**: 651.4 MtCO2
- **NDCs Cumulative Emissions**: 757.3 MtCO2
- **NPV Total Costs**: $183-186 billion

### Target Paper Claims (CORRECT)
- **POSCO Carbon Budget**: 1,110 MtCO2 (2025-2050)
- **NZ2050 Cumulative Emissions**: 1,045 MtCO2
- **Below2C Cumulative Emissions**: 1,290 MtCO2
- **NDCs Cumulative Emissions**: 1,535 MtCO2
- **NPV Total Costs**: $89-100 billion

### Root Cause
The model demand trajectory is too low (35-40 Mt/y) compared to POSCO's actual production scale. The user will provide the correct demand and carbon budget logic.

---

## DATA TO BE UPDATED

The following data will be provided by the user and must be updated in `data/posco_parameters_consolidated.xlsx`:

### 1. **Demand Trajectory (Sheet: `demand_path`)**
**Current Structure:**
```
year  demand_Mt
2025  40.0
2026  39.8
...
2050  35.0
```

**Action Required:**
- Wait for user to provide new demand trajectory
- Update the `demand_Mt` column with user's values
- Ensure years 2025-2050 are all populated

### 2. **Carbon Budget Parameters (Sheet: `industry_targets_anchors`)**
**Current Structure:**
```
parameter                              value
base_year                             2018
base_emissions_national_MtCO2         727.6
steel_sector_share                    0.12
posco_share_of_steel                  0.60
ndc_2030_reduction                    0.40
net_zero_year                         2050
```

**Action Required:**
- Wait for user to provide their carbon budget logic
- Update the parameters according to user's methodology
- May need to add new parameters if user's logic differs

### 3. **Free Allocation Schedule (Sheet: `free_alloc_params`)**
**Action Required:**
- Update to align with carbon budget changes
- Ensure allocation declines consistently with NDC targets
- User may provide specific values or logic

---

## VALIDATION CHECKS REQUIRED

After updating the data, verify:

1. **Demand Consistency**
   - Total demand should reflect POSCO's actual capacity (~60% of Korea's steel sector)
   - Check: Sum of annual demand over 26 years

2. **Carbon Budget Calculation**
   - Verify: POSCO allocation = National emissions × steel_share × posco_share × trajectory
   - Target: ~1,110 MtCO2 cumulative (2025-2050)

3. **Free Allocation Logic**
   - Should decline from high initial values (~95%) to low values by 2050
   - Must align with Korea's NDC (40% by 2030) and net-zero (2050) targets

4. **Data Integrity**
   - No missing years (2025-2050 continuous)
   - No negative values
   - Demand <= realistic capacity bounds
   - Free allocation <= actual emissions in early years

---

## SECONDARY DATA SOURCES TO VALIDATE

If user requests, validate these inputs against external sources:

### Technology Costs (Sheet: `tech_routes`)
- **Source**: IEA Iron and Steel Technology Roadmap 2024
- **Check**: CAPEX for BF-BOF ($1,000/tpy), H2-DRI ($2,500/tpy), CCUS premium
- **Paper Reference**: Lines 333-342 in main.tex

### Carbon Price Scenarios (Sheet: `carbon_price`)
- **Source**: NGFS Climate Scenarios Phase 5 (2024)
- **Check**:
  - NZ2050: Should reach $250/tCO2 by 2050 (currently $450 - TOO HIGH)
  - Below2C: Should reach $185/tCO2 by 2050 (currently $240 - TOO HIGH)
  - NDCs: Should reach $75/tCO2 by 2050 (currently $100 - TOO HIGH)
- **Action**: Scale down carbon prices by factor of ~0.5-0.6
- **Paper Reference**: Lines 293-301 in main.tex

### Hydrogen Costs (Sheet: `fuel_prices`)
- **Source**: IEA Global Hydrogen Review 2024
- **Check**: Baseline $4.50/kg (2030) → $2.80/kg (2050)
- **Paper Reference**: Line 326 in main.tex

### Emission Factors (Sheet: `ef_scope1`)
- **Source**: IEA Steel Technology Roadmap, industry benchmarks
- **Current values appear reasonable**
- BF-BOF: 2.1 tCO2/t (typical range 1.8-2.2)
- H2-DRI: 0.15 tCO2/t (near-zero with grid electricity)

---

## FILE STRUCTURE REFERENCE

The Excel file `data/posco_parameters_consolidated.xlsx` contains these sheets:
1. `tech_routes` - Technology characteristics (CAPEX, capacity)
2. `process_intensity` - Material/energy inputs per ton steel
3. `ef_scope1` - Emission factors by route
4. `fuel_prices` - Commodity price trajectories
5. `grid_CI` - Grid carbon intensity scenarios
6. `carbon_price` - NGFS carbon price scenarios
7. `demand_path` - Steel demand trajectory ← **UPDATE THIS**
8. `free_alloc_params` - ETS free allocation parameters ← **UPDATE THIS**
9. `industry_targets_anchors` - Carbon budget calculation parameters ← **UPDATE THIS**
10. `product_shares` - Product mix assumptions

---

## EXPECTED OUTPUTS AFTER UPDATE

Once data is updated and model is re-run, you should see:

### Optimization Results
- Cumulative emissions closer to 1,000-1,500 MtCO2 range
- Clear differentiation between scenarios
- NDCs scenario overshoots budget by ~38%
- Below2C scenario overshoots by ~16%
- NZ2050 scenario stays within budget

### Cost Results
- Total NPV costs in $80-120B range (not $180B)
- ETS costs should be higher due to higher production
- CAPEX should increase with larger capacity builds

### Technology Transitions
- H2-DRI adoption should occur around 2030-2035 for NZ2050
- BF-BOF should decline from dominant to minor role
- Production mix should show clear scenario differentiation

---

## SPECIFIC UPDATE WORKFLOW

1. **Receive Data from User**
   - Demand trajectory (26 values for 2025-2050)
   - Carbon budget methodology/parameters
   - (Optional) Free allocation schedule

2. **Open Excel File**
   ```python
   import pandas as pd
   import openpyxl

   file_path = 'data/posco_parameters_consolidated.xlsx'
   ```

3. **Update Sheets**
   - Load each sheet as DataFrame
   - Replace relevant values
   - Preserve data structure and formatting
   - Save back to same file

4. **Verify Updates**
   - Re-read file and print key parameters
   - Check for errors or inconsistencies
   - Validate against user's specifications

5. **Document Changes**
   - Create summary of what was changed
   - Note old vs new values for key parameters
   - Explain impact on model results

---

## EXAMPLE UPDATE CODE TEMPLATE

```python
import pandas as pd
import openpyxl

# Load workbook
file_path = 'data/posco_parameters_consolidated.xlsx'

# Update demand
demand_df = pd.read_excel(file_path, 'demand_path')
# Replace demand_Mt column with user's values
new_demand = [...]  # User-provided values
demand_df['demand_Mt'] = new_demand

# Update carbon budget parameters
budget_df = pd.read_excel(file_path, 'industry_targets_anchors')
# Update specific parameter values
budget_df.loc[budget_df['parameter'] == 'base_emissions_national_MtCO2', 'value'] = ...

# Write back to Excel
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    demand_df.to_excel(writer, sheet_name='demand_path', index=False)
    budget_df.to_excel(writer, sheet_name='industry_targets_anchors', index=False)

print("✅ Data updated successfully")
```

---

## QUESTIONS TO ASK USER IF DATA IS UNCLEAR

1. **Demand Trajectory**:
   - Is demand constant, growing, declining, or peaked?
   - What is the peak year and peak value?
   - What is the 2025 starting value?
   - What is the 2050 ending value?

2. **Carbon Budget**:
   - What is Korea's 2018 baseline emissions?
   - What share does steel sector represent?
   - What share does POSCO represent within steel sector?
   - How should emissions decline (linear, exponential, stepwise)?

3. **Free Allocation**:
   - Starting allocation in 2025 (MtCO2/year)?
   - Phase-out schedule (linear, accelerated, stepped)?
   - Final allocation level in 2050?

---

## SUCCESS CRITERIA

The data update is successful when:
- ✅ Model runs without errors
- ✅ Cumulative emissions are in 1,000-1,500 MtCO2 range
- ✅ Carbon budget calculation yields ~1,110 MtCO2 for POSCO
- ✅ Scenario results show clear differentiation
- ✅ Paper's claimed numbers are reproducible from model outputs
- ✅ All validation checks pass

---

## FILES TO MODIFY

**Primary:**
- `data/posco_parameters_consolidated.xlsx` (Excel input file)

**Secondary (if needed):**
- `src/carbon_budget.py` (if calculation logic needs updating)
- `src/io.py` (if new parameters need to be loaded)

---

## NOTES FOR AI ASSISTANT

- User will provide specific numbers - DO NOT estimate or guess
- Preserve Excel file structure and formatting
- Validate all changes before saving
- Create backup of original file before modifying
- Test that model still runs after changes
- Report any inconsistencies or issues to user

---

**WAITING FOR USER INPUT:**
1. Demand trajectory values (2025-2050)
2. Carbon budget calculation methodology
3. (Optional) Free allocation schedule

