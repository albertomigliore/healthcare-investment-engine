# EW: the 12 screening metrics, with workings

Valuation date 2026-11-06. Money in $ millions.

## Inputs

| Input | Value |
|---|---|
| Financial year used | 2025 (ended 31 Dec 2025) |
| Price date | 06 Nov 2026 |
| Share price ($) | 102.14 |
| Shares (m) | 580.7 |
| Market cap ($m) | 59313 |
| Enterprise value ($m) | 55792 |
| EBITDA ($m) | 1421 |
| Free cash flow ($m) | 1335 |
| Tax rate (pooled 3 yrs) | 12.4% |

## Risk-free rates (FRED)

| rate | value | basis |
|---|---|---|
| 3-month T-bill (Sharpe) | 4.33% | average 06 Nov 2023 – 05 Nov 2026 |
| 3-month T-bill, latest | 4.00% | as of 05 Nov 2026 |
| 10-year Treasury (DCF) | 4.84% | as of 05 Nov 2026 |

## Metrics

| Group | Metric | Workings | Result |
|---|---|---|---|
| Quality | ROIC | 1,264 x (1 - 12.4%) / (705 debt + 10,338 equity - 4,226 cash) | 16.2% |
| Quality | FCF margin | (1,595 op. cash flow - 260 capex) / 6,068 revenue | 22.0% |
| Quality | Net debt / EBITDA | (705 debt - 4,226 cash) / (1,264 op. income + 157 D&A) | -2.48x |
| Growth | Revenue growth (3-yr) | (6,068 revenue 2025 / 4,464 in 2022) ^ (1/3) - 1 | 10.8% |
| Growth | Operating profit growth (3-yr) | (1,264 op. income 2025 / 1,498 in 2022) ^ (1/3) - 1 | -5.5% |
| Value | EV / EBITDA | (59,313 market cap + 705 debt - 4,226 cash) / 1,421 EBITDA | 39.27x |
| Value | FCF yield | 1,335 FCF / 59,313 market cap ($102.14 x 580.7m shares) | 2.3% |
| Momentum | 12-1 month return | $86.48 (06 Oct 2026) / $82.44 (06 Nov 2025) - 1 | 4.9% |
| Momentum | Return vs sector (12m) | EW 23.9% minus IHI -4.6% (12 months to 06 Nov 2026) | 28.5% |
| Risk | Volatility | std. dev. of 753 daily returns (1.98%) x sqrt(252) | 31.5% |
| Risk | Beta | covariance / variance of 156 weekly returns, EW vs SPY | 0.62 |
| Risk | Max drawdown | $59.70 (25 Jul 2024) / $95.56 peak (28 Mar 2024) - 1 | -37.5% |
| Reported only | Sharpe ratio | (15.0% yearly return - 4.3% T-bill) / 31.5% volatility | 0.34 |

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