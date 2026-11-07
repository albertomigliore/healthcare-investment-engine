"""
Sessions 6-8: valuing the three finalists, and the decision.

Run:  python -m src.session6     (uses the outputs of Sessions 3 and 5)

For each finalist:
  1. WACC from CAPM (README section 9)
  2. DCF: base, bear and bull scenarios
  3. Reverse DCF: the growth today's price implies
  4. Trading comparables: peers' EV/EBITDA and EV/Sales applied to the company
  5. Monte Carlo: 10,000 DCFs -> median value and P(value > price)
  6. BUY / HOLD / SELL by the rule fixed in advance

Outputs (outputs/tables/): valuation_summary.csv, dcf_{TICKER}.csv (forecast table),
valuation_{TICKER}.md (every input and step, to rebuild the DCF by hand),
and charts 03 (valuation ranges) and 04 (Monte Carlo distributions).
"""
from dataclasses import replace

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config import settings
from src import data, fundamentals, report
from src import valuation as v

NAMES = {"GMED": "Globus Medical", "RMD": "ResMed", "DXCM": "DexCom"}
SURFACE, INK, INK_SOFT, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"


# ---------------------------------------------------------------------------
# Inputs
# ---------------------------------------------------------------------------
def line(statements: dict, statement: str, labels: list[str]) -> pd.Series:
    df = statements[statement].copy()
    df.columns = pd.to_datetime(df.columns)
    df = df.sort_index(axis=1)
    for label in labels:
        if label in df.index:
            return df.loc[label]
    raise KeyError(f"none of {labels} in {statement}")


