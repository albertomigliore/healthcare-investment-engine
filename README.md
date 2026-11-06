# MedTech Investment Research Engine

> **Status:** Session 0 – project specification. No code yet.
> This page is the plan: every choice is written down *before* looking at results, so the conclusion can't be bent to fit a favourite company.

---

## 1. The question

> **Among ~20 large US-listed medical device companies, which offer the best combination of quality, growth and valuation as of 6 November 2026, and does a DCF and reverse-DCF analysis of the top 3 support buying them at today's prices?**

There are two steps to answer it:

1. **Screen**: score all ~20 companies on the same rules and rank them.
2. **Deep dive**: value the top 3 properly and decide BUY / HOLD / SELL for each.

The ranking only *suggests* candidates. The valuation decides.

---

## 2. Why medical devices (MedTech)?

- **It fits my background**: biomedical technology.
- **The companies are comparable.** Device makers share a business model: they design, get regulatory approval, sell to hospitals and surgeons, and earn repeat revenue. Comparing a device maker with a drug company or a hospital chain would be like comparing apples with cars.
- **Their cash flows are positive and fairly stable**, which a DCF needs. A DCF of a biotech with no revenue would be guesswork.

---

## 3. Which companies? (the "universe")

### Rules (written first, applied to everyone)

**A company is IN if:**
1. It is listed on a US stock exchange and reports in US dollars.
2. Medical devices or equipment are its main business (more than ~half of revenue).
3. It is worth more than about $5 billion on the stock market.
4. It has at least 3 years of share price and financial history.

**A company is OUT if:**
- It has no revenue or makes losses, so a valuation would be meaningless.
- It was spun off or listed less than 3 years ago.
- Devices are only a small part of a bigger group.

### Candidate list

| Group | Companies (ticker) |
|---|---|
| Large diversified | Medtronic (MDT), Abbott (ABT), Becton Dickinson (BDX), GE HealthCare (GEHC) |
| Orthopaedics and surgery | Stryker (SYK), Zimmer Biomet (ZBH), Intuitive Surgical (ISRG), Globus Medical (GMED) |
| Heart and blood vessels | Boston Scientific (BSX), Edwards Lifesciences (EW), Penumbra (PEN) |
| Diabetes | DexCom (DXCM), Insulet (PODD) |
| Breathing and sleep | ResMed (RMD) |
| Hospital products | Baxter (BAX), Teleflex (TFX), STERIS (STE), Masimo (MASI) |
| Diagnostics and imaging | Hologic (HOLX) |
| Eye care and dental | Cooper Companies (COO), Align Technology (ALGN) |

**Still to check** (in Session 1, with the data): that every company is still listed in the same form. Companies get bought, taken private or split up. **Hologic** and **Teleflex** in particular had deals in progress in 2025. Anything that fails a rule is removed and recorded in the decision log (section 12).

**Excluded on purpose:**
- Johnson & Johnson: mostly a drug company.
- IDEXX: animal diagnostics, a different market.
- Solventum: spun off in 2024, so less than 3 years of history.
- Smith & Nephew: a UK company, so it doesn't meet the US listing and reporting rule.

---

## 4. What we compare against (benchmarks)

| Benchmark | What it is | Why |
|---|---|---|
| **S&P 500 (SPY)** | The 500 biggest US companies: "the market" | To measure **beta**, how much a stock moves when the whole market moves. That's the standard way to measure market risk, and it feeds the cost of capital in the DCF. |
| **Medical devices ETF (IHI)** | A fund holding US device companies: "the sector" | To check whether a company is **beating its own sector**, not just riding a sector-wide wave. |

**Risk-free rate**: the return on US government bonds, treated as "no risk". 10-year Treasury yield for the DCF; 3-month Treasury bill for the Sharpe ratio. The exact values and dates get recorded in Session 1.

---

## 5. Where the data come from

| Data | Source | Used for |
|---|---|---|
| Daily share prices (adjusted for dividends and splits) | Yahoo Finance via the `yfinance` Python library | Returns, risk, momentum, market value |
| Financial statements (last ~4 years) | Yahoo Finance via `yfinance` | All business metrics in the screen |
| Annual reports (10-K) | SEC EDGAR (the official US filings website) | **Checking by hand** the key numbers of the top 3 companies |
| Interest rates | US Treasury | Risk-free rate |

**Data rules:**
- Raw downloads are saved untouched in `data/raw/`, with the **date and source** recorded.
- A missing number stays missing. It is **never replaced with zero**.
- Units (thousands vs millions) and fiscal years are checked. Some companies' years don't end in December: Medtronic's ends in April.
- If a number could change the final decision, it's checked against the annual report.

---

## 6. Time settings

| Setting | Choice | Why |
|---|---|---|
| Valuation date | **6 November 2026** | Everything is a snapshot of this day |
| Price history | **3 years** | Recent enough to describe the companies as they are today |
| Financial history | Last 3 fiscal years of growth (4 annual reports) | Matches the 3-year window |
| Returns for beta | **Weekly** (~156 weeks) | Less noisy than daily; standard practice |
| Returns for volatility and drawdown | **Daily** | More detail |
| Currency | US dollars only | No currency conversion needed |

