#!/usr/bin/env python3
"""
Script to reduce paper to ~8,000 words while preserving all figures and tables.
Strategy: Heavy cuts to Intro, Literature, Discussion, Conclusion
"""

# This script identifies line ranges to delete from the old sections
# Manual approach due to LaTeX complexity

print("""
REDUCTION PLAN TO 8,000 WORDS

Based on analysis, here are the exact line ranges to DELETE:

1. Literature Review - Remove old subsections (lines 88-122)
   Keep: New condensed version (lines 76-86)

2. Methodology - Will keep mostly intact, trim verbose explanations

3. Data & Scenarios - Heavy reduction, keep only essentials

4. Results - Light trimming only

5. Discussion - HEAVY cuts (4,681 → 1,800 words = -2,881 words)

6. Conclusion - HEAVY cuts (1,558 → 600 words = -958 words)

Due to LaTeX formatting complexity, recommend manual editing with guidance:
- Delete lines 88-122 (old Literature subsections)
- Condense Discussion subsections
- Trim Conclusion to focus on key findings only

Would you like specific paragraph-by-paragraph guidance?
""")
