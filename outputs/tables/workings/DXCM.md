# DXCM: the 12 screening metrics, with workings

Valuation date 2026-11-06. Money in $ millions.

## Inputs

| Input | Value |
|---|---|
| Financial year used | 2025 (ended 31 Dec 2025) |
| Price date | 06 Nov 2026 |
| Share price ($) | 79.41 |
| Shares (m) | 384.8 |
| Market cap ($m) | 30557 |
| Enterprise value ($m) | 29948 |
| EBITDA ($m) | 1164 |
| Free cash flow ($m) | 1077 |
| Tax rate (pooled 3 yrs) | 22.1% |

## Risk-free rates (FRED)

| rate | value | basis |
|---|---|---|
| 3-month T-bill (Sharpe) | 4.33% | average 06 Nov 2023 – 05 Nov 2026 |
| 3-month T-bill, latest | 4.00% | as of 05 Nov 2026 |
| 10-year Treasury (DCF) | 4.84% | as of 05 Nov 2026 |

## Metrics

| Group | Metric | Workings | Result |
|---|---|---|---|
| Quality | ROIC | 912 x (1 - 22.1%) / (1,390 debt + 2,746 equity - 1,999 cash) | 33.2% |
| Quality | FCF margin | (1,441 op. cash flow - 364 capex) / 4,662 revenue | 23.1% |
| Quality | Net debt / EBITDA | (1,390 debt - 1,999 cash) / (912 op. income + 252 D&A) | -0.52x |
| Growth | Revenue growth (3-yr) | (4,662 revenue 2025 / 2,910 in 2022) ^ (1/3) - 1 | 17.0% |
| Growth | Operating profit growth (3-yr) | (912 op. income 2025 / 391 in 2022) ^ (1/3) - 1 | 32.6% |
| Value | EV / EBITDA | (30,557 market cap + 1,390 debt - 1,999 cash) / 1,164 EBITDA | 25.74x |
| Value | FCF yield | 1,077 FCF / 30,557 market cap ($79.41 x 384.8m shares) | 3.5% |
| Momentum | 12-1 month return | $83.39 (06 Oct 2026) / $58.02 (06 Nov 2025) - 1 | 43.7% |
| Momentum | Return vs sector (12m) | DXCM 36.9% minus IHI -4.6% (12 months to 06 Nov 2026) | 41.5% |
| Risk | Volatility | std. dev. of 753 daily returns (2.93%) x sqrt(252) | 46.6% |
| Risk | Beta | covariance / variance of 156 weekly returns, DXCM vs SPY | 1.07 |
| Risk | Max drawdown | $54.84 (10 Nov 2025) / $140.45 peak (09 Apr 2024) - 1 | -61.0% |
| Reported only | Sharpe ratio | (-5.7% yearly return - 4.3% T-bill) / 46.6% volatility | -0.22 |

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