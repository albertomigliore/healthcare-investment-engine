# DexCom (DXCM): valuation workings

Money in $ millions unless stated. Rebuild this in a spreadsheet: every number below is an input or a step.

## Inputs

| Input | Value |
|---|---|
| Financial year (base) | Dec 2025 |
| Revenue ($m) | 4662 |
| Operating margin today (as reported) | 19.6% |
| EBITDA margin today (operating income + D&A) | 25.0% |
| Target EBITDA margin (year 10) | 28.4% |
| Year-1 revenue growth | 12.5% |
| Terminal growth | 2.5% |
| Tax rate (3-yr pooled) | 22.1% |
| D&A % of revenue (latest year) | 5.4% |
| Capex % of revenue (3-yr avg; D&A converges to it) | 7.7% |
| Working capital per extra $ of revenue | 0.0% (3-yr cash flow statement: -215 into working capital for 1,752 of added revenue; floor 0) |
| Debt ($m) | 1390 |
| Cash + short-term investments ($m) | 1999 |
| Shares (m) | 384.8 |
| Share price, 6 Nov 2026 ($) | 79.41 |
| Risk-free rate (10-yr Treasury) | 4.84% |
| Beta: measured -> adjusted | 1.07 -> 1.05 |
| Equity risk premium | 5.0% |
| Cost of equity | 10.07% = 4.84% + 1.05 x 5.0% |
| Cost of debt (after tax) | 4.55% = (4.84% + 1.0%) x (1 - 22.1%) |
| Weights (equity / debt) | 95.7% / 4.3% |
| WACC | 9.83% |
| Base-case reasoning | Year-1 growth = midpoint of 2026 revenue guidance (12-13%, raised 29 Oct 2026). Target margin 23% = 2026 non-GAAP operating margin guidance (~24%) less ~1 point for items excluded from non-GAAP (Q3 2026: GAAP 24.3% vs non-GAAP 25.3%). |
| Source | https://www.investing.com/news/company-news/dexcom-q3-2026-slides-margins-hit-multiyear-high-guidance-raised-93CH-4985422 |

## Base-case forecast (growth and margin in %)

| year | growth | revenue | ebitda_margin | ebitda | da | ebit | tax | capex | change_nwc | fcff | discount_factor | pv_fcff |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 12.5 | 5245.0 | 25.3 | 1327.0 | 296.0 | 1032.0 | 228.0 | 406.0 | 0.0 | 693.0 | 0.9105 | 631.0 |
| 2 | 11.5 | 5848.0 | 25.6 | 1500.0 | 343.0 | 1157.0 | 255.0 | 453.0 | 0.0 | 792.0 | 0.8289 | 656.0 |
| 3 | 10.5 | 6462.0 | 26.0 | 1680.0 | 394.0 | 1285.0 | 284.0 | 500.0 | 0.0 | 895.0 | 0.7547 | 676.0 |
| 4 | 9.5 | 7076.0 | 26.3 | 1863.0 | 448.0 | 1415.0 | 312.0 | 548.0 | 0.0 | 1003.0 | 0.6872 | 689.0 |
| 5 | 8.5 | 7677.0 | 26.7 | 2048.0 | 505.0 | 1544.0 | 341.0 | 594.0 | 0.0 | 1113.0 | 0.6256 | 696.0 |
| 6 | 7.5 | 8253.0 | 27.0 | 2230.0 | 562.0 | 1669.0 | 368.0 | 639.0 | 0.0 | 1223.0 | 0.5696 | 697.0 |
| 7 | 6.5 | 8789.0 | 27.4 | 2406.0 | 619.0 | 1787.0 | 395.0 | 680.0 | 0.0 | 1331.0 | 0.5186 | 690.0 |
| 8 | 5.5 | 9273.0 | 27.7 | 2570.0 | 674.0 | 1895.0 | 419.0 | 718.0 | 0.0 | 1433.0 | 0.4722 | 677.0 |
| 9 | 4.5 | 9690.0 | 28.1 | 2719.0 | 728.0 | 1991.0 | 440.0 | 750.0 | 0.0 | 1529.0 | 0.4299 | 657.0 |
| 10 | 3.5 | 10029.0 | 28.4 | 2848.0 | 776.0 | 2072.0 | 458.0 | 776.0 | 0.0 | 1614.0 | 0.3914 | 632.0 |
| 11 | 2.5 | 10280.0 | 28.4 | 2920.0 | 796.0 | 2124.0 | 469.0 | 796.0 | 0.0 | 1655.0 |  |  |

Year 11 is only used for the terminal value: its FCFF / (WACC - terminal growth).

## Base-case result

- PV of years 1-10 cash flows: 6,702
- Terminal value: 22,564; discounted: 8,832 (57% of enterprise value)
- Enterprise value: 15,534
- Equity value = EV - debt + cash: 16,143
- **Value per share: $41.95** vs price $79.41
- Sanity check: implied terminal EV/EBITDA 7.7x

## Scenarios (value per share)

- bear: $27.63
- base: $41.95
- bull: $67.06

## Reverse DCF

- Year-1 growth needed to justify $79.41: **28.0%** (10-year revenue CAGR 16.3%) vs base case 12.5% and 3-year history 17.0%

## Comparables

| Peer | EV/EBITDA | EV/Sales |
|---|---|---|
| PODD | 18.6 | 3.9 |
| ABT | 17.5 | 4.4 |
| RMD | 15.6 | 5.9 |
| MDT | 15.8 | 4.1 |
| EW | 39.3 | 9.2 |

- EV/EBITDA: $49 - $58 (median $55)
- EV/Sales: $51 - $73 (median $55)

## Monte Carlo (10,000 runs)

- 10th / 50th / 90th percentile: $37 / $42 / $48
- P(value > price): 0%
- **Decision: SELL**