# ABT: the 12 screening metrics, with workings

Valuation date 2026-11-06. Money in $ millions.

## Inputs

| Input | Value |
|---|---|
| Financial year used | 2025 (ended 31 Dec 2025) |
| Price date | 06 Nov 2026 |
| Share price ($) | 109.93 |
| Shares (m) | 1736.6 |
| Market cap ($m) | 190904 |
| Enterprise value ($m) | 195825 |
| EBITDA ($m) | 11169 |
| Free cash flow ($m) | 7395 |
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
| Quality | ROIC | 8,053 x (1 - 0.0%) / (13,860 debt + 52,130 equity - 8,939 cash) | 14.1% |
| Quality | FCF margin | (9,566 op. cash flow - 2,171 capex) / 44,328 revenue | 16.7% |
| Quality | Net debt / EBITDA | (13,860 debt - 8,939 cash) / (8,053 op. income + 3,116 D&A) | 0.44x |
| Growth | Revenue growth (3-yr) | (44,328 revenue 2025 / 43,653 in 2022) ^ (1/3) - 1 | 0.5% |
| Growth | Operating profit growth (3-yr) | (8,053 op. income 2025 / 8,362 in 2022) ^ (1/3) - 1 | -1.2% |
| Value | EV / EBITDA | (190,904 market cap + 13,860 debt - 8,939 cash) / 11,169 EBITDA | 17.53x |
| Value | FCF yield | 7,395 FCF / 190,904 market cap ($109.93 x 1736.6m shares) | 3.9% |
| Momentum | 12-1 month return | $97.56 (06 Oct 2026) / $121.92 (06 Nov 2025) - 1 | -20.0% |
| Momentum | Return vs sector (12m) | ABT -9.8% minus IHI -4.6% (12 months to 06 Nov 2026) | -5.2% |
| Risk | Volatility | std. dev. of 753 daily returns (1.45%) x sqrt(252) | 23.0% |
| Risk | Beta | covariance / variance of 156 weekly returns, ABT vs SPY | 0.11 |
| Risk | Max drawdown | $81.47 (11 May 2026) / $134.98 peak (03 Mar 2025) - 1 | -39.6% |
| Reported only | Sharpe ratio | (7.2% yearly return - 4.3% T-bill) / 23.0% volatility | 0.13 |

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