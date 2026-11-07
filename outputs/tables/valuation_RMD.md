# ResMed (RMD): valuation workings

Money in $ millions unless stated. Rebuild this in a spreadsheet: every number below is an input or a step.

## Inputs

| Input | Value |
|---|---|
| Financial year (base) | Jun 2026 |
| Revenue ($m) | 5653 |
| Operating margin today (as reported) | 33.4% |
| EBITDA margin today (operating income + D&A) | 37.7% |
| Target EBITDA margin (year 10) | 37.7% |
| Year-1 revenue growth | 7.0% |
| Terminal growth | 2.5% |
| Tax rate (3-yr pooled) | 18.9% |
| D&A % of revenue (latest year) | 4.3% |
| Capex % of revenue (3-yr avg; D&A converges to it) | 2.5% |
| Working capital per extra $ of revenue | 0.9% (3-yr cash flow statement: 13 into working capital for 1,430 of added revenue; floor 0) |
| Debt ($m) | 826 |
| Cash + short-term investments ($m) | 1469 |
| Shares (m) | 144.2 |
| Share price, 6 Nov 2026 ($) | 235.3 |
| Risk-free rate (10-yr Treasury) | 4.84% |
| Beta: measured -> adjusted | 0.67 -> 0.78 |
| Equity risk premium | 5.0% |
| Cost of equity | 8.73% = 4.84% + 0.78 x 5.0% |
| Cost of debt (after tax) | 4.74% = (4.84% + 1.0%) x (1 - 18.9%) |
| Weights (equity / debt) | 97.6% / 2.4% |
| WACC | 8.64% |
| Base-case reasoning | Year-1 revenue growth = core constant-currency growth in Q1 FY2027 (7%; reported growth 6%). Target operating margin = latest year's (FY2026), i.e. no further expansion assumed in the base case. |
| Source | https://www.manilatimes.net/2026/10/30/tmt-newswire/globenewswire/resmed-inc-announces-results-for-the-first-quarter-of-fiscal-year-2027/2457769/amp |

## Base-case forecast (growth and margin in %)

| year | growth | revenue | ebitda_margin | ebitda | da | ebit | tax | capex | change_nwc | fcff | discount_factor | pv_fcff |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 7.0 | 6049.0 | 37.7 | 2280.0 | 250.0 | 2030.0 | 383.0 | 152.0 | 4.0 | 1742.0 | 0.9205 | 1603.0 |
| 2 | 6.6 | 6445.0 | 37.7 | 2429.0 | 255.0 | 2174.0 | 410.0 | 162.0 | 4.0 | 1854.0 | 0.8473 | 1571.0 |
| 3 | 6.1 | 6839.0 | 37.7 | 2578.0 | 258.0 | 2319.0 | 437.0 | 172.0 | 3.0 | 1965.0 | 0.78 | 1532.0 |
| 4 | 5.7 | 7225.0 | 37.7 | 2723.0 | 260.0 | 2463.0 | 465.0 | 182.0 | 3.0 | 2074.0 | 0.7179 | 1489.0 |
| 5 | 5.2 | 7601.0 | 37.7 | 2865.0 | 260.0 | 2605.0 | 491.0 | 191.0 | 3.0 | 2179.0 | 0.6609 | 1440.0 |
| 6 | 4.8 | 7962.0 | 37.7 | 3001.0 | 258.0 | 2743.0 | 517.0 | 200.0 | 3.0 | 2280.0 | 0.6083 | 1387.0 |
| 7 | 4.3 | 8304.0 | 37.7 | 3130.0 | 254.0 | 2876.0 | 542.0 | 209.0 | 3.0 | 2376.0 | 0.56 | 1330.0 |
| 8 | 3.8 | 8624.0 | 37.7 | 3250.0 | 248.0 | 3003.0 | 566.0 | 217.0 | 3.0 | 2465.0 | 0.5155 | 1270.0 |
| 9 | 3.4 | 8917.0 | 37.7 | 3361.0 | 240.0 | 3121.0 | 588.0 | 224.0 | 3.0 | 2546.0 | 0.4745 | 1208.0 |
| 10 | 3.0 | 9180.0 | 37.7 | 3460.0 | 231.0 | 3229.0 | 609.0 | 231.0 | 2.0 | 2618.0 | 0.4368 | 1143.0 |
| 11 | 2.5 | 9409.0 | 37.7 | 3547.0 | 237.0 | 3310.0 | 624.0 | 237.0 | 2.0 | 2684.0 |  |  |

Year 11 is only used for the terminal value: its FCFF / (WACC - terminal growth).

## Base-case result

- PV of years 1-10 cash flows: 13,974
- Terminal value: 43,734; discounted: 19,101 (58% of enterprise value)
- Enterprise value: 33,075
- Equity value = EV - debt + cash: 33,719
- **Value per share: $233.77** vs price $235.30
- Sanity check: implied terminal EV/EBITDA 12.3x

## Scenarios (value per share)

- bear: $157.59
- base: $233.77
- bull: $373.48

## Reverse DCF

- Year-1 growth needed to justify $235.30: **7.1%** (10-year revenue CAGR 5.0%) vs base case 7.0% and 3-year history 10.2%

## Comparables

| Peer | EV/EBITDA | EV/Sales |
|---|---|---|
| DXCM | 25.7 | 6.4 |
| PODD | 18.6 | 3.9 |
| ABT | 17.5 | 4.4 |
| MDT | 15.8 | 4.1 |
| EW | 39.3 | 9.2 |

- EV/EBITDA: $263 - $384 (median $279)
- EV/Sales: $165 - $256 (median $178)

## Monte Carlo (10,000 runs)

- 10th / 50th / 90th percentile: $207 / $234 / $267
- P(value > price): 47%
- **Decision: HOLD**