# POSCO Model Data Update Guide
## For Research Assistant / Manual Update

---

## 📋 OVERVIEW

This guide helps you update the POSCO steel decarbonization model's input data to match the academic paper requirements. The current model produces results that are too low because the demand trajectory doesn't reflect POSCO's actual production scale.

**Time Required**: 1-2 hours
**Difficulty**: Intermediate (Excel + basic validation)
**Tools Needed**: Microsoft Excel or LibreOffice Calc

---

## 🎯 GOAL

Update the Excel file `data/posco_parameters_consolidated.xlsx` so that when the optimization model runs, it produces:

| **Target Output** | **Value** |
|-------------------|-----------|
| POSCO Carbon Budget (2025-2050) | ~1,110 MtCO2 |
| NZ2050 Scenario Emissions | ~1,045 MtCO2 |
| Below2C Scenario Emissions | ~1,290 MtCO2 |
| NDCs Scenario Emissions | ~1,535 MtCO2 |

**Current Problem**: Model produces only 513 MtCO2 budget and 613-757 MtCO2 emissions (too low by ~50%).

---

## 📂 FILE LOCATION

The file you need to edit:
```
opt_posco/opt_posco/data/posco_parameters_consolidated.xlsx
```

**⚠️ IMPORTANT**: Make a backup copy before editing!
```
Copy the file to: posco_parameters_consolidated_BACKUP.xlsx
```

---

## 📝 STEP-BY-STEP UPDATE PROCESS

### STEP 1: Wait for User's Data

The user (Jinsu) will provide:

#### A. Demand Trajectory
You need 26 values (one for each year 2025-2050).

**Ask Jinsu:**
- "What should POSCO's annual steel production be for each year?"
- "Does it grow, stay constant, or decline?"
- "What are the starting (2025) and ending (2050) values?"

**Expected format:**
```
Year    Demand (Mt/year)
2025    55.0
2026    56.2
2027    57.4
...
2050    48.5
```

#### B. Carbon Budget Logic

The carbon budget determines how much CO2 POSCO is "allowed" to emit.

**Ask Jinsu:**
- "What is Korea's 2018 total emissions baseline?" (Currently: 727.6 MtCO2)
- "What percentage is the steel sector?" (Currently: 12%)
- "What percentage is POSCO within steel?" (Currently: 60%)
- "How should emissions decline to reach 1,110 MtCO2 total?"

**Expected format:**
```
National baseline 2018: XXX MtCO2
Steel sector share: XX%
POSCO share: XX%
2030 target: XX MtCO2/year
2050 target: X MtCO2/year (near zero)
```

#### C. Free Allocation Schedule (Optional)

Free allocation = free CO2 permits given to POSCO under Korea's ETS.

**Ask Jinsu:**
- "What free allocation should POSCO receive in 2025?"
- "How fast should it phase out?"
- "What should it be in 2050?"

---

### STEP 2: Open the Excel File

1. Navigate to: `opt_posco/opt_posco/data/`
2. Open: `posco_parameters_consolidated.xlsx`
3. You'll see 10 sheets (tabs at bottom)

**Sheets you'll edit:**
- ✏️ `demand_path` - Production demand
- ✏️ `industry_targets_anchors` - Carbon budget parameters
- ✏️ `free_alloc_params` - Free allocation schedule
- ⚠️ `carbon_price` - May need adjustment

---

### STEP 3: Update Demand Trajectory

**Sheet: `demand_path`**

**Current structure:**
| year | demand_Mt |
|------|-----------|
| 2025 | 40.0 |
| 2026 | 39.8 |
| ... | ... |
| 2050 | 35.0 |

**What to do:**
1. Click on the `demand_path` sheet tab
2. Find the `demand_Mt` column
3. Replace all values from 2025-2050 with Jinsu's provided values
4. Make sure:
   - All 26 years are filled (no blanks)
   - Values are positive numbers
   - Values are in million tons (Mt)

**Example of what updated values might look like:**
| year | demand_Mt |
|------|-----------|
| 2025 | 55.0 |
| 2026 | 56.5 |
| 2027 | 58.0 |
| 2030 | 60.0 |
| 2035 | 62.0 |
| 2040 | 58.0 |
| 2045 | 52.0 |
| 2050 | 48.0 |

**Validation:**
- Sum of all demand values should be ~1,400-1,500 Mt (total over 26 years)
- Values should reflect realistic production capacity (40-65 Mt/year range)

---

### STEP 4: Update Carbon Budget Parameters

**Sheet: `industry_targets_anchors`**

**Current structure:**
| parameter | value |
|-----------|-------|
| base_year | 2018 |
| base_emissions_national_MtCO2 | 727.6 |
| steel_sector_share | 0.12 |
| posco_share_of_steel | 0.60 |
| ndc_2030_reduction | 0.40 |
| net_zero_year | 2050 |

**What to do:**
1. Click on the `industry_targets_anchors` sheet tab
2. Update each parameter according to Jinsu's carbon budget logic
3. Common changes might be:
   - `base_emissions_national_MtCO2`: Different baseline year or value
   - `steel_sector_share`: Different percentage
   - `posco_share_of_steel`: Different POSCO market share

