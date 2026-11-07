# BDX: the 12 screening metrics, with workings

Valuation date 2026-11-06. Money in $ millions.

## Inputs

| Input | Value |
|---|---|
| Financial year used | 2025 (ended 30 Sep 2025) |
| Price date | 06 Nov 2026 |
| Share price ($) | 211.88 |
| Shares (m) | 285.4 |
| Market cap ($m) | 60471 |
| Enterprise value ($m) | 79003 |
| EBITDA ($m) | 5041 |
| Free cash flow ($m) | 2671 |
| Tax rate (pooled 3 yrs) | 11.4% |

## Risk-free rates (FRED)

| rate | value | basis |
|---|---|---|
| 3-month T-bill (Sharpe) | 4.33% | average 06 Nov 2023 – 05 Nov 2026 |
| 3-month T-bill, latest | 4.00% | as of 05 Nov 2026 |
| 10-year Treasury (DCF) | 4.84% | as of 05 Nov 2026 |

## Metrics

| Group | Metric | Workings | Result |
|---|---|---|---|
| Quality | ROIC | 2,579 x (1 - 11.4%) / (19,181 debt + 25,390 equity - 649 cash) | 5.2% |
| Quality | FCF margin | (3,431 op. cash flow - 760 capex) / 21,840 revenue | 12.2% |
| Quality | Net debt / EBITDA | (19,181 debt - 649 cash) / (2,579 op. income + 2,462 D&A) | 3.68x |
| Growth | Revenue growth (3-yr) | (21,840 revenue 2025 / 18,870 in 2022) ^ (1/3) - 1 | 5.0% |
| Growth | Operating profit growth (3-yr) | (2,579 op. income 2025 / 2,282 in 2022) ^ (1/3) - 1 | 4.2% |
| Value | EV / EBITDA | (60,471 market cap + 19,181 debt - 649 cash) / 5,041 EBITDA | 15.67x |
| Value | FCF yield | 2,671 FCF / 60,471 market cap ($211.88 x 285.4m shares) | 4.4% |
| Momentum | 12-1 month return | $180.30 (06 Oct 2026) / $136.06 (06 Nov 2025) - 1 | 32.5% |
| Momentum | Return vs sector (12m) | BDX 55.7% minus IHI -4.6% (12 months to 06 Nov 2026) | 60.4% |
| Risk | Volatility | std. dev. of 753 daily returns (1.63%) x sqrt(252) | 25.9% |
| Risk | Beta | covariance / variance of 156 weekly returns, BDX vs SPY | 0.28 |
| Risk | Max drawdown | $125.23 (06 May 2025) / $191.53 peak (06 Nov 2023) - 1 | -34.6% |
| Reported only | Sharpe ratio | (3.4% yearly return - 4.3% T-bill) / 25.9% volatility | -0.03 |

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

- None: every item found under its preferred label.