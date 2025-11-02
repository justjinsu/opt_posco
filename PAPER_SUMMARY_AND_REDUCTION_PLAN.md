# Paper Summary and Reduction Plan (19,600 → 7,500 words)

**Current:** 19,600 words | **Target:** 7,500 words | **Reduction needed:** 12,100 words (62%)

---

## 📖 PAPER SUMMARY

### **Title**
Testing the limits of carbon pricing: Can Korea's emissions trading system align steel industry investments with national climate targets?

### **Core Research Question**
Can carbon pricing alone drive POSCO's steel production technology choices to remain within Korea's climate-consistent carbon budget?

### **Answer**
**Mixed verdict with critical insights:**
- ✅ **Net Zero 2050 pricing nearly works** (+3.2% overshoot) - demonstrating ambitious early pricing CAN align investments
- ❌ **Moderate pricing fails catastrophically** - Below 2°C and NDCs both overshoot by +78%
- 🔬 **Technology choice matters** - CCUS vs H2-DRI serve as alternative pathways (41% H2-DRI when CCUS unavailable)
- 🏗️ **Infrastructure critical** - Price signals alone insufficient; need CO₂ networks OR H₂ supply chains

### **Key Findings**

1. **Carbon pricing is powerful but needs to be ambitious** (Net Zero: 1,146 MtCO₂ vs budget 1,110 MtCO₂)
2. **Technology thresholds matter** - CCUS activates at $165/tCO₂, scrap-EAF at $110/tCO₂, H2-DRI >$400/tCO₂
3. **Free allocation undermines pricing** - Only 2.5% of Net Zero emissions face actual ETS costs
4. **Higher prices reduce total costs** - $810/t under Net Zero vs $861/t under NDCs (capital substitution effect)
5. **Policy complementarity essential** - Price floors + infrastructure + faster allocation phase-out needed

### **Methodology**
Mixed-integer optimization model of POSCO's technology portfolio (2025-2050):
- 7 technology routes (BF-BOF, CCUS, Scrap-EAF, H2-DRI, etc.)
- 3 NGFS Phase V carbon price scenarios
- Sectoral carbon budget: 1,110 MtCO₂
- Discrete investment decisions with relining cycles

---

## 📊 CURRENT STRUCTURE & WORD COUNT

| Section | Words | % of Total | Status |
|---------|-------|------------|--------|
| **Highlights** | 443 | 2.3% | ✅ Keep as-is |
| **Introduction** | 941 | 4.9% | 🔧 Reduce to ~600 |
| **Literature Review** | 1,820 | 9.5% | ⚠️ **CUT HEAVILY to ~800** |
| - Steel decarbonization | 428 | | |
| - Carbon pricing effectiveness | 450 | | |
| - Carbon budgets | 409 | | |
| - Research contribution | 389 | | |
| **Methodology** | 2,344 | 12.2% | 🔧 Reduce to ~1,200 |
| - Framework | 329 | | |
| - Optimization formulation | 1,095 | | ⚠️ Simplify math |
| - Carbon budget assessment | 394 | | |
| - Scenario design | 340 | | |
| - Solution method | 99 | | |
| **Data & Scenarios** | 2,574 | 13.4% | ⚠️ **MOVE TO SUPPLEMENT ~500** |
| - System boundary | 288 | | Move to supplement |
| - Technology portfolio | 688 | | Move to supplement |
| - Carbon price scenarios | 557 | | Keep brief version |
| - Demand projection | 189 | | Move to supplement |
| - Input costs | 405 | | Move to supplement |
| - Technology costs | 325 | | Move to supplement |
| **Results** | 2,634 | 13.7% | 🔧 Reduce to ~2,000 |
| - Emission reductions | 239 | | Keep |
| - Technology transitions | 574 | | Keep |
| - Budget overshoots | 546 | | Keep |
| - Cost analysis | 490 | | Shorten |
| - No-CCUS sensitivity | 414 | | Shorten |
| - H2 cost sensitivity | 371 | | **CUT** or move to supplement |
| **Discussion** | 4,621 | 24.0% | ⚠️ **CUT HEAVILY to ~1,500** |
| - Adequacy gap | 816 | | Reduce to ~400 |
| - Political economy | 1,069 | | **CUT to ~300** |
| - Policy package | 2,736 | | ⚠️ **CUT to ~800** (move detail to supplement) |
| **Limitations** | 216 | 1.1% | 🔧 Reduce to ~150 |
| **Conclusion** | 2,278 | 11.8% | 🔧 Reduce to ~1,200 |
| - Key findings | 670 | | Reduce |
| - Policy implications | 663 | | Reduce |
| - Broader implications | 604 | | Shorten |
| - Final reflections | 341 | | **CUT** |
| **Admin** | 78 | 0.4% | Keep |
| **TOTAL** | **19,210** | **100%** | → **7,500** |