---

## 7. How each company is scored

### The five scoring groups

| Group | Weight | Question it answers |
|---|---|---|
| **Quality** | 30% | Is this a good business? |
| **Growth** | 25% | Is it getting bigger? |
| **Value** | 20% | Is the share price cheap compared with what the business earns? |
| **Momentum** | 15% | Is the share price trending up, compared with the sector? |
| **Risk** | 10% | How bumpy is the ride? |

**Why these weights?** Quality gets the most because in MedTech good businesses tend to *stay* good (patents, surgeons trained on one system, hospital contracts). Risk gets the least because all these companies are large and fairly stable, so their risk differences are small. **These weights are my judgement, not a law of nature**, which is why section 8 tests how much they matter.

### The 12 metrics, in plain words

**Quality (30%)**

| Metric | Formula | In plain words | Better if |
|---|---|---|---|
| ROIC | operating profit × (1 − tax rate) ÷ (debt + shareholders' equity − cash) | How much profit each dollar invested in the business earns each year | Higher |
| FCF margin | (cash from operations − spending on equipment) ÷ revenue | Out of every $1 of sales, how much real cash is left over | Higher |
| Net debt / EBITDA | (debt − cash) ÷ EBITDA | How many years of earnings it would take to pay off the debt | **Lower** |

**Growth (25%)**

| Metric | Formula | In plain words | Better if |
|---|---|---|---|
| Revenue growth (3-yr CAGR) | (revenue now ÷ revenue 3 years ago)^(1/3) − 1 | The average yearly growth of sales | Higher |
| Operating profit growth (3-yr CAGR) | Same formula, with operating profit | The average yearly growth of profit from the core business | Higher |

*If a profit figure is negative, its growth rate can't be calculated, so it's left missing and flagged.*

**Value (20%)**

| Metric | Formula | In plain words | Better if |
|---|---|---|---|
| EV / EBITDA | (market value + debt − cash) ÷ EBITDA | How many years of earnings you pay to buy the whole company | **Lower** (cheaper) |
| FCF yield | free cash flow ÷ market value | The cash return you'd get on the share price | Higher (cheaper) |

**Momentum (15%)**

| Metric | Formula | In plain words | Better if |
|---|---|---|---|
| 12-1 month return | price 1 month ago ÷ price 12 months ago − 1 | Last year's price trend, skipping the last month (very recent moves tend to reverse) | Higher |
| Return vs sector | 12-month stock return − 12-month IHI return | Did it beat the other device companies? | Higher |

**Risk (10%)**

| Metric | Formula | In plain words | Better if |
|---|---|---|---|
| Volatility | standard deviation of daily returns × √252 | How much the price jumps around in a typical year | **Lower** |
| Beta | slope of weekly stock returns against weekly S&P 500 returns | 1.2 means it tends to move 1.2% when the market moves 1% | **Lower** |
| Max drawdown | biggest fall from a peak to a later low, over 3 years | The worst loss you could have suffered | **Lower** (smaller fall) |

**Reported but not scored**: the Sharpe ratio (return per unit of risk) and a correlation table (which companies move together).

### Turning metrics into one score

1. **Percentile rank** each metric: "better than X% of the other companies", from 0 to 100. For "lower is better" metrics the order is flipped. Percentiles stop one extreme company from dominating.
2. **Group score** = the average of that group's metric ranks. If a metric is missing, the group uses the ones available, and the gap is flagged.
3. **Total score** = 30% Quality + 25% Growth + 20% Value + 15% Momentum + 10% Risk.
4. **Rank** the companies by total score, and show how much each group contributed, so it's visible *why* a company ranks where it does.

---

## 8. Is the ranking robust? (the quant check)

The weights in section 7 are my opinion. To see how much the ranking depends on them:

- Rerun the ranking **10,000 times** with random weights, each group varying around its chosen weight (e.g. Quality anywhere from 20% to 40%), always adding up to 100%.
- For each company, report **the probability it lands in the top 3**.

A company that is top 3 in 95% of the runs is a robust pick. One that is top 3 in 40% of them only made it because of my exact weights. **The top 3 for the deep dive are chosen using this check, not only the single ranking.**

---

## 9. How the top 3 are valued

Each company is valued **three ways**, because no single method is reliable on its own.

**a) DCF (discounted cash flow): "what is the business worth?"**
1. Forecast revenue for the next 5 years, with an explicit growth rate.
2. Forecast operating margin → operating profit → tax → free cash flow.
3. Discount each year's cash flow back to today using the **WACC** (the average return investors demand, from the cost of shares and the cost of debt).
4. Add a **terminal value** for all years after year 5 (assuming slow, steady growth of about 2.5–3% a year forever).
5. That sum is the **enterprise value**. Subtract net debt to get the **equity value**, then divide by the number of shares to get the **value per share**.

**b) Trading comparables: "what do similar companies sell for?"** Take the EV/EBITDA and EV/Sales of 4–6 genuinely similar companies from the universe, apply them to our company, and get a value range.

