# MDT: the 12 screening metrics, with workings

Valuation date 2026-11-06. Money in $ millions.

## Inputs

| Input | Value |
|---|---|
| Financial year used | 2026 (ended 30 Apr 2026) |
| Price date | 06 Nov 2026 |
| Share price ($) | 101.8 |
| Shares (m) | 1280.2 |
| Market cap ($m) | 130322 |
| Enterprise value ($m) | 149063 |
| EBITDA ($m) | 9425 |
| Free cash flow ($m) | 5426 |
| Tax rate (pooled 3 yrs) | 20.3% |

## Risk-free rates (FRED)

| rate | value | basis |
|---|---|---|
| 3-month T-bill (Sharpe) | 4.33% | average 06 Nov 2023 – 05 Nov 2026 |
| 3-month T-bill, latest | 4.00% | as of 05 Nov 2026 |
| 10-year Treasury (DCF) | 4.84% | as of 05 Nov 2026 |

## Metrics

| Group | Metric | Workings | Result |
|---|---|---|---|
| Quality | ROIC | 6,467 x (1 - 20.3%) / (27,961 debt + 49,463 equity - 9,220 cash) | 7.6% |
| Quality | FCF margin | (7,330 op. cash flow - 1,904 capex) / 36,364 revenue | 14.9% |
| Quality | Net debt / EBITDA | (27,961 debt - 9,220 cash) / (6,467 op. income + 2,958 D&A) | 1.99x |
| Growth | Revenue growth (3-yr) | (36,364 revenue 2026 / 31,227 in 2023) ^ (1/3) - 1 | 5.2% |
| Growth | Operating profit growth (3-yr) | (6,467 op. income 2026 / 5,485 in 2023) ^ (1/3) - 1 | 5.6% |
| Value | EV / EBITDA | (130,322 market cap + 27,961 debt - 9,220 cash) / 9,425 EBITDA | 15.82x |
| Value | FCF yield | 5,426 FCF / 130,322 market cap ($101.80 x 1280.2m shares) | 4.2% |
| Momentum | 12-1 month return | $87.09 (06 Oct 2026) / $87.17 (06 Nov 2025) - 1 | -0.1% |
| Momentum | Return vs sector (12m) | MDT 16.8% minus IHI -4.6% (12 months to 06 Nov 2026) | 21.4% |
| Risk | Volatility | std. dev. of 753 daily returns (1.38%) x sqrt(252) | 22.0% |
| Risk | Beta | covariance / variance of 156 weekly returns, MDT vs SPY | 0.27 |
| Risk | Max drawdown | $72.50 (02 Jun 2026) / $101.97 peak (25 Nov 2025) - 1 | -28.9% |
| Reported only | Sharpe ratio | (15.2% yearly return - 4.3% T-bill) / 22.0% volatility | 0.50 |

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