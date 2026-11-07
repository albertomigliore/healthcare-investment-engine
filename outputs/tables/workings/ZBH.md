# ZBH: the 12 screening metrics, with workings

Valuation date 2026-11-06. Money in $ millions.

## Inputs

| Input | Value |
|---|---|
| Financial year used | 2025 (ended 31 Dec 2025) |
| Price date | 06 Nov 2026 |
| Share price ($) | 105.59 |
| Shares (m) | 195.5 |
| Market cap ($m) | 20641 |
| Enterprise value ($m) | 27568 |
| EBITDA ($m) | 2192 |
| Free cash flow ($m) | 1420 |
| Tax rate (pooled 3 yrs) | 10.2% |

## Risk-free rates (FRED)

| rate | value | basis |
|---|---|---|
| 3-month T-bill (Sharpe) | 4.33% | average 06 Nov 2023 – 05 Nov 2026 |
| 3-month T-bill, latest | 4.00% | as of 05 Nov 2026 |
| 10-year Treasury (DCF) | 4.84% | as of 05 Nov 2026 |

## Metrics

| Group | Metric | Workings | Result |
|---|---|---|---|
| Quality | ROIC | 1,098 x (1 - 10.2%) / (7,519 debt + 12,698 equity - 592 cash) | 5.0% |
| Quality | FCF margin | (1,697 op. cash flow - 277 capex) / 8,232 revenue | 17.3% |
| Quality | Net debt / EBITDA | (7,519 debt - 592 cash) / (1,098 op. income + 1,094 D&A) | 3.16x |
| Growth | Revenue growth (3-yr) | (8,232 revenue 2025 / 6,940 in 2022) ^ (1/3) - 1 | 5.9% |
| Growth | Operating profit growth (3-yr) | (1,098 op. income 2025 / 696 in 2022) ^ (1/3) - 1 | 16.4% |
| Value | EV / EBITDA | (20,641 market cap + 7,519 debt - 592 cash) / 2,192 EBITDA | 12.58x |
| Value | FCF yield | 1,420 FCF / 20,641 market cap ($105.59 x 195.5m shares) | 6.9% |
| Momentum | 12-1 month return | $89.68 (06 Oct 2026) / $87.57 (06 Nov 2025) - 1 | 2.4% |
| Momentum | Return vs sector (12m) | ZBH 20.6% minus IHI -4.6% (12 months to 06 Nov 2026) | 25.2% |
| Risk | Volatility | std. dev. of 753 daily returns (1.79%) x sqrt(252) | 28.4% |
| Risk | Beta | covariance / variance of 156 weekly returns, ZBH vs SPY | 0.39 |
| Risk | Max drawdown | $79.16 (11 May 2026) / $129.40 peak (27 Mar 2024) - 1 | -38.8% |
| Reported only | Sharpe ratio | (-0.2% yearly return - 4.3% T-bill) / 28.4% volatility | -0.16 |

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