# MedTech Investment Research Engine

> **Status:** Sessions 1–2 of 9 complete: data pipeline built and checked, and all 12 screening metrics calculated and hand-checked on the test company (Stryker). See [Progress and findings](#progress-and-findings).
> This page is the plan: every choice is written down *before* looking at results, so the conclusion can't be bent to fit a favourite company.

---

## Progress and findings

### Session 1: Stryker data, loaded and checked ✅

![Stryker vs the market and its sector](outputs/charts/01_stryker_vs_benchmarks.png)

**Reproduce it:** `python -m src.session1` (downloads everything, runs the checks, redraws the chart).

**1. Yahoo Finance vs Stryker's official 10-K (FY2025, $ millions)**

| Item | Yahoo | 10-K | Difference | Match |
|---|---|---|---|---|
| Revenue | 25,116 | 25,116 | 0.0% | ✅ |
| Operating income: Yahoo's plain "Operating Income" | 5,059 | 4,889 | +3.5% | ❌ (adds back one-off charges; see finding 2) |
| Operating income: Yahoo's "As Reported" line | 4,889 | 4,889 | 0.0% | ✅ (used from Session 2 on) |
| Net income | 3,246 | 3,246 | 0.0% | ✅ |
| Operating cash flow | 5,044 | 5,044 | 0.0% | ✅ |
| Capital expenditure | −761 | −761 | 0.0% | ✅ |
| Total debt | 15,859 | 15,859 | 0.0% | ✅ |
| Cash | 4,011 | 4,011 | 0.0% | ✅ |
| Shares outstanding (m) | 382.5 | 382.7 | −0.1% | ✅ (cover-page count is dated one month later) |

Source: Stryker 10-K, accession 0000310764-26-000010, filed 11 Feb 2026, via the SEC's XBRL data. Stored with its source in [data/manual/SYK_10K_FY2025.csv](data/manual/SYK_10K_FY2025.csv).

**2. First numbers for Stryker**

| | Stryker | S&P 500 | Device sector (IHI) |
|---|---|---|---|
| 3-year total return | 21.2% | 75.0% | 23.9% |
| Return per year | 6.6% | 20.5% | 7.4% |
| Volatility (yearly) | 25.1% | 15.4% | 18.7% |
| Maximum drawdown | −32.5% (Jul 2025 → Sep 2026) | −18.8% | −26.6% |

| Business (FY2025) | |
|---|---|
| Revenue | $25.1bn |
| Revenue growth, 3-yr CAGR (2022–25) | 10.8% a year |
| Free cash flow | $4.3bn |
| FCF margin | 17.1% |

*Prices to the close of 6 Nov 2026.*

**3. What this tells us so far**
- **The business grew faster than the share price.** Revenue compounded at 10.8% a year, but the shares returned only 6.6% a year, so the market now pays less for each dollar of sales than it did 3 years ago. Whether that makes Stryker cheap or the old price too high is exactly what the valuation stage has to answer.
- **The whole sector lagged the market.** $100 in device stocks became $124; $100 in the S&P 500 became $175. Stryker's story is mostly a sector story, which is why the screen measures momentum *relative to IHI*, not just in absolute terms.
- **Stryker was bumpier than its sector** (25% vs 19% volatility) and had a deeper worst fall (−32% vs −27%).

**4. Data-quality findings** (each one changed the code)

| # | Finding | How it was caught | What was done |
|---|---|---|---|
| 1 | A download during US trading hours returns a **mid-day price disguised as a close**. | The last row had a quarter of the normal trading volume; the download was at 12:04 New York time. | `drop_unfinished_day()` now removes any unfinished day automatically and warns. |
| 2 | Yahoo's plain **"Operating Income" is 3.5% higher** than the 10-K. In Session 2 the cause was found: Yahoo adds back "special charges" ($170m in 2025, $977m in 2024). Stryker has had these "one-offs" every year from 2022 to 2025. | Line-by-line check against the 10-K, then a search of Yahoo's other income-statement lines. | Yahoo's **"Total Operating Income As Reported"** line matches the 10-K exactly, and is now used everywhere (decision log). |
| 3 | Yahoo's **2024 EBITDA looked too low**: only $0.3bn above *adjusted* operating income, when 2024 D&A was $1.05bn. Explained in Session 2: Yahoo's EBITDA is *after* the $977m special charge of 2024, while its "Operating Income" is *before* it. The two lines use different definitions. | Sanity check: EBITDA must be well above operating income. | EBITDA is built ourselves as as-reported operating income + D&A, so both use one definition. |
| 4 | Yahoo's **oldest financial year is almost empty** (45 of 46 lines missing). | Counted missing values per column. | Mostly-empty years are dropped; 4 usable years (2022–25) remain, as the plan needs. |


### Session 2: the 12 screening metrics for Stryker, hand-checked ✅

**Reproduce it:** `python -m src.session2`. Every formula with the real numbers plugged in: [outputs/tables/SYK_metrics_workings.md](outputs/tables/SYK_metrics_workings.md).

| Group | Metric | Workings ($ millions) | Stryker |
|---|---|---|---|
| Quality | ROIC | 4,889 × (1 − 19.5%) ÷ (15,859 debt + 22,420 equity − 4,011 cash) | **11.5%** |
| Quality | FCF margin | (5,044 operating cash flow − 761 capex) ÷ 25,116 revenue | **17.1%** |
| Quality | Net debt / EBITDA | (15,859 − 4,011) ÷ (4,889 operating income + 1,193 D&A) | **1.95x** |
| Growth | Revenue growth (3-yr) | (25,116 ÷ 18,449)^(1/3) − 1 | **10.8%** |
| Growth | Operating profit growth (3-yr) | (4,889 ÷ 2,841)^(1/3) − 1 | **19.8%** |
| Value | EV / EBITDA | (124,645 market cap + 15,859 − 4,011) ÷ 6,082 | **22.4x** |
| Value | FCF yield | 4,283 ÷ 124,645 ($325.87 × 382.5m shares) | **3.4%** |
| Momentum | 12-1 month return | $278.20 (6 Oct 2026) ÷ $349.93 (6 Nov 2025) − 1 | **−20.5%** |
| Momentum | Return vs sector (12m) | SYK −6.9% minus IHI −4.6% | **−2.2%** |
| Risk | Volatility | 1.58% daily std. dev. × √252 (753 days) | **25.1%** |
| Risk | Beta | weekly returns vs S&P 500 (156 weeks) | **0.53** |
| Risk | Max drawdown | $268.90 (24 Sep 2026) ÷ $398.20 (25 Jul 2025) − 1 | **−32.5%** |
| *Reported* | Sharpe ratio | (6.6% yearly return − 4.3% avg. T-bill) ÷ 25.1% | *0.09* |

Price: close of 6 Nov 2026. Financials: FY2025. Tax rate: 3-year pooled effective rate. Risk-free rates from FRED ([outputs/tables/risk_free_rates.csv](outputs/tables/risk_free_rates.csv)): 3-month T-bill averaged 4.33% over the 3 years; 10-year Treasury 4.90% (4 Nov 2026, the latest published before the valuation date).

**How the numbers were checked**
- **By hand:** every row above can be recomputed with a calculator from the workings column.
- **Independently:** volatility, beta (as a regression slope), drawdown and both momentum figures were recomputed straight from the raw CSV files with different code. All matched.
- **Automatically:** 34 tests check every formula on made-up examples with known answers, including edge cases (losses, negative EBITDA, missing data, weekends).

**What Stryker's numbers say** (on their own they mean little; Session 3 ranks them against 19 peers)
- **Margins are expanding.** Operating profit grew almost twice as fast as revenue (19.8% vs 10.8% a year): the operating margin went from 15.4% to 19.5%. Part of this is a low 2022 base (that year had $270m of special charges).
- **Investors pay for growth, not current cash.** The FCF yield (3.4%) is **below** the 10-year Treasury yield (4.9%): buying Stryker today only makes sense if its cash flows keep growing. The reverse DCF (Session 6) will put a number on how much growth the price assumes.
- **Low beta, high volatility.** Stryker moves only about half as much as the market (beta 0.53), yet its price swings more than the market's (25% vs 15% volatility). So most of its risk is **company-specific**, not market-driven, and in a diversified portfolio much of that risk would cancel out.
- **The trend is negative.** Down 20.5% on the 12-1 measure and slightly behind the sector over 12 months: momentum will count against it in the screen.

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
| 6 Nov 2026 | Drop any trading day that hasn't finished yet | A download at 12:04 New York time returned a mid-day price as if it were the close |
| 6 Nov 2026 | ~~Screen uses Yahoo figures; valuation uses 10-K figures~~ **Replaced (Session 2):** operating income = Yahoo's "As Reported" line everywhere | The 3.5% gap was Yahoo adding back "one-off" charges. The as-reported figure matches the 10-K, so it is verifiable, and it doesn't accept the company's own view of what counts as a one-off. Stryker had such charges in every year from 2022 to 2025 |
| 6 Nov 2026 | Calculate EBITDA ourselves (as-reported operating income + D&A) instead of using Yahoo's | Yahoo's EBITDA and "Operating Income" treat one-off charges differently, so mixing them is inconsistent |
| 6 Nov 2026 | Official figures come from the SEC's XBRL data, with the filing's accession number recorded | Same numbers as the 10-K document, but machine-readable and traceable to the exact filing |
| 6 Nov 2026 | All settings live in `config/settings.py`; formulas in `src/metrics.py` with automatic tests | One place to change a choice; every formula checked on examples with known answers |
| 6 Nov 2026 | ROIC tax rate = total tax ÷ total pre-tax profit over 3 years (capped at 35%; 21% if pre-tax profit is negative) | One year's rate can be distorted (Stryker: 14% in 2024, 28% in 2025); pooling smooths that out |
| 6 Nov 2026 | Risk-free rates from FRED (DTB3, DGS10); Sharpe uses the 3-year *average* T-bill rate | FRED republishes the US Treasury's daily rates as a free, downloadable series. A 3-year return should be compared with the rate available over those same 3 years |
| 6 Nov 2026 | Market cap = valuation-date price × shares from the latest balance sheet | The same, verifiable share count for every company (it matched the 10-K cover page within 0.1% for Stryker) |
| 6 Nov 2026 | Max drawdown stored as a negative number, with "higher is better" | −10% is a smaller fall than −30%, so scoring must rank closer-to-zero higher |

---

## 13. Work plan (~20 hours)

| # | Session | Hours | Done when |
|---|---|---|---|
| 0 | Specification (this page) | 1 | ✅ This README |
| 1 | Setup + Stryker data | 2 | ✅ Stryker's prices and financials loaded and checked against its annual report |
| 2 | Stryker metrics | 2 | ✅ All 12 metrics for Stryker, checked by hand |
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
├── config/
│   └── settings.py    # every choice in one place: tickers, dates, weights, decision rule
├── data/
│   ├── raw/           # downloads exactly as received (never edited)
│   ├── manual/        # figures taken from official filings, with their source
│   └── processed/     # cleaned, checked data
├── src/
│   ├── data.py        # downloading, saving and loading data
│   ├── fundamentals.py     # picks the needed lines out of the statements, records the label used
│   ├── metrics.py          # the formulas, one small function each
│   ├── company_metrics.py  # the 12 metrics for one company, with workings
│   ├── session1.py         # Session 1 pipeline: python -m src.session1
│   └── session2.py         # Session 2 pipeline: python -m src.session2
├── notebooks/         # exploring and checking one company step by step
├── outputs/
│   ├── charts/        # final charts
│   └── tables/        # ranking, valuations, simulations
├── reports/           # the investment memo
└── tests/             # automatic checks on the formulas: python -m pytest
```
