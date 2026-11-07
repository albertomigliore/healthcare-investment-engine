# Investment memo: US medical devices, November 2026

**Valuation date:** 6 November 2026 (closing prices) · **Universe:** 17 US-listed device companies · **Method and code:** [README](../README.md)

> *This is a learning project, not investment advice.*

---

## 1. Recommendation

| Company | Price | Base-case DCF | Monte Carlo median | P(value > price) | Growth the price implies | Company guidance | **Call** |
|---|---|---|---|---|---|---|---|
| **DexCom (DXCM)** | $79.41 | $42 | $42 | 0% | ~28% next year | 12–13% | **SELL** |
| **Globus Medical (GMED)** | $71.05 | $71 | $71 | 47% | 5.1% | ~5% | **HOLD** |
| **ResMed (RMD)** | $235.30 | $234 | $234 | 47% | 7.1% | ~7% (core, Q1 FY27) | **HOLD** |

**In one sentence:** a quantitative screen of 17 device companies picked three that looked like the best mix of quality, growth and value, but valuing them shows that two are priced almost exactly for what they are expected to deliver, and the third, DexCom, is priced for growth more than twice what the company itself guides.

The decision rule was fixed before any value was calculated: **BUY** only if the median simulated value is at least 15% above the price *and* the probability of being undervalued is at least 65%; **SELL** if the median is at least 15% below the price; otherwise **HOLD**.

---

## 2. How I got here

1. **Universe (20 candidates → 17).** Large US-listed companies whose main business is medical devices. Three had been taken over or were being taken over (Hologic, Masimo, Penumbra), and Baxter failed the "no operating losses" rule after a $485m write-down. I did not replace them: choosing replacements after seeing the data would open the door to picking favourites.
2. **Screen.** Twelve metrics in five groups, each converted to a percentile rank and combined: Quality 30%, Growth 25%, Value 20%, Momentum 15%, Risk 10%.
3. **Robustness.** The weights are my judgement, so I re-ran the ranking 10,000 times with each weight varied by ±10 points. Globus Medical and ResMed finished in the top 3 in 100% of runs, DexCom in 95%; no other company exceeded 5%. The top 3 does not depend on my exact weights.
4. **Valuation of the top 3.** A 10-year DCF, a reverse DCF (what growth does the price imply?), trading comparables, bear/base/bull scenarios, and a 10,000-run Monte Carlo.

Every company's revenue and operating profit were cross-checked against its own 10-K filing (34 of 34 match).

---

## 3. DexCom: SELL

**The business.** DexCom makes continuous glucose monitors (CGMs), wearable sensors that let people with diabetes track blood sugar without finger pricks. It is the highest-quality company in the universe on my measures: 33% return on invested capital, 23% free cash flow margin, net cash on the balance sheet. The shares were the best performers in the screen (+44% on the 12-1 month measure).

**The problem is the price, not the business.** At $79.41, DexCom trades at 25.7x EBITDA. For a DCF to reach that price, revenue would need to grow about 28% next year and about 16% a year for ten years. The company's own guidance, raised on 29 October 2026, is 12–13% for 2026, with fourth-quarter growth around 10% and international growth of only 5% in Q3.

**Every method agrees.**
- DCF: bear $28, base $42, bull $67. Even the bull case (growth 3 points above guidance, margins 3 points higher, a lower discount rate) is below today's price.
- Comparables: peers' multiples imply $49–73.
- Monte Carlo: none of 10,000 simulations reaches the price.

**Stress test.** I stacked three assumptions in DexCom's favour at once: adding back share-based pay (3.4% of revenue, which I otherwise treat as a real cost because it dilutes shareholders), assuming no extra capex for its new plants, and cutting the discount rate to 8.5%. Value: $66.79, still below the SELL threshold of $67.50.

**What would make me wrong.** A step-change in growth that guidance doesn't yet reflect: faster adoption in type 2 diabetes patients not on insulin, a major international expansion, or a new product cycle. A takeover would also make the call wrong. The market may be pricing such optionality; my model does not, deliberately, because the base case follows the company's own guidance.

---

## 4. Globus Medical: HOLD

**The business.** Spine and orthopaedic implants, plus "enabling technologies" (surgical robotics and navigation).

**Why the screen ranked it first.** It looked like growth at a bargain price: 42% revenue growth a year over three years at only 12.1x EBITDA, the lowest multiple in the whole universe.