def build_inputs(ticker: str, metrics_row: pd.Series, rates: pd.DataFrame, assumptions: pd.Series) -> tuple:
    """Everything the DCF needs, from the raw statements, with a record of where each number came from."""
    statements = data.load_financials(ticker)
    table, sources = fundamentals.extract_fundamentals(statements)
    table, _ = fundamentals.apply_overrides(ticker, table, sources)
    latest, fy = table.iloc[-1], table.index[-1]
    last3 = table.iloc[-3:]

    tax = (last3["tax"].sum() / last3["pretax_income"].sum())
    tax = float(np.clip(tax, 0, settings.TAX_RATE_CAP))
    # Working capital needed per extra $ of revenue = what growth actually cost over the last
    # 3 years according to the cash flow statement (Session 6 finding: the balance-sheet version,
    # receivables + inventory - payables, ignores accrued liabilities such as DexCom's rebates).
    # Floored at 0: we never assume that growth releases cash forever.
    wc_cash = line(statements, "cashflow", ["Change In Working Capital"])
    wc_years = table.index[-3:]
    revenue_added = (table["revenue"].diff()).loc[wc_years].sum()
    cash_into_wc = -wc_cash.reindex(wc_years).sum()            # cash flow sign: negative = cash tied up
    nwc_pct = max(0.0, cash_into_wc / revenue_added) if revenue_added > 0 else 0.0

    op_margin0 = latest["operating_income"] / latest["revenue"]
    da_pct0 = latest["depreciation_amortisation"] / latest["revenue"]
    ebitda_margin0 = latest["ebitda"] / latest["revenue"]          # = op_margin0 + da_pct0
    # The assumptions file gives a target OPERATING margin (what companies guide on) or "latest";
    # it becomes an EBITDA-margin target by adding back today's D&A %.
    target = (ebitda_margin0 if assumptions["margin_target"] == "latest"
              else float(assumptions["margin_target"]) + da_pct0)
    risk_free = rates.loc[2, "value"]
    beta_raw = metrics_row["beta"]
    beta = v.adjusted_beta(beta_raw, settings.BETA_BLUME_WEIGHT)
    market_cap = metrics_row["market_cap_bn"] * 1e9
    w = v.wacc(risk_free, beta, settings.EQUITY_RISK_PREMIUM, settings.CREDIT_SPREAD, tax,
               market_cap, latest["total_debt"])

    inputs = v.DCFInputs(
        revenue0=latest["revenue"], g1=float(assumptions["g1"]), g_term=settings.TERMINAL_GROWTH,
        margin0=ebitda_margin0, margin_target=target, tax_rate=tax,
        da_pct0=da_pct0,
        capex_pct=(last3["capital_expenditure"].abs() / last3["revenue"]).mean(),
        nwc_pct=nwc_pct, wacc=w["wacc"], debt=latest["total_debt"], cash=latest["cash"],
        shares=latest["shares"], years=settings.FORECAST_YEARS)
    record = {
        "Financial year (base)": f"{fy:%b %Y}",
        "Revenue ($m)": round(latest["revenue"] / 1e6),
        "Operating margin today (as reported)": f"{op_margin0:.1%}",
        "EBITDA margin today (operating income + D&A)": f"{ebitda_margin0:.1%}",
        f"Target EBITDA margin (year {settings.FORECAST_YEARS})": f"{target:.1%}",
        "Year-1 revenue growth": f"{inputs.g1:.1%}",
        "Terminal growth": f"{inputs.g_term:.1%}",
        "Tax rate (3-yr pooled)": f"{tax:.1%}",
        "D&A % of revenue (latest year)": f"{inputs.da_pct0:.1%}",
        "Capex % of revenue (3-yr avg; D&A converges to it)": f"{inputs.capex_pct:.1%}",
        "Working capital per extra $ of revenue": f"{nwc_pct:.1%} (3-yr cash flow statement: {cash_into_wc/1e6:,.0f} into working capital for {revenue_added/1e6:,.0f} of added revenue; floor 0)",
        "Debt ($m)": round(latest["total_debt"] / 1e6),
        "Cash + short-term investments ($m)": round(latest["cash"] / 1e6),
        "Shares (m)": round(latest["shares"] / 1e6, 1),
        "Share price, 6 Nov 2026 ($)": metrics_row["price"],
        "Risk-free rate (10-yr Treasury)": f"{risk_free:.2%}",
        "Beta: measured -> adjusted": f"{beta_raw:.2f} -> {beta:.2f}",
        "Equity risk premium": f"{settings.EQUITY_RISK_PREMIUM:.1%}",
        "Cost of equity": f"{w['cost_of_equity']:.2%} = {risk_free:.2%} + {beta:.2f} x {settings.EQUITY_RISK_PREMIUM:.1%}",
        "Cost of debt (after tax)": f"{w['cost_of_debt_after_tax']:.2%} = ({risk_free:.2%} + {settings.CREDIT_SPREAD:.1%}) x (1 - {tax:.1%})",
        "Weights (equity / debt)": f"{w['weight_equity']:.1%} / {w['weight_debt']:.1%}",
        "WACC": f"{w['wacc']:.2%}",
        "Base-case reasoning": assumptions["reasoning"],
        "Source": assumptions["source"],
    }
    return inputs, record, table


def scenario(i: v.DCFInputs, name: str) -> v.DCFInputs:
    s = settings.SCENARIOS[name]
    return replace(i, g1=i.g1 + s["g1"], margin_target=i.margin_target + s["margin"],
                   wacc=i.wacc + s["wacc"], g_term=s["g_term"])


def peer_multiples(peers: list[str], metrics_all: pd.DataFrame) -> pd.DataFrame:
    rows = {}
    for p in peers:
        table, sources = fundamentals.extract_fundamentals(data.load_financials(p))
        table, _ = fundamentals.apply_overrides(p, table, sources)
        latest = table.iloc[-1]
        ev = metrics_all.loc[p, "ev_bn"] * 1e9
        rows[p] = {"EV/EBITDA": ev / latest["ebitda"], "EV/Sales": ev / latest["revenue"]}
    return pd.DataFrame(rows).T


