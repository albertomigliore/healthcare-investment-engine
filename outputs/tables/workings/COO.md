# COO: the 12 screening metrics, with workings

Valuation date 2026-11-06. Money in $ millions.

## Inputs

| Input | Value |
|---|---|
| Financial year used | 2025 (ended 31 Oct 2025) |
| Price date | 06 Nov 2026 |
| Share price ($) | 62.36 |
| Shares (m) | 195.9 |
| Market cap ($m) | 12216 |
| Enterprise value ($m) | 14611 |
| EBITDA ($m) | 1060 |
| Free cash flow ($m) | 434 |
| Tax rate (pooled 3 yrs) | 32.0% |

## Risk-free rates (FRED)

| rate | value | basis |
|---|---|---|
| 3-month T-bill (Sharpe) | 4.33% | average 06 Nov 2023 – 05 Nov 2026 |
| 3-month T-bill, latest | 4.00% | as of 05 Nov 2026 |
| 10-year Treasury (DCF) | 4.84% | as of 05 Nov 2026 |

## Metrics

| Group | Metric | Workings | Result |
|---|---|---|---|
| Quality | ROIC | 683 x (1 - 32.0%) / (2,505 debt + 8,239 equity - 111 cash) | 4.4% |
| Quality | FCF margin | (796 op. cash flow - 362 capex) / 4,092 revenue | 10.6% |
| Quality | Net debt / EBITDA | (2,505 debt - 111 cash) / (683 op. income + 377 D&A) | 2.26x |
| Growth | Revenue growth (3-yr) | (4,092 revenue 2025 / 3,308 in 2022) ^ (1/3) - 1 | 7.3% |
| Growth | Operating profit growth (3-yr) | (683 op. income 2025 / 508 in 2022) ^ (1/3) - 1 | 10.4% |
| Value | EV / EBITDA | (12,216 market cap + 2,505 debt - 111 cash) / 1,060 EBITDA | 13.78x |
| Value | FCF yield | 434 FCF / 12,216 market cap ($62.36 x 195.9m shares) | 3.6% |
| Momentum | 12-1 month return | $56.43 (06 Oct 2026) / $69.00 (06 Nov 2025) - 1 | -18.2% |
| Momentum | Return vs sector (12m) | COO -9.6% minus IHI -4.6% (12 months to 06 Nov 2026) | -5.0% |
| Risk | Volatility | std. dev. of 753 daily returns (1.98%) x sqrt(252) | 31.5% |
| Risk | Beta | covariance / variance of 156 weekly returns, COO vs SPY | 0.57 |
| Risk | Max drawdown | $53.27 (15 Sep 2026) / $111.23 peak (16 Sep 2024) - 1 | -52.1% |
| Reported only | Sharpe ratio | (-9.3% yearly return - 4.3% T-bill) / 31.5% volatility | -0.43 |

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