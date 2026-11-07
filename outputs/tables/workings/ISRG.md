# ISRG: the 12 screening metrics, with workings

Valuation date 2026-11-06. Money in $ millions.

## Inputs

| Input | Value |
|---|---|
| Financial year used | 2025 (ended 31 Dec 2025) |
| Price date | 06 Nov 2026 |
| Share price ($) | 452.8 |
| Shares (m) | 355.1 |
| Market cap ($m) | 160789 |
| Enterprise value ($m) | 154854 |
| EBITDA ($m) | 3623 |
| Free cash flow ($m) | 2491 |
| Tax rate (pooled 3 yrs) | 11.5% |

## Risk-free rates (FRED)

| rate | value | basis |
|---|---|---|
| 3-month T-bill (Sharpe) | 4.33% | average 06 Nov 2023 – 05 Nov 2026 |
| 3-month T-bill, latest | 4.00% | as of 05 Nov 2026 |
| 10-year Treasury (DCF) | 4.84% | as of 05 Nov 2026 |

## Metrics

| Group | Metric | Workings | Result |
|---|---|---|---|
| Quality | ROIC | 2,946 x (1 - 11.5%) / (0 debt + 17,824 equity - 5,935 cash) | 21.9% |
| Quality | FCF margin | (3,030 op. cash flow - 540 capex) / 10,065 revenue | 24.7% |
| Quality | Net debt / EBITDA | (0 debt - 5,935 cash) / (2,946 op. income + 677 D&A) | -1.64x |
| Growth | Revenue growth (3-yr) | (10,065 revenue 2025 / 6,222 in 2022) ^ (1/3) - 1 | 17.4% |
| Growth | Operating profit growth (3-yr) | (2,946 op. income 2025 / 1,577 in 2022) ^ (1/3) - 1 | 23.1% |
| Value | EV / EBITDA | (160,789 market cap + 0 debt - 5,935 cash) / 3,623 EBITDA | 42.75x |
| Value | FCF yield | 2,491 FCF / 160,789 market cap ($452.80 x 355.1m shares) | 1.5% |
| Momentum | 12-1 month return | $404.76 (06 Oct 2026) / $547.78 (06 Nov 2025) - 1 | -26.1% |
| Momentum | Return vs sector (12m) | ISRG -17.3% minus IHI -4.6% (12 months to 06 Nov 2026) | -12.7% |
| Risk | Volatility | std. dev. of 753 daily returns (2.08%) x sqrt(252) | 33.1% |
| Risk | Beta | covariance / variance of 156 weekly returns, ISRG vs SPY | 1.16 |
| Risk | Max drawdown | $332.02 (23 Jul 2026) / $610.45 peak (22 Jan 2025) - 1 | -45.6% |
| Reported only | Sharpe ratio | (17.8% yearly return - 4.3% T-bill) / 33.1% volatility | 0.41 |

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
| total_debt | override: ISRG 10-K FY2025 (accession 0001035267-26-000010) |
| cash | Cash Cash Equivalents And Short Term Investments |
| equity | Stockholders Equity |
| shares | Ordinary Shares Number |

## Data flags

- total_debt 2025: filled with 0 from ISRG 10-K FY2025 (accession 0001035267-26-000010)