**Key formula to verify:**
```
POSCO annual baseline =
  base_emissions_national × steel_sector_share × posco_share_of_steel

Example with current values:
  727.6 × 0.12 × 0.60 = 52.4 MtCO2/year
```

**Target**: Parameters should calculate to get ~1,110 MtCO2 cumulative budget for POSCO over 2025-2050.

**How to check:**
The carbon budget is calculated as:
- Start with baseline emissions in 2018
- Decline 40% by 2030 (NDC target)
- Decline to near-zero by 2050
- Sum all annual emissions = cumulative budget

---

### STEP 5: Update Free Allocation Schedule

**Sheet: `free_alloc_params`**

This sheet may have different structures. Common formats:

**Format A: Simple declining schedule**
| year | free_alloc_MtCO2 |
|------|------------------|
| 2025 | 52.0 |
| 2026 | 50.0 |
| ... | ... |
| 2050 | 5.0 |

**Format B: Parameters to calculate allocation**
| parameter | value |
|-----------|-------|
| initial_allocation_2025 | 52.0 |
| decline_rate_annual | 0.05 |
| final_allocation_2050 | 5.0 |

**What to do:**
1. Check which format your file uses
2. If Jinsu provides specific values for each year, enter them
3. If Jinsu provides a decline logic, either:
   - Calculate the values yourself and enter them
   - Update the parameters if using Format B

**Typical declining schedule:**
- Start high: ~90-95% of baseline emissions in 2025
- Linear decline
- End low: ~5-10% of emissions in 2050

**Validation:**
- Free allocation should never exceed actual emissions
- Should decline over time (no increases)
- 2050 value should be much lower than 2025

---

### STEP 6: (Optional) Update Carbon Prices

**Sheet: `carbon_price`**

⚠️ **IMPORTANT FINDING**: Your current carbon prices are too high!

**Current values (2050):**
- NGFS_NetZero2050: $450/tCO2
- NGFS_Below2C: $240/tCO2
- NGFS_NDCs: $100/tCO2

**Paper claims (2050):**
- NGFS_NetZero2050: $250/tCO2 (you have 80% too high!)
- NGFS_Below2C: $185/tCO2 (you have 30% too high!)
- NGFS_NDCs: $75/tCO2 (you have 33% too high!)

**What to do IF Jinsu wants to fix this:**

1. Click on `carbon_price` sheet
2. Find all three scenarios
3. Scale down the prices:
   - NZ2050: Multiply all values by 0.56 (to get from 450→250)
   - Below2C: Multiply all values by 0.77 (to get from 240→185)
   - NDCs: Multiply all values by 0.75 (to get from 100→75)

**Structure:**
| scenario | year | price_USD_per_tCO2 |
|----------|------|--------------------|
| NGFS_NetZero2050 | 2025 | 50 → 28 |
| NGFS_NetZero2050 | 2030 | 150 → 84 |
| ... | ... | ... |
| NGFS_NetZero2050 | 2050 | 450 → 250 |

**Validation:**
- Prices should increase over time (never decrease)
- NZ2050 should be highest, NDCs lowest
- 2030 price for NZ2050 should be ~$130/tCO2 (mentioned in paper)

---

### STEP 7: Save and Validate

**Saving:**
1. Save the file as `posco_parameters_consolidated.xlsx` (same name)
2. Keep your backup copy safe
3. Check that all sheets were saved (Excel sometimes only saves active sheet)

**Quick validation checklist:**

✅ **Demand Sheet**
- [ ] All years 2025-2050 have values
- [ ] No negative numbers
- [ ] Values look reasonable (40-65 Mt/year range)
- [ ] Sum of demand > 1,400 Mt total

✅ **Carbon Budget Parameters**
- [ ] All parameters have values
- [ ] No blanks or errors
- [ ] Parameters make sense (shares between 0-1, years are correct)

✅ **Free Allocation**
- [ ] Values decline over time
- [ ] Starting value is reasonable (40-60 MtCO2/year)
- [ ] Ending value is low (5-15 MtCO2/year)

✅ **Carbon Prices (if updated)**
- [ ] All three scenarios present
- [ ] Prices increase over time
- [ ] 2050 values match paper claims

---

### STEP 8: Document Your Changes

Create a simple log file: `data_update_log.txt`

**Template:**
```
DATA UPDATE LOG
Date: [DATE]
Updated by: [YOUR NAME]

CHANGES MADE:
1. Demand Trajectory
   - Old: 40 Mt (2025) declining to 35 Mt (2050)
   - New: [YOUR NEW VALUES]
   - Reason: Match POSCO actual production scale

2. Carbon Budget Parameters
   - Changed: [LIST PARAMETERS]
   - Old values: [OLD]
   - New values: [NEW]
   - Reason: Achieve 1,110 MtCO2 target budget

3. Free Allocation
   - Changed: [WHAT CHANGED]
   - Reason: [WHY]

4. Carbon Prices (if changed)
   - Scaled down by factors: 0.56, 0.77, 0.75
   - Reason: Match paper's NGFS price claims

VALIDATION:
- File opens without errors: [YES/NO]
- All years 2025-2050 present: [YES/NO]
- No negative values: [YES/NO]
- Demand sum: [VALUE] Mt total

NEXT STEPS:
- Re-run optimization model
- Check if results match paper targets
```