---

## 🎯 REDUCTION STRATEGY (19,600 → 7,500 words)

### **Phase 1: Structural Cuts** (-8,500 words)

#### **1. Literature Review: 1,820 → 800 words** (-1,020 words)
**Current:** 4 long subsections reviewing steel tech, carbon pricing, budgets, research gap
**New structure:**
- Merge into 2 tight subsections:
  - "Steel decarbonization and carbon pricing" (~400 words)
  - "Research gap and contribution" (~400 words)
- **Action:** Cut literature citations by 50%, focus only on directly relevant studies
- **Move to supplement:** Detailed technology comparisons, international ETS reviews

#### **2. Data & Scenarios: 2,574 → 500 words** (-2,074 words)
**Current:** 6 detailed subsections on data sources and parameters
**New structure:**
- Collapse into 1 concise section (~500 words)
- Keep: NGFS scenario specifications, key technology routes
- **Move to supplement:**
  - Full technology portfolio specs (688 words)
  - Input cost details (405 words)
  - Technology cost tables (325 words)
  - Demand projections (189 words)
  - System boundary details (288 words)

#### **3. Discussion - Policy Package: 2,736 → 800 words** (-1,936 words)
**Current:** 5 detailed subsections on policy recommendations
**New structure:**
- Condense to 3 key policy domains (~800 words):
  - Carbon price floors + allocation phase-out (~300 words)
  - Infrastructure provision (~250 words)
  - Risk-sharing mechanisms (~250 words)
- **Move to supplement:**
  - Detailed policy implementation steps
  - International precedents (UK, Norway, Germany examples)
  - Fiscal analysis

#### **4. Discussion - Political Economy: 1,069 → 300 words** (-769 words)
**Current:** Long discussion of institutional barriers, lobbying, path dependency
**New:** Tight synthesis of key barriers (~300 words)
- **Move to supplement:** Detailed EU ETS comparisons, regulatory capture analysis

#### **5. Conclusion - Cut "Broader Implications" & "Final Reflections"** (-945 words)
**Current:** 604 + 341 = 945 words on generalizability and future research
**New:** Merge into tightened "Policy Implications" section
- **Action:** Remove speculative future research directions, focus on Korea-specific takeaways

---

### **Phase 2: Targeted Reductions** (-3,600 words)

#### **6. Methodology - Simplify Math: 2,344 → 1,200 words** (-1,144 words)
**Current:** Dense optimization formulation (1,095 words), detailed equations
**New structure:**
- Framework overview (~200 words)
- **Simplified** optimization description (~400 words) - key constraints only
- Scenario design (~300 words)
- Carbon budget assessment (~300 words)
- **Move to supplement:**
  - Full mathematical formulation
  - All constraint equations
  - Detailed variable definitions

#### **7. Results - Remove H2 Sensitivity: 2,634 → 2,000 words** (-634 words)
**Current:** 6 subsections including H2 cost breakthrough analysis (371 words)
**Action:**
- **Cut entirely:** "Hydrogen cost breakthroughs" subsection (371 words)
  - Finding: "cheap H2 doesn't solve the problem" - interesting but not core
