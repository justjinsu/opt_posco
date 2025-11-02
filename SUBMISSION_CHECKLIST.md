# Energy Policy Submission Checklist - Final Preparation

## 📊 NGFS Data Update Summary

### ✅ Completed Tasks

1. **Downloaded NGFS Phase V Data**
   - Source: NGFS IIASA Scenario Explorer
   - Model: MESSAGEix-GLOBIOM 2.0-M-R12
   - Region: Other Pacific Asia
   - File: `data/ngfs_snapshot_1762055076.csv`

2. **Converted to US$2024**
   - Inflation factor: 1.423 (2010→2024)
   - Created: `data/v2_sheets/carbon_price.csv`
   - Backup: `data/v2_sheets/carbon_price_OLD_backup.csv`

3. **Updated Paper Values**
   - ✅ Abstract: New carbon prices
   - ✅ Highlights: New carbon prices
   - ✅ Section 3.2.3: Added MESSAGEix-Global specification
   - ✅ Section 3.3: Full regional justification
   - ✅ References: Updated to Phase V

4. **Updated Cover Letter**
   - ✅ Fixed overshoot percentage (4% → 7%)

5. **Documentation Created**
   - ✅ `NGFS_DATA_NOTES.md` - Data provenance
   - ✅ `RUN_MODEL_INSTRUCTIONS.md` - How to run model
   - ✅ `SUBMISSION_CHECKLIST.md` - This file

---

## ⚠️ CRITICAL: Before Submission

### YOU MUST DO THESE STEPS:

### 1. **Run the Optimization Model** 🔴 REQUIRED

```bash
cd /Users/jinsupark/jinsu-coding/opt_posco/opt_posco
source .venv/bin/activate  # or your venv
python -m src.run --data data/posco_parameters_consolidated.xlsx --output outputs
```

**Why?** The new NGFS carbon prices are significantly different:
- Net Zero 2030: **$383** (was $150) - **+156%**
- NDCs 2030: **$118** (was $40) - **+195%**

This will change ALL results in the paper!

### 2. **Update Results Throughout Paper** 🔴 REQUIRED

After model runs, check these sections and update values:

#### Section 4 (Results)
- [ ] Line 452: Annual emissions by scenario
- [ ] Line 508-514: Cumulative emissions and overshoots
- [ ] Line 532-536: Total system costs
- [ ] Line 559-565: No-CCUS sensitivity results
- [ ] Line 586-588: Hydrogen sensitivity results

#### Tables (in `tables/` directory)
- [ ] `scenario_comparison.tex` - Update ALL values
- [ ] `annual_technology_shares.tex` - Update technology percentages
- [ ] `cost_abatement.tex` - Update cost metrics
- [ ] Check other tables for consistency

#### Figures
- [ ] Regenerate ALL figures with `generate_publication_figures.py`
- [ ] Check `figures/` directory for updated plots
- [ ] Verify figures render correctly in compiled PDF

#### Abstract & Conclusion
- [ ] Abstract (lines 56-57): Update cumulative emissions
- [ ] Conclusion (Section 7): Update summary statistics

### 3. **Compile and Check LaTeX** 🔴 REQUIRED

```bash
cd /Users/jinsupark/jinsu-coding/opt_posco/opt_posco
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Check the PDF
open main.pdf
```

**Check for:**
- [ ] All figures appear correctly
- [ ] No LaTeX errors or warnings
- [ ] References formatted properly
- [ ] Tables formatted correctly
- [ ] Highlights count = 5 (not 6)
- [ ] Page numbers and formatting look professional

### 4. **Compile Cover Letter** 🔴 REQUIRED

```bash
cd submission/
pdflatex cover_letter.tex
open cover_letter.pdf
```

**Verify:**
- [ ] Overshoot percentage is 7% (not 4%)
- [ ] Title matches main.tex
- [ ] Your contact details correct

---

## 📋 Energy Policy Requirements Check

### Manuscript Format
- [x] elsarticle document class ✓
- [x] authoryear bibliography style ✓
- [x] Title and author information ✓
- [x] 5 highlights (3-5 required) ✓
- [x] Abstract with keywords ✓
- [x] JEL codes ✓
- [x] Structured sections ✓

### Content Requirements
- [x] Introduction with clear research question ✓
- [x] Literature review ✓
- [x] Methodology description ✓
- [x] Data sources documented ✓
- [ ] **Results section** - MUST UPDATE AFTER MODEL RUN 🔴
- [x] Discussion and policy implications ✓
- [x] Limitations section ✓
- [x] Conclusion ✓

### Supporting Materials
- [x] References cited properly ✓
- [x] Figures with captions ✓
- [x] Tables with notes ✓
- [x] Data availability statement ✓
- [x] Funding statement ✓
- [x] Conflict of interest statement ✓
- [x] Acknowledgements ✓

### Submission Materials
- [ ] Main manuscript PDF
- [ ] Cover letter PDF
- [ ] All figure files (high resolution)
- [ ] Supplementary materials (optional: code, data)
- [ ] Suggested reviewers (in cover letter ✓)

---

## 🎯 Expected Changes After Model Run

### Old Values (Paper Currently States):
```
Net Zero 2050: $150 (2030), $450 (2050)
Below 2°C: $80 (2030), $240 (2050)
NDCs: $40 (2030), $100 (2050)
```

