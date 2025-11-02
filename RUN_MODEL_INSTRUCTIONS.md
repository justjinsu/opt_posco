# Instructions to Run POSCO Optimization Model with Updated NGFS Data

## ✅ What Has Been Updated

### 1. Carbon Price Data
- **File:** `data/v2_sheets/carbon_price.csv`
- **Source:** NGFS Phase V (November 2024), MESSAGEix-GLOBIOM 2.0-M-R12
- **Region:** Other Pacific Asia (Korea, Japan, Australia, New Zealand)
- **Currency:** US$2024 (converted from US$2010 with inflation factor 1.423)
- **Backup:** Original data saved to `data/v2_sheets/carbon_price_OLD_backup.csv`

### 2. New Carbon Price Values (US$2024)

| Scenario | 2025 | 2030 | 2035 | 2040 | 2045 | 2050 |
|----------|------|------|------|------|------|------|
| **Net Zero 2050** | $0 | $383 | $382 | $455 | $536 | $638 |
| **Below 2°C** | $0 | $71 | $77 | $98 | $126 | $166 |
| **NDCs** | $0 | $118 | $121 | $124 | $127 | $130 |

### 3. Paper Updates
- **Abstract:** Updated carbon price values
- **Highlights:** Updated carbon price values
- **Section 3.2.3 (Methodology):** Added regional justification for "Other Pacific Asia"
- **Section 3.3 (Data):** Full explanation of MESSAGEix-GLOBIOM model choice and currency conversion
- **References:** Updated NGFS citation to Phase V

---

## 🚀 How to Run the Model

### Step 1: Verify Python Environment

```bash
cd /Users/jinsupark/jinsu-coding/opt_posco/opt_posco

# Check if virtual environment exists
ls -la .venv/  # or venv/

# Activate if needed
source .venv/bin/activate  # or source venv/bin/activate
```

### Step 2: Install Dependencies (if needed)

```bash
pip install pyomo pandas numpy matplotlib seaborn openpyxl
pip install highspy  # HiGHS solver
```

### Step 3: Run the Optimization

```bash
# Option A: Run all three scenarios
python -m src.run --data data/posco_parameters_consolidated.xlsx --output outputs

# Option B: Run specific scenario
python -m src.run --data data/posco_parameters_consolidated.xlsx \
                  --scenario NGFS_NetZero2050 \
                  --output outputs

# Option C: Run with CCUS sensitivity
python -m src.run --data data/posco_parameters_consolidated.xlsx \
                  --scenario NGFS_NetZero2050 \
                  --ccus-rate 0.0 \
                  --output outputs/noCCUS
```

### Step 4: Check Output Files

Results will be saved to:
```
outputs/
├── series_NGFS_NetZero2050.csv
├── series_NGFS_Below2C.csv
├── series_NGFS_NDCs.csv
├── detailed_results_NGFS_NetZero2050.csv
├── detailed_results_NGFS_Below2C.csv
└── detailed_results_NGFS_NDCs.csv
```

### Step 5: Generate Updated Figures

```bash
# Generate publication-ready figures
python generate_publication_figures.py

# Check outputs in figures/ directory
ls -lh figures/
```

---

## 📋 Post-Model Run Checklist

After running the model, you need to:

### 1. **Verify Results Match Paper Values**

The paper currently states:
- Net Zero 2050: Cumulative emissions = 1,190 MtCO₂ (+7% overshoot)
- Below 2°C: Cumulative emissions = 1,713 MtCO₂ (+54% overshoot)
- NDCs: Cumulative emissions = 1,981 MtCO₂ (+78% overshoot)

**⚠️ WARNING:** These values may change with new NGFS data!

Check `outputs/series_NGFS_NetZero2050.csv` and sum the `emissions_scope1` column for 2025-2050.

### 2. **Update Paper if Results Changed**

If cumulative emissions or technology shares differ significantly, update:
- **Abstract** (lines 56-57)
- **Highlights** (lines 48-49)
- **Section 4 (Results)** - all values
- **Tables** in `tables/` directory
- **Conclusion** (Section 7)

