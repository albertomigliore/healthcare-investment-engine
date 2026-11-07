# GEHC: the 12 screening metrics, with workings

Valuation date 2026-11-06. Money in $ millions.

## Inputs

| Input | Value |
|---|---|
| Financial year used | 2025 (ended 31 Dec 2025) |
| Price date | 06 Nov 2026 |
| Share price ($) | 82.38 |
| Shares (m) | 455.7 |
| Market cap ($m) | 37544 |
| Enterprise value ($m) | 43515 |
| EBITDA ($m) | 3341 |
| Free cash flow ($m) | 1505 |
| Tax rate (pooled 3 yrs) | 24.5% |

## Risk-free rates (FRED)

| rate | value | basis |
|---|---|---|
| 3-month T-bill (Sharpe) | 4.33% | average 06 Nov 2023 – 05 Nov 2026 |
| 3-month T-bill, latest | 4.00% | as of 05 Nov 2026 |
| 10-year Treasury (DCF) | 4.84% | as of 05 Nov 2026 |

## Metrics

| Group | Metric | Workings | Result |
|---|---|---|---|
| Quality | ROIC | 2,763 x (1 - 24.5%) / (10,463 debt + 10,379 equity - 4,492 cash) | 12.8% |
| Quality | FCF margin | (1,987 op. cash flow - 482 capex) / 20,625 revenue | 7.3% |
| Quality | Net debt / EBITDA | (10,463 debt - 4,492 cash) / (2,763 op. income + 578 D&A) | 1.79x |
| Growth | Revenue growth (3-yr) | (20,625 revenue 2025 / 18,341 in 2022) ^ (1/3) - 1 | 4.0% |
| Growth | Operating profit growth (3-yr) | (2,763 op. income 2025 / 2,522 in 2022) ^ (1/3) - 1 | 3.1% |
| Value | EV / EBITDA | (37,544 market cap + 10,463 debt - 4,492 cash) / 3,341 EBITDA | 13.02x |
| Value | FCF yield | 1,505 FCF / 37,544 market cap ($82.38 x 455.7m shares) | 4.0% |
| Momentum | 12-1 month return | $64.73 (06 Oct 2026) / $74.02 (06 Nov 2025) - 1 | -12.5% |
| Momentum | Return vs sector (12m) | GEHC 11.3% minus IHI -4.6% (12 months to 06 Nov 2026) | 15.9% |
| Risk | Volatility | std. dev. of 753 daily returns (2.12%) x sqrt(252) | 33.7% |
| Risk | Beta | covariance / variance of 156 weekly returns, GEHC vs SPY | 1.09 |
| Risk | Max drawdown | $58.55 (08 Apr 2025) / $93.46 peak (30 Sep 2024) - 1 | -37.4% |
| Reported only | Sharpe ratio | (5.2% yearly return - 4.3% T-bill) / 33.7% volatility | 0.03 |

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