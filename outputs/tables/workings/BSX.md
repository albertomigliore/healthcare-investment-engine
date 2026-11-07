# BSX: the 12 screening metrics, with workings

Valuation date 2026-11-06. Money in $ millions.

## Inputs

| Input | Value |
|---|---|
| Financial year used | 2025 (ended 31 Dec 2025) |
| Price date | 06 Nov 2026 |
| Share price ($) | 42.75 |
| Shares (m) | 1483.0 |
| Market cap ($m) | 63398 |
| Enterprise value ($m) | 72869 |
| EBITDA ($m) | 4981 |
| Free cash flow ($m) | 3404 |
| Tax rate (pooled 3 yrs) | 17.3% |

## Risk-free rates (FRED)

| rate | value | basis |
|---|---|---|
| 3-month T-bill (Sharpe) | 4.33% | average 06 Nov 2023 – 05 Nov 2026 |
| 3-month T-bill, latest | 4.00% | as of 05 Nov 2026 |
| 10-year Treasury (DCF) | 4.84% | as of 05 Nov 2026 |

## Metrics

| Group | Metric | Workings | Result |
|---|---|---|---|
| Quality | ROIC | 3,613 x (1 - 17.3%) / (11,436 debt + 24,232 equity - 1,965 cash) | 8.9% |
| Quality | FCF margin | (4,534 op. cash flow - 1,130 capex) / 20,074 revenue | 17.0% |
| Quality | Net debt / EBITDA | (11,436 debt - 1,965 cash) / (3,613 op. income + 1,368 D&A) | 1.90x |
| Growth | Revenue growth (3-yr) | (20,074 revenue 2025 / 12,682 in 2022) ^ (1/3) - 1 | 16.5% |
| Growth | Operating profit growth (3-yr) | (3,613 op. income 2025 / 1,649 in 2022) ^ (1/3) - 1 | 29.9% |
| Value | EV / EBITDA | (63,398 market cap + 11,436 debt - 1,965 cash) / 4,981 EBITDA | 14.63x |
| Value | FCF yield | 3,404 FCF / 63,398 market cap ($42.75 x 1483.0m shares) | 5.4% |
| Momentum | 12-1 month return | $42.19 (06 Oct 2026) / $99.05 (06 Nov 2025) - 1 | -57.4% |
| Momentum | Return vs sector (12m) | BSX -56.8% minus IHI -4.6% (12 months to 06 Nov 2026) | -52.2% |
| Risk | Volatility | std. dev. of 753 daily returns (1.80%) x sqrt(252) | 28.6% |
| Risk | Beta | covariance / variance of 156 weekly returns, BSX vs SPY | 0.73 |
| Risk | Max drawdown | $41.58 (07 Oct 2026) / $108.14 peak (08 Sep 2025) - 1 | -61.5% |
| Reported only | Sharpe ratio | (-6.8% yearly return - 4.3% T-bill) / 28.6% volatility | -0.39 |

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