# NGFS Phase V Carbon Price Data

## Source
- **Database:** NGFS IIASA Scenario Explorer (https://data.ene.iiasa.ac.at/ngfs/)
- **Model:** MESSAGEix-GLOBIOM 2.0-M-R12-NGFS
- **Region:** Other Pacific Asia (includes Korea, Japan, Australia, New Zealand)
- **Variable:** Price|Carbon
- **Phase:** NGFS Phase V (November 2024)
- **Downloaded:** January 2025

## Currency Conversion
- **Original:** US$2010/tCO2
- **Converted to:** US$2024/tCO2
- **Inflation Factor:** 1.423 (US CPI: 2010=218.056, 2024=310.326)

## Regional Justification for "Other Pacific Asia"
Korea is classified under the "Other Pacific Asia" region in MESSAGEix-GLOBIOM, which aggregates:
- **South Korea** (primary focus)
- Japan (similar advanced economy context)
- Australia, New Zealand (OECD Pacific members)

This regional grouping is appropriate because:
1. **Economic Development:** All are high-income OECD economies with similar carbon pricing trajectories
2. **Industrial Structure:** Heavy industry (steel, chemicals) represents significant share of emissions
3. **Policy Context:** All have or are implementing carbon pricing mechanisms
4. **Trade Integration:** Closely integrated supply chains and trade relationships

## Scenarios Used

### Net Zero 2050
- Limits warming to 1.5°C
- Achieves net-zero CO2 emissions globally by 2050
- Most aggressive carbon pricing pathway
- 2030: $383/tCO2, 2050: $638/tCO2 (US$2024)

### Below 2°C
- Aligns with Paris Agreement "well below 2°C" goal
- Moderate policy ambition
- 2030: $71/tCO2, 2050: $166/tCO2 (US$2024)

### Nationally Determined Contributions (NDCs)
- Based on current national climate pledges as of March 2024
- Gradual strengthening without major policy shifts
- 2030: $118/tCO2, 2050: $130/tCO2 (US$2024)

## Key Differences from Previous Literature

Previous steel sector studies often used:
- **REMIND-MAgPIE** (not available in NGFS Phase V at time of analysis)
- **GCAM** (focuses more on land-use/agriculture, less suitable for industrial analysis)

MESSAGEix-GLOBIOM is preferred because:
1. IIASA's flagship energy systems optimization model
2. Detailed bottom-up technology representation (matches our MILP approach)
3. Extensively validated for energy-intensive industries
4. Most widely used in industrial decarbonization literature

## Data File
Raw NGFS export: `data/ngfs_snapshot_1762055076.csv`
Processed for model: `data/v2_sheets/carbon_price.csv`
Original backup: `data/v2_sheets/carbon_price_OLD_backup.csv`

## Citation
Network for Greening the Financial System (2024). NGFS Climate Scenarios for
Central Banks and Supervisors -- Phase V. November 2024. NGFS Secretariat, Paris.
Available at https://www.ngfs.net/ngfs-scenarios-portal/ and
https://data.ene.iiasa.ac.at/ngfs/
