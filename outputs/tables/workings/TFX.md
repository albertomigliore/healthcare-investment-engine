# TFX: the 12 screening metrics, with workings

Valuation date 2026-11-06. Money in $ millions.

## Inputs

| Input | Value |
|---|---|
| Financial year used | 2025 (ended 31 Dec 2025) |
| Price date | 06 Nov 2026 |
| Share price ($) | 150.87 |
| Shares (m) | 44.2 |
| Market cap ($m) | 6668 |
| Enterprise value ($m) | 9015 |
| EBITDA ($m) | 296 |
| Free cash flow ($m) | 245 |
| Tax rate (pooled 3 yrs) | 0.0% |

## Risk-free rates (FRED)

| rate | value | basis |
|---|---|---|
| 3-month T-bill (Sharpe) | 4.33% | average 06 Nov 2023 – 05 Nov 2026 |
| 3-month T-bill, latest | 4.00% | as of 05 Nov 2026 |
| 10-year Treasury (DCF) | 4.84% | as of 05 Nov 2026 |

## Metrics

| Group | Metric | Workings | Result |
|---|---|---|---|
| Quality | ROIC | 118 x (1 - 0.0%) / (2,726 debt + 3,125 equity - 379 cash) | 2.2% |
| Quality | FCF margin | (341 op. cash flow - 95 capex) / 1,993 revenue | 12.3% |
| Quality | Net debt / EBITDA | (2,726 debt - 379 cash) / (118 op. income + 178 D&A) | 7.93x |
| Growth | Revenue growth (3-yr) | (1,993 revenue 2025 / 1,712 in 2023) ^ (1/2) - 1 | 7.9% |
| Growth | Operating profit growth (3-yr) | (118 op. income 2025 / 259 in 2023) ^ (1/2) - 1 | -32.4% |
| Value | EV / EBITDA | (6,668 market cap + 2,726 debt - 379 cash) / 296 EBITDA | 30.44x |
| Value | FCF yield | 245 FCF / 6,668 market cap ($150.87 x 44.2m shares) | 3.7% |
| Momentum | 12-1 month return | $124.74 (06 Oct 2026) / $107.32 (06 Nov 2025) - 1 | 16.2% |
| Momentum | Return vs sector (12m) | TFX 40.6% minus IHI -4.6% (12 months to 06 Nov 2026) | 45.2% |
| Risk | Volatility | std. dev. of 753 daily returns (2.26%) x sqrt(252) | 35.8% |
| Risk | Beta | covariance / variance of 156 weekly returns, TFX vs SPY | 0.52 |
| Risk | Max drawdown | $99.54 (20 Jan 2026) / $249.78 peak (14 Dec 2023) - 1 | -60.1% |
| Reported only | Sharpe ratio | (-10.1% yearly return - 4.3% T-bill) / 35.8% volatility | -0.40 |

## Yahoo labels used

| Item | Yahoo label |
|---|---|
| revenue | Total Revenue |
| operating_income | Total Operating Income As Reported |
| pretax_income | Pretax Income |
| tax | Tax Provision |
| depreciation_amortisation | Depreciation And Amortization |
| operating_cash_flow | Operating Cash Flow |
| capital_expenditure | Capital Expenditure |
| total_debt | Total Debt |
| cash | Cash Cash Equivalents And Short Term Investments |
| equity | Stockholders Equity |
| shares | Ordinary Shares Number |

## Data flags

- growth measured over 2 years (2023-2025): later years were restated after a divestiture, but 2022 was never restated, so it is not like-for-like