### New Values (Already Updated in Paper):
```
Net Zero 2050: $383 (2030), $638 (2050)  ← +156% and +42%
Below 2°C: $71 (2030), $166 (2050)      ← -11% and -31%
NDCs: $118 (2030), $130 (2050)          ← +195% and +30%
```

### Impact on Results (Expected):

**Net Zero 2050:**
- Higher early prices → Earlier technology adoption
- Budget overshoot may DECREASE (currently +7%)
- CCUS and EAF may deploy sooner
- Lower total ETS costs (more early abatement)

**Below 2°C:**
- Lower 2050 prices → Less aggressive late transition
- Budget overshoot may INCREASE (currently +54%)
- May stick with BF-BOF longer

**NDCs:**
- Much higher prices throughout → Significant changes!
- Budget overshoot may DECREASE substantially (currently +78%)
- May trigger CCUS deployment (wasn't in old NDC case)

---

## 📤 Submission Portal Information

**Journal:** Energy Policy (Elsevier)
**Portal:** https://www.editorialmanager.com/enpol/

### You Will Need:
1. **Manuscript PDF** (main.pdf)
2. **Cover Letter PDF** (cover_letter.pdf)
3. **All figure files** (from figures/ directory)
   - Ensure high resolution (300+ DPI)
   - PDF or EPS format preferred
4. **Suggested reviewers** (already in cover letter):
   - Prof. Oliver Sartor (Columbia)
   - Dr. Valentin Vogl (Lund University)
   - Dr. Meredith Fowlie (UC Berkeley)
5. **Keywords:** Steel decarbonization, carbon pricing, mixed-integer optimization, hydrogen DRI, CCUS, Korea ETS, CBAM
6. **JEL Codes:** Q41, Q54, L61

### Optional (Recommended):
- Supplementary materials:
  - Model code (src/ directory)
  - Input data (data/ directory)
  - Output results (outputs/ directory)
- Graphical abstract (Energy Policy encourages these)
- Data repository link (Zenodo, GitHub, etc.)

### Timeline Expectations:
- First decision: ~30 days
- After review: ~73 days
- Total to acceptance: ~181 days (~6 months)
- Publication: ~12 days after acceptance

### Open Access:
- **Optional:** $4,220 USD
- **Not required** for publication

---

## ✅ Final Pre-Submission Checklist

### Before Running Model:
- [x] NGFS data downloaded and verified
- [x] Carbon price CSV file updated
- [x] Paper values updated with new prices
- [x] Regional justification added
- [x] Currency conversion documented
- [x] References updated to Phase V

### After Running Model (DO THESE!):
- [ ] Model ran successfully (no errors)
- [ ] Output files generated
- [ ] Results seem reasonable
- [ ] Updated ALL result values in paper
- [ ] Regenerated ALL figures
- [ ] Updated ALL tables
- [ ] Recompiled LaTeX successfully
- [ ] Checked PDF appearance
- [ ] Cover letter compiled
- [ ] No TODOs or placeholders in text
- [ ] All citations complete
- [ ] Figures at publication quality (300+ DPI)

### Final Review:
- [ ] Read abstract aloud - does it flow?
- [ ] Check highlights - are they compelling?
- [ ] Skim introduction - clear motivation?
- [ ] Review figures - self-explanatory captions?
- [ ] Check tables - readable and formatted?
- [ ] Conclusion - answers research question?
- [ ] Policy implications - actionable?

### Administrative:
- [ ] Author name and affiliation correct
- [ ] Email contact information correct
- [ ] Conflict of interest appropriate
- [ ] Data availability statement accurate
- [ ] All co-authors approved (if any)

---

## 🚨 Common Pitfalls to Avoid

1. **DON'T submit without re-running model** - Results WILL change!
2. **DON'T forget to regenerate figures** - Old figures won't match new text
3. **DON'T submit with placeholder text** - Remove all TODO/TBD markers
4. **DON'T mix up scenario labels** - Check all NZ2050/Below2C/NDCs are consistent
5. **DON'T forget table footnotes** - Explain abbreviations and units
6. **DON'T submit low-res figures** - Energy Policy requires 300+ DPI
7. **DON'T forget to compile bibliography** - Run bibtex!

---

## 📝 Post-Submission Tasks

After submitting:
1. Save submission confirmation email
2. Note manuscript number
3. Add calendar reminder for ~30 days (first decision)
4. Archive this version of paper (tag in git if using)
5. Don't start new analyses until after review
6. Prepare response letter template for reviewers

---

## 🆘 If Something Goes Wrong

### Model Won't Run:
- Check `RUN_MODEL_INSTRUCTIONS.md`
- Verify Python environment
- Check solver installation
- Review error messages carefully

### Results Look Weird:
- Compare to old outputs (in archive/)
- Check if carbon prices loaded correctly
- Verify all constraints are active
- Run sanity checks (test scripts in tests/)

### LaTeX Won't Compile:
- Check for special characters (%, &, etc.)
- Verify all \cite{} keys exist in references.bib
- Check figure paths are correct
- Look for unclosed braces {}

### Figures Missing:
- Check graphics path in main.tex (line 22)
- Verify files exist in figures/ directory
- Check file extensions (.png, .pdf, etc.)
- Regenerate with generate_publication_figures.py

---

## ✨ You're Almost There!

This is high-quality work. The methodology is sound, the policy relevance is clear, and the findings are important.

**Just run the model with new data, update the results, and submit!**

Good luck! 🚀