### 3. **Regenerate All Figures**

Figures to update (if results changed):
- `figures/scope1_by_scenario.png`
- `figures/technology_transition.png`
- `figures/production_mix_evolution.png`
- `figures/emissions_pathways.png`
- `figures/ets_cost_by_scenario.png`
- `figures/ets_cost_logic.png`

### 4. **Update Tables**

LaTeX tables in `tables/` directory may need updates:
- `tables/scenario_comparison.tex`
- `tables/annual_technology_shares.tex`
- `tables/cost_abatement.tex`

---

## 🔍 Troubleshooting

### Problem: "Module not found: src"

**Solution:**
```bash
# Make sure you're in the project root
cd /Users/jinsupark/jinsu-coding/opt_posco/opt_posco

# Run as module
python -m src.run [arguments]
```

### Problem: "Solver 'highs' not available"

**Solution:**
```bash
pip install highspy

# Or use GLPK (slower but free)
python -m src.run --solver glpk [other arguments]
```

### Problem: "Parameter loading failed"

**Solution:**
Check that `data/posco_parameters_consolidated.xlsx` exists and contains all required sheets:
- carbon_price
- demand_path
- fuel_prices
- hotmetal_routes
- reduction_routes
- melting_EAF
- etc.

### Problem: Results don't match paper

**Expected!** The new NGFS data has different carbon prices:
- Net Zero: **$383** in 2030 (was $150) - **156% higher!**
- NDCs: **$118** in 2030 (was $40) - **195% higher!**

This will change:
- Technology adoption timing
- Cumulative emissions
- ETS costs
- Budget overshoots

**You MUST re-run the model and update ALL results in the paper!**

---

## 📤 After Model Run: Paper Submission Preparation

Once model completes successfully:

1. ✅ **Check model outputs** are reasonable
2. ✅ **Update all paper values** to match new outputs
3. ✅ **Regenerate all figures**
4. ✅ **Compile LaTeX** and check PDF
5. ✅ **Verify references** are complete
6. ✅ **Check highlights count** (should be 5)
7. ✅ **Proofread abstract** and conclusion
8. ✅ **Compile cover letter**
9. ✅ **Prepare supplementary materials** (code, data)
10. ✅ **Submit to Energy Policy**

---

## 🎯 Summary of Changes for Paper

### What You DON'T Need to Change:
- Model structure and formulation (Section 3.1)
- Technology descriptions (Section 3.2)
- Literature review (Section 2)
- Policy recommendations structure (Section 5.3)

### What You MUST Update (After Model Run):
- All carbon price values (✅ DONE)
- Regional justification (✅ DONE)
- Currency specification (✅ DONE)
- **Results Section 4** - numbers will change
- **Tables** - technology shares, costs, emissions
- **Figures** - all scenario plots
- **Conclusion** - summary statistics

---

## 📝 Quick Reference: Key Files

```
opt_posco/
├── data/
│   ├── ngfs_snapshot_1762055076.csv         # Raw NGFS data
│   ├── NGFS_DATA_NOTES.md                   # Documentation
│   └── v2_sheets/
│       ├── carbon_price.csv                 # ✅ UPDATED
│       ├── carbon_price_OLD_backup.csv      # Backup
│       └── carbon_price_NGFS_PhaseV.csv     # Source file
├── src/
│   ├── run.py                               # Main script
│   ├── scenarios.py                         # Scenario definitions
│   ├── model.py                             # Optimization model
│   └── analysis.py                          # Results analysis
├── main.tex                                 # ✅ UPDATED
└── submission/
    └── cover_letter.tex                     # ✅ UPDATED

```

---

## 🆘 Need Help?

If the model fails or results look wrong, check:
1. Python environment is activated
2. All dependencies installed
3. Data files are readable
4. Solver (HiGHS or GLPK) is available
5. Disk space available for outputs

For model-specific questions, examine:
- `src/model.py` - optimization formulation
- `src/io.py` - data loading logic
- `tests/` - unit tests for validation