**c) Reverse DCF: "what is the market assuming?"** Start from today's share price and solve backwards: **what revenue growth would make the DCF equal today's price?** Then compare it with what the company has actually achieved. If the market needs 12% a year and the company has grown 6%, the price looks too optimistic.

**Scenarios**: three versions of each DCF.

| Case | Purpose | What changes |
|---|---|---|
| Bear | Try to break the investment idea | Lower growth, lower margins, higher WACC |
| Base | The most defensible case | Assumptions backed by history and company guidance |
| Bull | The upside | Higher growth and margins, lower WACC |

**Monte Carlo**: run the DCF **10,000 times**, each time drawing growth, margins, WACC and terminal growth at random from sensible ranges. The result is a **distribution of values**, giving the median value and **the probability the company is worth more than today's price**.

### Decision rule (fixed now, before seeing any results)

| Decision | Condition |
|---|---|
| **BUY** | Median simulated value is **at least 15% above** today's price **and** P(value > price) is at least 65% |
| **SELL** | Median simulated value is **at least 15% below** today's price |
| **HOLD** | Anything in between |

Fixing the rule in advance means the conclusion follows the evidence and can't be bent towards a favourite company.

---

## 10. What the project will produce

- **A ranking table** of all companies, with each group's contribution.
- **Top-3 probabilities** from the robustness check.
- **A valuation for each of the 3 finalists**: DCF, comparables, reverse DCF, bear/base/bull and the Monte Carlo distribution.
- **3–5 charts** that support the decision, and no more.
- **An investment memo** (5–7 pages) in `reports/`: recommendation, reasons, valuation, risks, what the market is pricing in, and limitations.

---

## 11. Known limitations (written in advance, updated as we go)

- **Survivorship bias**: we only look at companies that exist today. The ones that failed or were bought aren't in the list.
- **Exclusion bias**: leaving out loss-making companies removes the riskiest part of the sector.
- **Data quality**: Yahoo Finance data can have gaps or errors, which is why the top 3 are checked against their annual reports.
- **Fiscal years differ**: some companies' years end in different months, so "the last year" doesn't cover exactly the same period for everyone.
- **The weights are subjective**: tested in section 8, but still a choice.
- **A DCF is only as good as its assumptions**: hence the scenarios and the Monte Carlo.
- **A 3-year window is short**: it may not include a full economic cycle.
- **This is a learning project, not investment advice.**

---

## 12. Decision log

Every change, with the reason. This shows the thinking behind the project.

| Date | Decision | Why |
|---|---|---|
| 6 Nov 2026 | Focus on US-listed medical device companies | Comparable business models; positive cash flows suit a DCF; fits my degree |
| 6 Nov 2026 | 3-year price window | Recent, reflects the companies as they are now |
| 6 Nov 2026 | S&P 500 for beta, IHI for relative momentum | Beta against the market feeds the cost of capital; sector comparison isolates company strength |
| 6 Nov 2026 | Weights 30/25/20/15/10 | Quality is the most durable signal in MedTech; risk differences between large device firms are small |
| 6 Nov 2026 | EV/EBITDA and FCF yield instead of P/E | Earnings per share in MedTech are distorted by acquisition-related accounting charges |
| 6 Nov 2026 | Stryker as the test company for the pipeline | Large, clear business, carries debt (tests the debt-to-equity step); **not** a pick |
| 6 Nov 2026 | Excluded J&J, IDEXX, Solventum, Smith & Nephew | Mostly pharma / animal market / under 3 years of history / not a US company |

---

## 13. Work plan (~20 hours)

| # | Session | Hours | Done when |
|---|---|---|---|
| 0 | Specification (this page) | 1 | ✅ This README |
| 1 | Setup + Stryker data | 2 | Stryker's prices and financials loaded and checked against its annual report |
| 2 | Stryker metrics | 2 | All 12 metrics for Stryker, checked by hand |
| 3 | All ~20 companies | 2 | One table: every company × every metric |
| 4 | Market risk | 2 | Volatility, beta, drawdown, momentum, correlations |
| 5 | Ranking + robustness | 2 | Ranking, contributions, top-3 probabilities |
| 6 | DCF + reverse DCF, company 1 | 3 | A working, sanity-checked DCF and the implied growth |
| 7 | Companies 2–3, comparables, scenarios | 2 | All 3 finalists valued three ways |
| 8 | Monte Carlo | 1.5 | Value distributions and P(undervalued) |
| 9 | Memo, charts, GitHub | 2.5 | Memo written, repository published |

**Deliberately left out** (optional extras in the brief): portfolio optimisation, backtesting, automatic extraction of annual reports, dashboards.

---

## 14. Folder structure

```
healthcare-investment-engine/
├── config/            # settings: tickers, weights, dates, assumptions
├── data/
│   ├── raw/           # downloads exactly as received (never edited)
│   └── processed/     # cleaned, checked data
├── src/               # the Python code
├── notebooks/         # exploring and checking one company step by step
├── outputs/
│   ├── charts/        # final charts
│   └── tables/        # ranking, valuations, simulations
├── reports/           # the investment memo
└── tests/             # automatic checks on the formulas
```
