# Globus Medical (GMED): valuation workings

Money in $ millions unless stated. Rebuild this in a spreadsheet: every number below is an input or a step.

## Inputs

| Input | Value |
|---|---|
| Financial year (base) | Dec 2025 |
| Revenue ($m) | 2939 |
| Operating margin today (as reported) | 16.3% |
| EBITDA margin today (operating income + D&A) | 25.7% |
| Target EBITDA margin (year 10) | 25.7% |
| Year-1 revenue growth | 5.0% |
| Terminal growth | 2.5% |
| Tax rate (3-yr pooled) | 14.3% |
| D&A % of revenue (latest year) | 9.4% |
| Capex % of revenue (3-yr avg; D&A converges to it) | 5.2% |
| Working capital per extra $ of revenue | 14.7% (3-yr cash flow statement: 281 into working capital for 1,916 of added revenue; floor 0) |
| Debt ($m) | 119 |
| Cash + short-term investments ($m) | 557 |
| Shares (m) | 135.1 |
| Share price, 6 Nov 2026 ($) | 71.05 |
| Risk-free rate (10-yr Treasury) | 4.84% |
| Beta: measured -> adjusted | 0.74 -> 0.82 |
| Equity risk premium | 5.0% |
| Cost of equity | 8.96% = 4.84% + 0.82 x 5.0% |
| Cost of debt (after tax) | 5.00% = (4.84% + 1.0%) x (1 - 14.3%) |
| Weights (equity / debt) | 98.8% / 1.2% |
| WACC | 8.91% |
| Base-case reasoning | Year-1 growth = 2026 revenue guidance (~$3.09bn, +5.1%, cut in Q3 2026; base business ex-Nevro +3% in Q3). NOT the 42% 3-year figure, which came mostly from acquisitions (NuVasive 2023, Nevro). Target margin = latest year's (FY2025). |
| Source | https://www.sec.gov/Archives/edgar/data/0001237831/000162828026071042/gmed-q32026ex991.htm |

## Base-case forecast (growth and margin in %)

| year | growth | revenue | ebitda_margin | ebitda | da | ebit | tax | capex | change_nwc | fcff | discount_factor | pv_fcff |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 5.0 | 3086.0 | 25.7 | 794.0 | 278.0 | 517.0 | 74.0 | 160.0 | 22.0 | 540.0 | 0.9182 | 495.0 |
| 2 | 4.8 | 3232.0 | 25.7 | 832.0 | 277.0 | 555.0 | 79.0 | 167.0 | 21.0 | 564.0 | 0.8431 | 476.0 |
| 3 | 4.5 | 3378.0 | 25.7 | 870.0 | 275.0 | 595.0 | 85.0 | 175.0 | 21.0 | 589.0 | 0.7741 | 456.0 |
| 4 | 4.2 | 3521.0 | 25.7 | 907.0 | 272.0 | 635.0 | 91.0 | 182.0 | 21.0 | 613.0 | 0.7108 | 436.0 |
| 5 | 4.0 | 3662.0 | 25.7 | 943.0 | 267.0 | 676.0 | 97.0 | 189.0 | 21.0 | 636.0 | 0.6527 | 415.0 |
| 6 | 3.8 | 3800.0 | 25.7 | 978.0 | 261.0 | 717.0 | 103.0 | 196.0 | 20.0 | 659.0 | 0.5993 | 395.0 |
| 7 | 3.5 | 3933.0 | 25.7 | 1013.0 | 253.0 | 759.0 | 109.0 | 203.0 | 19.0 | 681.0 | 0.5503 | 375.0 |
| 8 | 3.2 | 4060.0 | 25.7 | 1045.0 | 244.0 | 801.0 | 115.0 | 210.0 | 19.0 | 702.0 | 0.5053 | 355.0 |
| 9 | 3.0 | 4182.0 | 25.7 | 1077.0 | 234.0 | 843.0 | 121.0 | 216.0 | 18.0 | 722.0 | 0.4639 | 335.0 |
| 10 | 2.8 | 4297.0 | 25.7 | 1106.0 | 222.0 | 884.0 | 126.0 | 222.0 | 17.0 | 741.0 | 0.426 | 316.0 |
| 11 | 2.5 | 4405.0 | 25.7 | 1134.0 | 228.0 | 906.0 | 130.0 | 228.0 | 16.0 | 761.0 |  |  |

Year 11 is only used for the terminal value: its FCFF / (WACC - terminal growth).

## Base-case result

- PV of years 1-10 cash flows: 4,053
- Terminal value: 11,875; discounted: 5,059 (56% of enterprise value)
- Enterprise value: 9,112
- Equity value = EV - debt + cash: 9,550
- **Value per share: $70.71** vs price $71.05
- Sanity check: implied terminal EV/EBITDA 10.5x

## Scenarios (value per share)

- bear: $47.12
- base: $70.71
- bull: $114.46

## Reverse DCF

- Year-1 growth needed to justify $71.05: **5.1%** (10-year revenue CAGR 3.9%) vs base case 5.0% and 3-year history 42.2%

## Comparables

| Peer | EV/EBITDA | EV/Sales |
|---|---|---|
| SYK | 22.4 | 5.4 |
| ZBH | 12.6 | 3.4 |
| MDT | 15.8 | 4.1 |
| ISRG | 42.8 | 15.4 |

- EV/EBITDA: $87 - $157 (median $110)
- EV/Sales: $88 - $176 (median $107)

## Monte Carlo (10,000 runs)

- 10th / 50th / 90th percentile: $63 / $71 / $81
- P(value > price): 47%
- **Decision: HOLD**