- Shorten "No-CCUS sensitivity" from 414 → 250 words (-164 words)
- Tighten "Cost analysis" from 490 → 390 words (-100 words)

#### **8. Introduction: 941 → 600 words** (-341 words)
**Current:** Broad context-setting with multiple motivations
**New:** Tighter opening focused on:
- Korea steel sector importance
- Carbon pricing question
- Research contribution
- **Cut:** Lengthy international climate policy context

#### **9. Discussion - Adequacy Gap: 816 → 400 words** (-416 words)
**Current:** Detailed three-dimensional inadequacy analysis
**New:** Streamlined gap explanation emphasizing Net Zero near-success

#### **10. Conclusion - Tighten All Subsections: 2,278 → 1,200 words** (-1,078 words)
- Key findings: 670 → 450 words (-220 words)
- Policy implications: 663 → 450 words (-213 words)
- Broader implications: 604 → 300 words (-304 words)
- **Cut:** Final reflections entirely (341 words)

#### **11. Limitations: 216 → 150 words** (-66 words)
**Action:** Bulleted list of key limitations, remove elaboration

---

## 📋 REDUCTION SUMMARY TABLE

| Section | Current | Target | Reduction | Strategy |
|---------|---------|--------|-----------|----------|
| Highlights | 443 | 443 | 0 | Keep |
| Introduction | 941 | 600 | -341 | Tighten context |
| **Literature Review** | **1,820** | **800** | **-1,020** | **Merge subsections, cut 50% citations** |
| **Methodology** | **2,344** | **1,200** | **-1,144** | **Move math to supplement** |
| **Data & Scenarios** | **2,574** | **500** | **-2,074** | **Move 5 subsections to supplement** |
| Results | 2,634 | 2,000 | -634 | Cut H2 sensitivity, tighten others |
| **Discussion** | **4,621** | **1,600** | **-3,021** | **Move policy details to supplement** |
| Limitations | 216 | 150 | -66 | Bullet format |
| **Conclusion** | **2,278** | **1,200** | **-1,078** | **Cut final reflections, tighten** |
| Admin | 78 | 78 | 0 | Keep |
| **TOTAL** | **19,600** | **~7,571** | **-12,029** | **Target: 7,500** |

---

## 🎯 RECOMMENDED APPROACH

### **Option 1: Aggressive Cut (Recommended for Energy Policy)**

**Keep in main text (7,500 words):**
1. ✅ **Core story:** Net Zero nearly works (+3.2%), moderate pricing fails (+78%)
2. ✅ **Key findings:** Technology thresholds, cost paradox, infrastructure dependency
3. ✅ **Essential policy:** Price floors, allocation phase-out, infrastructure
4. ✅ **Simplified methods:** Conceptual framework, key constraints only

**Move to online supplement (~8,000 words):**
1. 📄 Full optimization formulation with all equations
2. 📄 Detailed technology specifications and cost parameters
3. 📄 Comprehensive policy implementation roadmap
4. 📄 Political economy deep dive
5. 📄 H2 cost sensitivity analysis
6. 📄 Extended data tables

### **Option 2: Target Different Journal**

If you prefer to keep more content, consider:
- **Applied Energy** (no strict word limit, typically 8,000-15,000 words)
- **Energy Economics** (typically 8,000-12,000 words)
- **Nature Energy** (Articles: 3,000-4,000 words + extensive supplement)

---

## ✂️ NEXT STEPS

Would you like me to:

1. **Execute the reduction plan?** I can systematically cut/condense the paper to 7,500 words
2. **Create a supplement document?** Move technical details to a separate supplementary file
3. **Show you specific sections for approval?** Review cuts section-by-section before implementing

**Recommendation:** Execute Option 1 - aggressive cut to 7,500 words + create comprehensive supplement. This gives you:
- Clean, focused main paper (7,500 words) for Energy Policy
- Rich technical supplement for readers who want details
- Best of both worlds

Let me know how you'd like to proceed!
