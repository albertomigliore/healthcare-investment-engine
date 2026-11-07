# RMD: the 12 screening metrics, with workings

Valuation date 2026-11-06. Money in $ millions.

## Inputs

| Input | Value |
|---|---|
| Financial year used | 2026 (ended 30 Jun 2026) |
| Price date | 06 Nov 2026 |
| Share price ($) | 235.3 |
| Shares (m) | 144.2 |
| Market cap ($m) | 33940 |
| Enterprise value ($m) | 33296 |
| EBITDA ($m) | 2131 |
| Free cash flow ($m) | 1629 |
| Tax rate (pooled 3 yrs) | 18.9% |

## Risk-free rates (FRED)

| rate | value | basis |
|---|---|---|
| 3-month T-bill (Sharpe) | 4.33% | average 06 Nov 2023 – 05 Nov 2026 |
| 3-month T-bill, latest | 4.00% | as of 05 Nov 2026 |
| 10-year Treasury (DCF) | 4.84% | as of 05 Nov 2026 |

## Metrics

| Group | Metric | Workings | Result |
|---|---|---|---|
| Quality | ROIC | 1,887 x (1 - 18.9%) / (826 debt + 6,585 equity - 1,469 cash) | 25.8% |
| Quality | FCF margin | (1,806 op. cash flow - 177 capex) / 5,653 revenue | 28.8% |
| Quality | Net debt / EBITDA | (826 debt - 1,469 cash) / (1,887 op. income + 244 D&A) | -0.30x |
| Growth | Revenue growth (3-yr) | (5,653 revenue 2026 / 4,223 in 2023) ^ (1/3) - 1 | 10.2% |
| Growth | Operating profit growth (3-yr) | (1,887 op. income 2026 / 1,132 in 2023) ^ (1/3) - 1 | 18.6% |
| Value | EV / EBITDA | (33,940 market cap + 826 debt - 1,469 cash) / 2,131 EBITDA | 15.63x |
| Value | FCF yield | 1,629 FCF / 33,940 market cap ($235.30 x 144.2m shares) | 4.8% |
| Momentum | 12-1 month return | $220.69 (06 Oct 2026) / $247.04 (06 Nov 2025) - 1 | -10.7% |
| Momentum | Return vs sector (12m) | RMD -4.8% minus IHI -4.6% (12 months to 06 Nov 2026) | -0.1% |
| Risk | Volatility | std. dev. of 753 daily returns (2.01%) x sqrt(252) | 31.9% |
| Risk | Beta | covariance / variance of 156 weekly returns, RMD vs SPY | 0.67 |
| Risk | Max drawdown | $182.30 (02 Jun 2026) / $290.65 peak (22 Aug 2025) - 1 | -37.3% |
| Reported only | Sharpe ratio | (16.3% yearly return - 4.3% T-bill) / 31.9% volatility | 0.38 |

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