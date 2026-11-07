# ALGN: the 12 screening metrics, with workings

Valuation date 2026-11-06. Money in $ millions.

## Inputs

| Input | Value |
|---|---|
| Financial year used | 2025 (ended 31 Dec 2025) |
| Price date | 06 Nov 2026 |
| Share price ($) | 166.0 |
| Shares (m) | 71.4 |
| Market cap ($m) | 11846 |
| Enterprise value ($m) | 10866 |
| EBITDA ($m) | 783 |
| Free cash flow ($m) | 491 |
| Tax rate (pooled 3 yrs) | 30.4% |

## Risk-free rates (FRED)

| rate | value | basis |
|---|---|---|
| 3-month T-bill (Sharpe) | 4.33% | average 06 Nov 2023 – 05 Nov 2026 |
| 3-month T-bill, latest | 4.00% | as of 05 Nov 2026 |
| 10-year Treasury (DCF) | 4.84% | as of 05 Nov 2026 |

## Metrics

| Group | Metric | Workings | Result |
|---|---|---|---|
| Quality | ROIC | 546 x (1 - 30.4%) / (114 debt + 4,049 equity - 1,095 cash) | 12.4% |
| Quality | FCF margin | (593 op. cash flow - 102 capex) / 4,035 revenue | 12.2% |
| Quality | Net debt / EBITDA | (114 debt - 1,095 cash) / (546 op. income + 237 D&A) | -1.25x |
| Growth | Revenue growth (3-yr) | (4,035 revenue 2025 / 3,735 in 2022) ^ (1/3) - 1 | 2.6% |
| Growth | Operating profit growth (3-yr) | (546 op. income 2025 / 643 in 2022) ^ (1/3) - 1 | -5.3% |
| Value | EV / EBITDA | (11,846 market cap + 114 debt - 1,095 cash) / 783 EBITDA | 13.87x |
| Value | FCF yield | 491 FCF / 11,846 market cap ($166.00 x 71.4m shares) | 4.1% |
| Momentum | 12-1 month return | $141.45 (06 Oct 2026) / $133.73 (06 Nov 2025) - 1 | 5.8% |
| Momentum | Return vs sector (12m) | ALGN 24.1% minus IHI -4.6% (12 months to 06 Nov 2026) | 28.8% |
| Risk | Volatility | std. dev. of 753 daily returns (2.80%) x sqrt(252) | 44.5% |
| Risk | Beta | covariance / variance of 156 weekly returns, ALGN vs SPY | 1.31 |
| Risk | Max drawdown | $124.88 (25 Sep 2025) / $330.25 peak (09 Apr 2024) - 1 | -62.2% |
| Reported only | Sharpe ratio | (-5.7% yearly return - 4.3% T-bill) / 44.5% volatility | -0.22 |

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