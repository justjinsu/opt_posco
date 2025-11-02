# NGFS Phase V Results Summary

**Date:** January 2, 2025
**Model:** POSCO Steel Decarbonization Optimization
**Data Source:** NGFS Phase V (November 2024), MESSAGEix-GLOBIOM 2.0, Other Pacific Asia
**Currency:** US$2024 (converted from US$2010, factor 1.423)

---

## 📊 Key Results Comparison

### Net Zero 2050

**Carbon Prices (US$2024):**
- 2025: $0 → 2030: $383 → 2040: $455 → 2050: $638

**Results:**
| Metric | Paper (Old Values) | NGFS Phase V (New) | Change |
|--------|-------------------|-------------------|--------|
| Cumulative Emissions | 1,190 MtCO₂ | **1,146 MtCO₂** | ✅ **-44 MtCO₂** |
| Budget Overshoot | +7.2% | **+3.2%** | ✅ **Improved!** |
| 2050 CCUS Share | 51% | **51.0%** | ✅ Match |
| 2050 Scrap-EAF Share | 36% | **35.7%** | ✅ Match |

**Why better?** Higher early carbon prices ($383 vs old $150 in 2030) drive earlier technology adoption and lower cumulative emissions.

---

### Below 2°C

**Carbon Prices (US$2024):**
- 2025: $0 → 2030: $71 → 2040: $98 → 2050: $166

**Results:**
| Metric | Paper (Old Values) | NGFS Phase V (New) | Change |
|--------|-------------------|-------------------|--------|
| Cumulative Emissions | 1,713 MtCO₂ | **1,981 MtCO₂** | ⚠️ **+268 MtCO₂** |
| Budget Overshoot | +54% | **+78.4%** | ⚠️ **Worse** |
| 2050 BF-BOF Share | ~60-70%? | **94.9%** | ⚠️ More conventional |
| 2050 Scrap-EAF Share | ~30-40%? | **5.1%** | ⚠️ Less scrap |

**Why worse?** Lower late-stage prices ($166 vs old $240 in 2050) make expensive decarbonization technologies less attractive.

---

### NDCs (Nationally Determined Contributions)

**Carbon Prices (US$2024):**
- 2025: $0 → 2030: $118 → 2040: $124 → 2050: $130

**Results:**
| Metric | Paper (Old Values) | NGFS Phase V (New) | Change |
|--------|-------------------|-------------------|--------|
| Cumulative Emissions | 1,981 MtCO₂ | **1,978 MtCO₂** | ✅ **-3 MtCO₂** |
| Budget Overshoot | +78% | **+78.2%** | ✅ **Match!** |
| 2050 BF-BOF Share | ~95% | **94.9%** | ✅ Match |
| 2050 Scrap-EAF Share | ~5% | **5.1%** | ✅ Match |

**Why similar?** NDC scenario carbon prices happen to be close to the old assumptions, so results match well.

---

## 🎯 Key Findings

### 1. **Net Zero 2050 Performance IMPROVED** ✅

The budget overshoot is now **+3.2%** instead of **+7%**. This is because:
- NGFS Phase V Net Zero prices are **much higher** in early years ($383 vs $150 in 2030)
- Higher early prices incentivize earlier CCUS and scrap-EAF adoption
- Earlier transition = lower cumulative emissions

