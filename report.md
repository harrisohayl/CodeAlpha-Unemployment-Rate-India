# India Unemployment Analysis: Trends, COVID-19 Impact, and Policy Insights

## 1. Overview

This analysis covers two complementary datasets on estimated unemployment across 28 Indian states/UTs:

- **Dataset 1** (`Unemployment_in_India.csv`): May 2019 – June 2020, with a Rural/Urban split.
- **Dataset 2** (`Unemployment_Rate_upto_11_2020.csv`): January 2020 – October 2020, with regional zone (North/South/East/West/Northeast) and geographic coordinates.

Together they give a before-and-after view of India's labor market through the COVID-19 lockdown.

## 2. Data Cleaning

- Stripped whitespace from column headers and string fields (a common artifact of this dataset).
- Removed 28 fully-blank rows in Dataset 1.
- Parsed all dates to proper `datetime` format (`DD-MM-YYYY`).
- Standardized column names (`unemployment_rate`, `employed`, `labour_participation_rate`, `state`, `zone`, etc.) for consistency across both files.
- Cleaned files exported to `data/cleaned_unemployment_in_india.csv` and `data/cleaned_unemployment_upto_nov2020.csv`.

## 3. National Trend & the COVID-19 Shock

![National Trend](charts/01_national_trend_covid.png)

The national average unemployment rate held in a fairly stable **8–10% band** through late 2019 and early 2020. It then spiked sharply in **April 2020**, coinciding exactly with the nationwide lockdown announced March 25, 2020.

**Phase comparison:**

| Phase | Avg. Unemployment Rate |
|---|---|
| Pre-COVID | 9.51% |
| Lockdown (Mar–May 2020) | 19.68% |
| Post-Lockdown Recovery | 11.90% |

![Phase Comparison](charts/02_covid_phase_comparison.png)

The lockdown **roughly doubled** the unemployment rate nationally. Recovery began quickly once restrictions eased, but by June 2020 the rate had not yet returned to pre-COVID levels — landing about **2.4 points above baseline**, suggesting a partial, not full, snapback in the short window this data covers.

## 4. Which States Were Hit Hardest?

![Top States COVID Peak](charts/03_top_states_covid_peak.png)

During the April 2020 peak, unemployment surged past 40–50% in several states, with **Puducherry, Tripura, Jharkhand, Bihar, and Haryana** among the worst affected. States with a higher share of informal, daily-wage, and migrant labor (construction, small manufacturing, gig-style urban work) appear to have absorbed the sharpest shocks, consistent with the sudden halt of in-person, cash-based economic activity during lockdown.

Looking at the **full period average** (not just the peak):

![State Averages](charts/08_state_avg_full_period.png)

**Tripura, Haryana, Jharkhand, Bihar, and Himachal Pradesh** show the highest average unemployment overall, while **Meghalaya, Odisha, Assam, Uttarakhand, and Gujarat** show the lowest — a pattern that predates COVID and points to structural, not just pandemic-driven, differences in labor markets across states.

## 5. Rural vs Urban Divide

![Rural vs Urban](charts/04_rural_vs_urban.png)

Across the full period, **urban unemployment (13.28%) ran meaningfully higher than rural (10.38%)**. This is a distinctive feature of India's labor market: rural areas benefit from agriculture as a fallback employer and from safety-net programs like MGNREGA, which cushioned the shock. Urban unemployment spiked more violently during lockdown, reflecting the concentration of contact-dependent service and informal-sector jobs in cities.

## 6. Regional (Zonal) Differences

![Zone Comparison](charts/06_zone_comparison.png)

| Zone | Avg. Unemployment Rate (2020) |
|---|---|
| North | 15.89% |
| East | 13.92% |
| Northeast | 10.95% |
| South | 10.45% |
| West | 8.24% |

The **North zone consistently ran hottest**, nearly double the **West zone**, which stayed the most resilient throughout 2020. This gap likely reflects differences in industrial mix — the West (Gujarat, Maharashtra) has a larger manufacturing and export base with more diversified employment, while northern states leaned more heavily on sectors that were harder-hit by lockdown restrictions.

## 7. Seasonal Patterns (Pre-COVID)

![Seasonal Pattern](charts/05_seasonal_pattern.png)

Excluding the COVID period to isolate a "normal" cycle, unemployment shows a mild seasonal rhythm: a small **uptick in January–February and again in October–November**, with a relative trough around **May–July**. This is consistent with agricultural labor cycles (post-harvest slack season in winter) and hiring patterns tied to the mid-year fiscal calendar.

## 8. Labour Participation & Employment Correlation

![Correlation Heatmap](charts/07_correlation_heatmap.png)

Interestingly, the **unemployment rate showed almost no linear correlation with the labour participation rate (0.003)** — meaning states with more people actively seeking work weren't necessarily the ones with higher unemployment. There is a **weak negative correlation with total employed persons (-0.22)**, a mild size effect: larger labor pools show slightly lower measured unemployment rates.

## 9. Key Insights

1. **COVID-19 roughly doubled national unemployment**, from ~9.5% to ~19.7%, with the shock concentrated almost entirely in April–May 2020.
2. **Recovery was underway by June 2020 but incomplete** — the rate remained above pre-pandemic baseline.
3. **Urban areas absorbed a larger shock than rural areas**, likely due to reliance on informal, contact-dependent service jobs and the partial buffering role of agriculture and rural employment schemes.
4. **Structural, pre-existing gaps between states persist independent of COVID** — Tripura, Haryana, Bihar, and Jharkhand show chronically elevated unemployment, pointing to underlying labor-market weaknesses rather than one-off shocks.
5. **The North zone is the country's most persistent unemployment hotspot**, while the West is the most resilient — a pattern worth investigating alongside industrial composition and investment flows.
6. **Mild seasonality exists** tied to agricultural and fiscal-year cycles, useful for anticipating short-term policy interventions (e.g., timing public works programs).

## 10. Policy Recommendations

- **Target relief and reskilling programs geographically**: states like Tripura, Haryana, Bihar, and Jharkhand warrant sustained, not just crisis-driven, labor-market intervention.
- **Strengthen urban safety nets**: extend an MGNREGA-style guaranteed-employment scheme to urban informal workers, who currently lack the buffer rural workers have.
- **Use seasonal patterns to time public works spending**: front-load job-guarantee program funding into the January–February and October–November windows when unemployment typically ticks up.
- **Investigate the North-West zone gap**: understand what makes western-zone labor markets more resilient (industrial diversification, ease of doing business, infrastructure) and study whether those conditions are replicable in northern states.
- **Build early-warning monitoring**: given how fast the April 2020 spike hit, monthly (rather than quarterly) unemployment tracking would allow faster policy response to future shocks.

## 11. Files in This Project

```
unemployment_project/
├── data/
│   ├── Unemployment_in_India.csv            (raw)
│   ├── Unemployment_Rate_upto_11_2020.csv    (raw)
│   ├── cleaned_unemployment_in_india.csv     (cleaned)
│   └── cleaned_unemployment_upto_nov2020.csv (cleaned)
├── scripts/
│   └── analysis.py                           (full analysis pipeline)
├── charts/
│   └── 01–08 PNG charts referenced above
└── report.md                                  (this file)
```
