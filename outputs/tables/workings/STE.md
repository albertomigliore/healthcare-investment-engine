# STE: the 12 screening metrics, with workings

Valuation date 2026-11-06. Money in $ millions.

## Inputs

| Input | Value |
|---|---|
| Financial year used | 2026 (ended 31 Mar 2026) |
| Price date | 06 Nov 2026 |
| Share price ($) | 252.3 |
| Shares (m) | 97.8 |
| Market cap ($m) | 24675 |
| Enterprise value ($m) | 26323 |
| EBITDA ($m) | 1588 |
| Free cash flow ($m) | 972 |
| Tax rate (pooled 3 yrs) | 23.4% |

## Risk-free rates (FRED)

| rate | value | basis |
|---|---|---|
| 3-month T-bill (Sharpe) | 4.33% | average 06 Nov 2023 – 05 Nov 2026 |
| 3-month T-bill, latest | 4.00% | as of 05 Nov 2026 |
| 10-year Treasury (DCF) | 4.84% | as of 05 Nov 2026 |

## Metrics

| Group | Metric | Workings | Result |
|---|---|---|---|
| Quality | ROIC | 1,102 x (1 - 23.4%) / (2,087 debt + 7,184 equity - 440 cash) | 9.6% |
| Quality | FCF margin | (1,341 op. cash flow - 369 capex) / 5,936 revenue | 16.4% |
| Quality | Net debt / EBITDA | (2,087 debt - 440 cash) / (1,102 op. income + 486 D&A) | 1.04x |
| Growth | Revenue growth (3-yr) | (5,936 revenue 2026 / 4,536 in 2023) ^ (1/3) - 1 | 9.4% |
| Growth | Operating profit growth (3-yr) | (1,102 op. income 2026 / 791 in 2023) ^ (1/3) - 1 | 11.7% |
| Value | EV / EBITDA | (24,675 market cap + 2,087 debt - 440 cash) / 1,588 EBITDA | 16.57x |
| Value | FCF yield | 972 FCF / 24,675 market cap ($252.30 x 97.8m shares) | 3.9% |
| Momentum | 12-1 month return | $208.65 (06 Oct 2026) / $257.84 (06 Nov 2025) - 1 | -19.1% |
| Momentum | Return vs sector (12m) | STE -2.2% minus IHI -4.6% (12 months to 06 Nov 2026) | 2.5% |
| Risk | Volatility | std. dev. of 753 daily returns (1.51%) x sqrt(252) | 23.9% |
| Risk | Beta | covariance / variance of 156 weekly returns, STE vs SPY | 0.33 |
| Risk | Max drawdown | $198.79 (17 Jun 2026) / $266.36 peak (16 Jan 2026) - 1 | -25.4% |
| Reported only | Sharpe ratio | (6.1% yearly return - 4.3% T-bill) / 23.9% volatility | 0.07 |

## Yahoo labels used

| Item | Yahoo label |
|---|---|
| revenue | Total Revenue |
| operating_income | Total Operating Income As Reported |
| pretax_income | Pretax Income |
| tax | Tax Provision |
| depreciation_amortisation | Depreciation Amortization Depletion |
| operating_cash_flow | Operating Cash Flow |
| capital_expenditure | Capital Expenditure |
| total_debt | Total Debt |
| cash | Cash Cash Equivalents And Short Term Investments |
| equity | Stockholders Equity |
| shares | Ordinary Shares Number |

## Data flags

- depreciation_amortisation: used fallback label 'Depreciation Amortization Depletion'