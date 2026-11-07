# PODD: the 12 screening metrics, with workings

Valuation date 2026-11-06. Money in $ millions.

## Inputs

| Input | Value |
|---|---|
| Financial year used | 2025 (ended 31 Dec 2025) |
| Price date | 06 Nov 2026 |
| Share price ($) | 146.51 |
| Shares (m) | 70.4 |
| Market cap ($m) | 10313 |
| Enterprise value ($m) | 10546 |
| EBITDA ($m) | 564 |
| Free cash flow ($m) | 350 |
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
| Quality | ROIC | 474 x (1 - 0.0%) / (949 debt + 1,515 equity - 716 cash) | 27.1% |
| Quality | FCF margin | (569 op. cash flow - 219 capex) / 2,708 revenue | 12.9% |
| Quality | Net debt / EBITDA | (949 debt - 716 cash) / (474 op. income + 90 D&A) | 0.41x |
| Growth | Revenue growth (3-yr) | (2,708 revenue 2025 / 1,305 in 2022) ^ (1/3) - 1 | 27.5% |
| Growth | Operating profit growth (3-yr) | (474 op. income 2025 / 38 in 2022) ^ (1/3) - 1 | 132.7% |
| Value | EV / EBITDA | (10,313 market cap + 949 debt - 716 cash) / 564 EBITDA | 18.69x |
| Value | FCF yield | 350 FCF / 10,313 market cap ($146.51 x 70.4m shares) | 3.4% |
| Momentum | 12-1 month return | $134.73 (06 Oct 2026) / $323.40 (06 Nov 2025) - 1 | -58.3% |
| Momentum | Return vs sector (12m) | PODD -54.7% minus IHI -4.6% (12 months to 06 Nov 2026) | -50.1% |
| Risk | Volatility | std. dev. of 753 daily returns (2.57%) x sqrt(252) | 40.8% |
| Risk | Beta | covariance / variance of 156 weekly returns, PODD vs SPY | 0.46 |
| Risk | Max drawdown | $130.47 (30 Sep 2026) / $352.82 peak (09 Sep 2025) - 1 | -63.0% |
| Reported only | Sharpe ratio | (-2.7% yearly return - 4.3% T-bill) / 40.8% volatility | -0.17 |

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