# ---------------------------------------------------------------------------
# Charts
# ---------------------------------------------------------------------------
def _style(ax):
    ax.set_facecolor(SURFACE)
    ax.tick_params(colors=INK_SOFT, length=0)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def football_field(results: dict, path) -> None:
    """For each finalist: the value range from every method, against today's price."""
    fig, axes = plt.subplots(len(results), 1, figsize=(11, 2.3 * len(results) + 0.9))
    fig.patch.set_facecolor(SURFACE)
    for ax, (t, r) in zip(np.atleast_1d(axes), results.items()):
        _style(ax)
        bars = [
            ("Comparables: EV/Sales (25th-75th pct.)", r["comps_sales"]["low"], r["comps_sales"]["high"], r["comps_sales"]["mid"], AQUA),
            ("Comparables: EV/EBITDA (25th-75th pct.)", r["comps_ebitda"]["low"], r["comps_ebitda"]["high"], r["comps_ebitda"]["mid"], AQUA),
            ("DCF: bear - bull (tick = base)", r["bear"], r["bull"], r["base"], ORANGE),
            ("Monte Carlo: 10th-90th pct. (tick = median)", r["mc_p10"], r["mc_p90"], r["mc_median"], BLUE),
        ]
        for y, (label, lo, hi, mid, colour) in enumerate(bars):
            ax.barh(y, hi - lo, left=lo, height=0.55, color=colour, alpha=0.85)
            ax.plot([mid, mid], [y - 0.3, y + 0.3], color=INK, linewidth=2)
            ax.text(hi, y, f"  ${lo:,.0f} – ${hi:,.0f}", va="center", color=INK, fontsize=8.5)
        ax.set_yticks(range(len(bars)))
        ax.set_yticklabels([b[0] for b in bars], fontsize=8.5, color=INK_SOFT)
        ax.axvline(r["price"], color=INK, linestyle=(0, (3, 2)), linewidth=1.2)
        ax.text(r["price"], len(bars) - 0.35, f" price ${r['price']:,.2f}", color=INK, fontsize=9, va="bottom")
        ax.set_title(f"{NAMES[t]} ({t}): {r['decision']}", loc="left", fontsize=11, fontweight="bold", color=INK)
        xmax = max(b[2] for b in bars) * 1.25
        ax.set_xlim(0, xmax)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    fig.suptitle("Value per share by method vs today's price", x=0.01, ha="left", fontsize=13,
                 fontweight="bold", color=INK)
    fig.text(0.01, 0.005, "Dashed line = close of 6 Nov 2026. Decision rule (fixed in advance): BUY if median "
             "Monte Carlo value ≥ price +15% and P(value > price) ≥ 65%; SELL if median ≤ price −15%; else HOLD.",
             color=INK_SOFT, fontsize=8)
    fig.tight_layout(rect=(0, 0.02, 1, 0.96))
    fig.savefig(path, dpi=160, facecolor=SURFACE)
    plt.close(fig)


def mc_chart(mcs: dict, results: dict, path) -> None:
    """Small multiples: the distribution of 10,000 simulated values per share, against the price."""
    fig, axes = plt.subplots(1, len(mcs), figsize=(12, 3.8))
    fig.patch.set_facecolor(SURFACE)
    for ax, (t, mc) in zip(np.atleast_1d(axes), mcs.items()):
        _style(ax)
        r = results[t]
        vals = mc["value_per_share"]
        vals = vals[vals <= vals.quantile(0.995)]          # hide the extreme 0.5% tail (display only)
        bins = np.linspace(vals.min(), vals.max(), 50)
        below, above = vals[vals < r["price"]], vals[vals >= r["price"]]
        ax.hist(below, bins=bins, color="#b5b4ae", edgecolor=SURFACE, linewidth=0.4)
        ax.hist(above, bins=bins, color=BLUE, edgecolor=SURFACE, linewidth=0.4)
        ax.axvline(r["price"], color=INK, linestyle=(0, (3, 2)), linewidth=1.2)
        ax.axvline(r["mc_median"], color=ORANGE, linewidth=1.6)
        ax.set_yticks([])
        ax.set_title(f"{NAMES[t]}: P(value > price) = {r['p_above']:.0%}", loc="left", fontsize=10.5,
                     fontweight="bold", color=INK)
        ax.text(0.98, 0.95, f"price ${r['price']:,.0f}\nmedian ${r['mc_median']:,.0f}", transform=ax.transAxes,
                ha="right", va="top", fontsize=8.5, color=INK)
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    fig.suptitle("Monte Carlo: 10,000 DCFs with random growth, margin, WACC and terminal growth",
                 x=0.01, ha="left", fontsize=12.5, fontweight="bold", color=INK)
    fig.text(0.01, 0.005, "Blue = simulated value above today's price (dashed); orange line = median. "
             "Assumptions drawn between the bear and bull cases (base most likely).", color=INK_SOFT, fontsize=8)
    fig.tight_layout(rect=(0, 0.03, 1, 0.93))
    fig.savefig(path, dpi=160, facecolor=SURFACE)
    plt.close(fig)