---

## 🔍 HOW TO VERIFY SUCCESS

After updating the data, the model needs to be re-run. Ask the technical team to:

1. **Run all three scenarios:**
```bash
python -m src.run --params data/posco_parameters_consolidated.xlsx \
  --carbon_scenario NGFS_NetZero2050 --solve --outdir outputs

python -m src.run --params data/posco_parameters_consolidated.xlsx \
  --carbon_scenario NGFS_Below2C --solve --outdir outputs

python -m src.run --params data/posco_parameters_consolidated.xlsx \
  --carbon_scenario NGFS_NDCs --solve --outdir outputs
```

2. **Check the results:**
Look at `outputs/summary_NGFS_*.json` files for:
- `cumulative_emissions_MtCO2` should be ~1,045, ~1,290, ~1,535
- Total costs should be ~$89-100B (not $180B+)

3. **Compare to paper claims:**
- If results match ±10%, SUCCESS! ✅
- If still far off, demand trajectory may need further adjustment

---

## ❓ FAQ / TROUBLESHOOTING

### Q: What if the demand values don't sum to the right total?
**A**: Calculate what sum you need (~1,500-1,600 Mt total to get ~1,110 MtCO2 emissions), then scale all demand values proportionally.

### Q: How do I know if carbon budget parameters are right?
**A**: Use this formula:
```
Annual baseline = National × Steel% × POSCO%
Cumulative budget ≈ Baseline × 26 years × 0.5 (due to decline)

Example:
52 MtCO2/year × 26 years × 0.5 = 676 MtCO2
(Too low! Need higher baseline or adjust decline)
```

### Q: What if Excel shows errors after I save?
**A**:
- Check for blank cells (fill with 0 or appropriate value)
- Check for text in number columns
- Make sure year columns are in correct format (2025, not "2025")

### Q: Can I add new rows or columns?
**A**: NO! The model reads specific column names and sheet names. Only change the values in existing cells.

### Q: What if I need to undo changes?
**A**: Use your backup file and start over. That's why we made a backup!

---

## 📞 WHEN TO ASK FOR HELP

Ask Jinsu or technical team if:
1. ❌ You're not sure what values to enter
2. ❌ Excel shows error messages when you try to save
3. ❌ Results after re-running are still far off from targets
4. ❌ You see formula errors (#REF!, #VALUE!, etc.)
5. ❌ Any parameter seems unrealistic or suspicious

---

## 📊 REFERENCE: TARGET NUMBERS

These are the numbers the paper claims (what we're aiming for):

| **Item** | **Target Value** | **Unit** |
|----------|------------------|----------|
| POSCO Carbon Budget | 1,110 | MtCO2 (2025-2050) |
| NZ2050 Emissions | 1,045 | MtCO2 cumulative |
| Below2C Emissions | 1,290 | MtCO2 cumulative |
| NDCs Emissions | 1,535 | MtCO2 cumulative |
| NDCs Overshoot | 38% | Above budget |
| Below2C Overshoot | 16% | Above budget |
| NZ2050 Undershoot | 6% | Below budget |

**Key carbon prices mentioned in paper:**
- 2025: $35/tCO2 (NZ2050)
- 2030: $130/tCO2 (NZ2050) ← Critical threshold
- 2050: $250/tCO2 (NZ2050)

---

## ✅ COMPLETION CHECKLIST

Before you consider the update complete:

- [ ] Received all data from Jinsu (demand, budget logic, allocation)
- [ ] Made backup of original Excel file
- [ ] Updated demand_path sheet with 26 values
- [ ] Updated industry_targets_anchors parameters
- [ ] Updated free_alloc_params schedule
- [ ] (Optional) Adjusted carbon prices if requested
- [ ] Saved file successfully
- [ ] Created data_update_log.txt
- [ ] Verified no Excel errors
- [ ] Checked all validation criteria
- [ ] Notified technical team to re-run model
- [ ] Waiting for results to verify success

---

## 📎 USEFUL FORMULAS

**Check if demand is reasonable:**
```
Average demand = SUM(all demand values) / 26
Should be: 50-60 Mt/year
```

**Check carbon budget calculation:**
```
Rough estimate:
Total demand (Mt) × Average emission factor (2.0 tCO2/t) × Decline factor (0.5)
Should be: ~1,500 Mt × 2.0 × 0.5 = 1,500 MtCO2
```

**Check free allocation logic:**
```
Starting allocation should be ≈ 90% × Baseline emissions
Ending allocation should be ≈ 10% × Future emissions

Example:
Start: 0.90 × 52 = 47 MtCO2/year
End: 0.10 × 20 = 2 MtCO2/year
```

---

**READY TO START?**

1. Wait for Jinsu's data inputs
2. Make your backup
3. Follow steps 1-8
4. Use the checklist
5. Document your changes

Good luck! 🎯