**Why the valuation disagrees.** The 42% was mostly *bought*: Globus merged with NuVasive in 2023 and later acquired Nevro. On its own, the business is guided to grow about 5% in 2026; the guidance was cut in Q3, when sales fell 0.7% (base business ex-Nevro +3%). The reverse DCF shows the price implies 5.1% growth, almost exactly the guidance.

**Cheap for a reason.** Peers trade at multiples that would put Globus at $107–110, but peers aren't growing at 5% with a recent guidance cut. The DCF ($71) says the market has priced Globus correctly, and the Monte Carlo puts the chance of it being undervalued at 47%: a coin toss.

**What would change the call.** Evidence that organic growth is re-accelerating, particularly in robotics (+24% in Q3), or successful integration lifting margins above today's. The company has raised its buyback programme by $500m, which signals management thinks the shares are cheap.

---

## 5. ResMed: HOLD

**The business.** The leading maker of CPAP devices and masks for sleep apnoea, with a large recurring revenue stream from masks and accessories.

**A great business at a fair price.** ResMed is the all-rounder of the screen: 25.8% return on invested capital, 28.8% free cash flow margin, no weak group. It grew 10% a year over three years and 7% (core, constant currency) in the latest quarter.

**The price already reflects it.** The reverse DCF implies 7.1% growth, against 7% recently delivered. Base-case value $234 vs price $235. My modelled first-year cash flow margin (28.8%) matches exactly what ResMed actually earned, which gives me confidence in the inputs.

**Risks.** Weight-loss drugs (GLP-1s) reducing sleep-apnoea prevalence over time is a widely discussed risk for the category; component cost inflation (flagged by the company); and the integration of recent acquisitions. Upside: margins keep expanding (non-GAAP gross margin 62.5% in Q1 FY27).

---

## 6. What the market is pricing in

| | Growth implied by the price | Recent / guided growth | Gap |
|---|---|---|---|
| Globus Medical | 5.1% | ~5% | none |
| ResMed | 7.1% | ~7% | none |
| DexCom | ~28% (16% a year over 10 years) | 12–13% | **large** |

The reverse DCF is the most useful single number in the project. It turns "is this stock cheap?" into a question that can be checked: "does the business need to do something it has never done, or that it says it won't, to justify the price?"

---

## 7. Can these numbers be trusted?

**Data.** Every number came from Yahoo Finance and was cross-checked against official SEC filings. Along the way I found and fixed:
- an intraday price disguised as a closing price;
- Yahoo adding back "one-off" charges to operating income (Stryker had them every year);
- Teleflex's growth comparing two different companies after a restatement;
- a spin-off recorded as a stock split (I verified the adjustment factor, 1.272);
- Intuitive Surgical showing no debt line (it has no debt, confirmed in its 10-K).

**Method.** All rules were fixed before seeing results. I changed the valuation method twice after the first run, and I report this openly:
1. The first 5-year model valued companies after year 5 at 7.6–12x EBITDA, below any device company today (12–43x), and mishandled non-cash amortisation. I switched to a 10-year, EBITDA-based model.
2. The model's first-year cash flow for DexCom was 9.6% of revenue vs 23.1% actually earned, because the balance-sheet working-capital measure ignored accrued rebates. I switched to the cash flow statement.

The first run said SELL for all three; it is kept in the repository. Neither change was chosen to reach a conclusion, and the DexCom SELL survives the most generous combination of assumptions I tested.

---

## 8. Limitations

- **Survivorship and takeover bias.** Companies that failed or were bought (three of the 20 candidates) are missing, and those are often the attractive ones.
- **Bought vs organic growth** can't be separated with free data. Globus shows why this matters.
- **Model probabilities.** "P(value > price)" is the share of simulated futures above the price given the model and the ranges chosen; it measures how robust the conclusion is to those assumptions, not the true probability of the share being undervalued. The draws are also independent, whereas growth, margins and the discount rate are related in reality.
- **One-number assumptions.** The equity risk premium (5%), terminal growth (2.5%) and beta adjustment are standard choices, not facts; the Monte Carlo varies the most important ones but not all.
- **Guidance can be wrong.** The base cases lean on what companies say; a company that beats its own guidance consistently would be undervalued by this approach.
- **Three years** of prices is short and may not cover a full cycle.

---

*Data: Yahoo Finance and SEC EDGAR (XBRL), FRED (US Treasury rates); company guidance from earnings releases (sources in [data/manual/valuation_assumptions.csv](../data/manual/valuation_assumptions.csv)). Code, tests and every intermediate table: [repository](../README.md).*
