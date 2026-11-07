# GMED: the 12 screening metrics, with workings

Valuation date 2026-11-06. Money in $ millions.

## Inputs

| Input | Value |
|---|---|
| Financial year used | 2025 (ended 31 Dec 2025) |
| Price date | 06 Nov 2026 |
| Share price ($) | 71.05 |
| Shares (m) | 135.1 |
| Market cap ($m) | 9596 |
| Enterprise value ($m) | 9157 |
| EBITDA ($m) | 757 |
| Free cash flow ($m) | 579 |
| Tax rate (pooled 3 yrs) | 14.3% |

## Risk-free rates (FRED)

| rate | value | basis |
|---|---|---|
| 3-month T-bill (Sharpe) | 4.33% | average 06 Nov 2023 – 05 Nov 2026 |
| 3-month T-bill, latest | 4.00% | as of 05 Nov 2026 |
| 10-year Treasury (DCF) | 4.84% | as of 05 Nov 2026 |

## Metrics

| Group | Metric | Workings | Result |
|---|---|---|---|
| Quality | ROIC | 480 x (1 - 14.3%) / (119 debt + 4,573 equity - 557 cash) | 9.9% |
| Quality | FCF margin | (753 op. cash flow - 174 capex) / 2,939 revenue | 19.7% |
| Quality | Net debt / EBITDA | (119 debt - 557 cash) / (480 op. income + 277 D&A) | -0.58x |
| Growth | Revenue growth (3-yr) | (2,939 revenue 2025 / 1,023 in 2022) ^ (1/3) - 1 | 42.2% |
| Growth | Operating profit growth (3-yr) | (480 op. income 2025 / 228 in 2022) ^ (1/3) - 1 | 28.2% |
| Value | EV / EBITDA | (9,596 market cap + 119 debt - 557 cash) / 757 EBITDA | 12.10x |
| Value | FCF yield | 579 FCF / 9,596 market cap ($71.05 x 135.1m shares) | 6.0% |
| Momentum | 12-1 month return | $76.43 (06 Oct 2026) / $61.71 (06 Nov 2025) - 1 | 23.9% |
| Momentum | Return vs sector (12m) | GMED 15.1% minus IHI -4.6% (12 months to 06 Nov 2026) | 19.8% |
| Risk | Volatility | std. dev. of 753 daily returns (2.66%) x sqrt(252) | 42.2% |
| Risk | Beta | covariance / variance of 156 weekly returns, GMED vs SPY | 0.74 |
| Risk | Max drawdown | $51.89 (21 Jul 2025) / $93.32 peak (22 Jan 2025) - 1 | -44.4% |
| Reported only | Sharpe ratio | (15.2% yearly return - 4.3% T-bill) / 42.2% volatility | 0.26 |

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