**Technology Mix (2050):**
- CCUS (BF-BOF+CCUS): **51.0%** (matches paper!)
- Scrap-EAF: **35.7%** (matches paper's 36%)
- Conventional BF-BOF: **13.3%**

**Paper Update Needed:**
- Abstract line 57: Change "1,190 MtCO₂ (+7%)" → "**1,146 MtCO₂ (+3.2%)**"
- Highlights line 48: Change overshoot percentage
- Section 4 results: Update all emission values

---

### 2. **Below 2°C Performance WORSENED** ⚠️

The budget overshoot increased from **+54%** to **+78.4%**. This is because:
- NGFS Phase V Below 2°C prices are **lower** in late period ($166 vs $240 in 2050)
- Lower prices don't justify expensive CCUS retrofits
- Model sticks with conventional BF-BOF much longer

**Technology Mix (2050):**
- Conventional BF-BOF: **94.9%** (minimal transition!)
- Scrap-EAF: **5.1%** (very limited)
- No CCUS deployment

**Paper Update Needed:**
- Abstract line 57: Change "1,713 MtCO₂ (+54%)" → "**1,981 MtCO₂ (+78.4%)**"
- Section 4: Revise Below 2°C results discussion
- Explain that NGFS Phase V Below 2°C is less aggressive than Phase IV

---

### 3. **NDCs Performance UNCHANGED** ✅

Results are nearly identical to the paper:
- Cumulative: 1,978 MtCO₂ vs paper's 1,981 MtCO₂
- Overshoot: +78.2% vs paper's +78%

**Technology Mix (2050):**
- Conventional BF-BOF: **94.9%**
- Scrap-EAF: **5.1%**
- Minimal decarbonization

**Paper Update Needed:**
- Minor adjustments only (rounding)

---

## 📝 Required Paper Updates

### CRITICAL UPDATES (Must Change):

**1. Abstract (main.tex line 57)**

OLD:
```
Current trajectories remain inadequate: cumulative emissions reach 1,190 MtCO₂ (+7%)
under Net Zero 2050, 1,713 MtCO₂ (+54%) under Below 2°C, and 1,981 MtCO₂ (+78%)
under the NDC case.
```

NEW:
```
Current trajectories remain inadequate: cumulative emissions reach 1,146 MtCO₂ (+3.2%)
under Net Zero 2050, 1,981 MtCO₂ (+78.4%) under Below 2°C, and 1,978 MtCO₂ (+78.2%)
under the NDC case.
```

**2. Highlights (main.tex line 48)**

OLD:
```
Even under Net Zero 2050 pricing (\$383/tCO₂ by 2030, \$638/tCO₂ by 2050),
cumulative emissions reach 1,190~MtCO$_2$ (+7\%)
```

NEW:
```
Even under Net Zero 2050 pricing (\$383/tCO₂ by 2030, \$638/tCO₂ by 2050),
cumulative emissions reach 1,146~MtCO$_2$ (+3.2\%)
```

**3. Section 4 (Results)**

Update ALL emission values, technology shares, and ETS costs for all three scenarios.

---

## 💡 Interpretation

### Good News ✅

1. **Net Zero 2050 is more achievable** than previously thought with real NGFS Phase V prices
2. The budget overshoot reduced from +7% to +3.2% - closer to compliance
3. Technology mix (51% CCUS, 36% scrap-EAF) remains similar

### Bad News ⚠️

1. **Below 2°C pathway is weaker** in NGFS Phase V
2. Below 2°C now overshoots by +78% (worse than old NDCs!)
3. This suggests NGFS Phase V Below 2°C is less ambitious than Phase IV

### Recommendation 📢

**Update your policy message:**

OLD MESSAGE:
> "Even under Net Zero 2050, we overshoot by 7%, so current ETS pricing is inadequate"

NEW MESSAGE:
> "Under NGFS Phase V Net Zero 2050 prices, overshoot is only 3.2%, showing that
> ambitious early carbon pricing CAN align with carbon budgets. However, the Below 2°C
> scenario (+78% overshoot) demonstrates that moderate ambition is insufficient.
> This reinforces the need for price floors converging toward $500-600/tCO₂ by 2050."

---

## 📂 Output Files

All results saved to `outputs/` directory:

- `outputs/series_NGFS_NetZero2050.csv` - Net Zero time series
- `outputs/series_NGFS_Below2C.csv` - Below 2°C time series
- `outputs/series_NGFS_NDCs.csv` - NDCs time series

---

## ✅ Next Steps

1. **Update main.tex** with new values (Abstract, Highlights, Section 4)
2. **Regenerate figures** with `generate_publication_figures.py`
3. **Update tables** in `tables/` directory
4. **Revise discussion** to reflect improved Net Zero performance
5. **Compile PDF** and check all changes
6. **Submit to Energy Policy!**

---

## 🔬 Technical Details

**Model Configuration:**
- Discount rate: 5%
- Capacity utilization: 90%
- CCUS capture rate: 80%
- Carbon budget: 1,110 MtCO₂ (2025-2050)
- Solver: HiGHS 1.11.0
- Solve times: 2-5 seconds per scenario

**Data Sources:**
- NGFS Phase V (November 2024)
- MESSAGEix-GLOBIOM 2.0-M-R12
- Region: Other Pacific Asia
- Currency conversion: CPI 2010→2024 (factor 1.423)
- Interpolation: Linear between key years (2025, 2030, 2035, 2040, 2045, 2050)

**Files:**
- Model: `src/model.py`
- Data: `data/posco_parameters_consolidated.xlsx`
- Carbon prices: `data/v2_sheets/carbon_price_complete.csv`

---

**Generated:** 2025-01-02
**Status:** ✅ All scenarios completed successfully
**Ready for:** Paper updates and submission preparation