# ---------------------------------------------------------------------------
def main() -> None:
    finalists = pd.read_csv(settings.TABLES_DIR / "finalists.csv", index_col=0).index.tolist()
    metrics_all = pd.read_csv(settings.TABLES_DIR / "metrics_all.csv", index_col=0)
    rates = pd.read_csv(settings.TABLES_DIR / "risk_free_rates.csv")
    assumptions = pd.read_csv(settings.MANUAL_DIR / "valuation_assumptions.csv", index_col=0)
    rule = dict(buy_upside=settings.BUY_MIN_UPSIDE, buy_probability=settings.BUY_MIN_PROBABILITY,
                sell_downside=settings.SELL_MIN_DOWNSIDE)

    results, mcs, summary = {}, {}, []
    for t in finalists:
        i, record, table = build_inputs(t, metrics_all.loc[t], rates, assumptions.loc[t])
        price = metrics_all.loc[t, "price"]
        cases = {name: scenario(i, name) for name in ("bear", "base", "bull")}
        values = {name: v.dcf(c) for name, c in cases.items()}
        base_proj = v.project(i)
        base_proj.to_csv(settings.TABLES_DIR / f"dcf_{t}.csv")

        g_implied = v.implied_growth(i, price)
        cagr_implied = v.forecast_cagr(replace(i, g1=g_implied)) if pd.notna(g_implied) else np.nan
        hist_cagr = metrics_all.loc[t, "revenue_cagr"]

        peers = peer_multiples(settings.PEERS[t], metrics_all)
        latest = table.iloc[-1]
        comps_ebitda = v.comparables_value(peers["EV/EBITDA"], latest["ebitda"], i.debt, i.cash, i.shares)
        comps_sales = v.comparables_value(peers["EV/Sales"], latest["revenue"], i.debt, i.cash, i.shares)

        bear_mc = {"g1": cases["bear"].g1, "margin_target": cases["bear"].margin_target,
                   "wacc": cases["bear"].wacc, "g_term": cases["bear"].g_term}
        bull_mc = {"g1": cases["bull"].g1, "margin_target": cases["bull"].margin_target,
                   "wacc": cases["bull"].wacc, "g_term": cases["bull"].g_term}
        mc = v.monte_carlo(i, bear_mc, bull_mc, settings.N_SIMULATIONS, settings.RANDOM_SEED)
        mcs[t] = mc
        vals = mc["value_per_share"]
        median, p_above = vals.median(), (vals > price).mean()
        call = v.decision(median, p_above, price, **rule)

        results[t] = {"price": price, "bear": values["bear"]["value_per_share"],
                      "base": values["base"]["value_per_share"], "bull": values["bull"]["value_per_share"],
                      "comps_ebitda": comps_ebitda, "comps_sales": comps_sales,
                      "mc_p10": vals.quantile(0.10), "mc_median": median, "mc_p90": vals.quantile(0.90),
                      "p_above": p_above, "decision": call}
        summary.append({
            "ticker": t, "price": price, "wacc": i.wacc,
            "dcf_bear": values["bear"]["value_per_share"], "dcf_base": values["base"]["value_per_share"],
            "dcf_bull": values["bull"]["value_per_share"],
            "terminal_share_of_ev": values["base"]["terminal_share_of_ev"],
            "implied_terminal_ev_ebitda": values["base"]["implied_terminal_ev_ebitda"],
            "comps_ev_ebitda_mid": comps_ebitda["mid"], "comps_ev_sales_mid": comps_sales["mid"],
            "implied_year1_growth": g_implied, "implied_forecast_revenue_cagr": cagr_implied,
            "historical_3yr_revenue_cagr": hist_cagr, "base_year1_growth": i.g1,
            "mc_p10": vals.quantile(0.10), "mc_median": median, "mc_p90": vals.quantile(0.90),
            "p_value_above_price": p_above, "median_vs_price": median / price - 1, "decision": call,
        })

        # Hand-check document: every input, the forecast table, every result
        proj = base_proj.copy()
        money = ["revenue", "ebitda", "da", "ebit", "tax", "capex", "change_nwc", "fcff", "pv_fcff"]
        proj[money] = (proj[money] / 1e6).round(0)
        proj[["growth", "ebitda_margin"]] = (proj[["growth", "ebitda_margin"]] * 100).round(1)
        proj["discount_factor"] = proj["discount_factor"].round(4)
        b = values["base"]
        md = [
            f"# {NAMES[t]} ({t}): valuation workings", "",
            "Money in $ millions unless stated. Rebuild this in a spreadsheet: every number below is an input or a step.", "",
            "## Inputs", "", report.markdown_table(pd.DataFrame(list(record.items()), columns=["Input", "Value"])), "",
            "## Base-case forecast (growth and margin in %)", "",
            report.markdown_table(proj.reset_index()), "",
            f"Year {settings.FORECAST_YEARS + 1} is only used for the terminal value: its FCFF / (WACC - terminal growth).", "",
            "## Base-case result", "",
            f"- PV of years 1-{settings.FORECAST_YEARS} cash flows: {b['pv_explicit']/1e6:,.0f}",
            f"- Terminal value: {b['terminal_value']/1e6:,.0f}; discounted: {b['pv_terminal']/1e6:,.0f} "
            f"({b['terminal_share_of_ev']:.0%} of enterprise value)",
            f"- Enterprise value: {b['enterprise_value']/1e6:,.0f}",
            f"- Equity value = EV - debt + cash: {b['equity_value']/1e6:,.0f}",
            f"- **Value per share: ${b['value_per_share']:,.2f}** vs price ${price:,.2f}",
            f"- Sanity check: implied terminal EV/EBITDA {b['implied_terminal_ev_ebitda']:.1f}x", "",
            "## Scenarios (value per share)", "",
            *[f"- {n}: ${values[n]['value_per_share']:,.2f}" for n in ("bear", "base", "bull")], "",
            "## Reverse DCF", "",
            f"- Year-1 growth needed to justify ${price:,.2f}: **{g_implied:.1%}** "
            f"({settings.FORECAST_YEARS}-year revenue CAGR {cagr_implied:.1%}) vs base case {i.g1:.1%} and 3-year history {hist_cagr:.1%}", "",
            "## Comparables", "", report.markdown_table(peers.round(1).reset_index().rename(columns={"index": "Peer"})), "",
            f"- EV/EBITDA: ${comps_ebitda['low']:,.0f} - ${comps_ebitda['high']:,.0f} (median ${comps_ebitda['mid']:,.0f})",
            f"- EV/Sales: ${comps_sales['low']:,.0f} - ${comps_sales['high']:,.0f} (median ${comps_sales['mid']:,.0f})", "",
            "## Monte Carlo (10,000 runs)", "",
            f"- 10th / 50th / 90th percentile: ${vals.quantile(0.1):,.0f} / ${median:,.0f} / ${vals.quantile(0.9):,.0f}",
            f"- P(value > price): {p_above:.0%}",
            f"- **Decision: {call}**",
        ]
        (settings.TABLES_DIR / f"valuation_{t}.md").write_text("\n".join(md), encoding="utf-8")

    pd.DataFrame(summary).set_index("ticker").to_csv(settings.TABLES_DIR / "valuation_summary.csv")
    football_field(results, settings.CHARTS_DIR / "03_valuation_ranges.png")
    mc_chart(mcs, results, settings.CHARTS_DIR / "04_monte_carlo.png")
    with pd.option_context("display.width", 250, "display.max_columns", 30):
        print(pd.DataFrame(summary).set_index("ticker").T.to_string())


if __name__ == "__main__":
    main()
