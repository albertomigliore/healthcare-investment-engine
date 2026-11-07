"""
Export everything the interactive page needs into app/data.js.

Run:  python -m src.export_app      (after Sessions 3, 5 and 6)

The page (app/index.html) is static: open it with a double-click, no server.
All numbers come from the pipeline outputs; nothing is typed by hand.
"""
import json
from dataclasses import asdict

import numpy as np
import pandas as pd

from config import settings
from src import session6

APP_DIR = settings.PROJECT_ROOT / "app"

NAMES = {"MDT": "Medtronic", "ABT": "Abbott", "BDX": "Becton Dickinson", "GEHC": "GE HealthCare",
         "SYK": "Stryker", "ZBH": "Zimmer Biomet", "ISRG": "Intuitive Surgical", "GMED": "Globus Medical",
         "BSX": "Boston Scientific", "EW": "Edwards Lifesciences", "PEN": "Penumbra", "DXCM": "DexCom",
         "PODD": "Insulet", "RMD": "ResMed", "BAX": "Baxter", "TFX": "Teleflex", "STE": "STERIS",
         "MASI": "Masimo", "HOLX": "Hologic", "COO": "Cooper Companies", "ALGN": "Align Technology"}

WHAT_THEY_MAKE = {
    "MDT": "Diversified devices: cardiac rhythm, surgical, neuroscience, diabetes.",
    "ABT": "Diagnostics, devices (incl. FreeStyle Libre glucose sensors), nutrition and generics.",
    "BDX": "Syringes, catheters, medication management and surgical products.",
    "GEHC": "Imaging (CT, MRI, ultrasound), patient monitoring and imaging drugs.",
    "SYK": "Orthopaedic implants, surgical equipment and neurotechnology.",
    "ZBH": "Hip, knee and other orthopaedic implants.",
    "ISRG": "The da Vinci surgical robot, with recurring instrument sales.",
    "GMED": "Spine and orthopaedic implants plus surgical robotics and navigation.",
    "BSX": "Cardiology (heart-rhythm, structural heart), endoscopy and urology devices.",
    "EW": "Heart valves, especially transcatheter (TAVR) valves.",
    "DXCM": "Continuous glucose monitors (wearable blood-sugar sensors).",
    "PODD": "The Omnipod tubeless insulin pump.",
    "RMD": "CPAP machines and masks for sleep apnoea, plus home-care software.",
    "TFX": "Catheters and devices for vascular access and interventional procedures.",
    "STE": "Sterilisation equipment and services for hospitals and pharma.",
    "COO": "Contact lenses and women's health / fertility products.",
    "ALGN": "Invisalign clear aligners and dental scanners.",
}

METRIC_HELP = {
    "roic": "Profit after tax earned on each dollar invested by lenders and shareholders.",
    "fcf_margin": "Out of every $1 of sales, the cash left after running and investing in the business.",
    "net_debt_to_ebitda": "Years of earnings needed to repay debt (negative = more cash than debt).",
    "revenue_cagr": "Average yearly sales growth over 3 years (bought growth included).",
    "operating_income_cagr": "Average yearly growth of operating profit over 3 years.",
    "ev_to_ebitda": "Years of earnings you pay to buy the whole company. Lower = cheaper.",
    "fcf_yield": "Cash return on the share price: free cash flow / market value.",
    "momentum_12_1": "Price change from 12 months ago to 1 month ago (skips the last month).",
    "return_vs_sector": "12-month return minus the device sector ETF's (IHI).",
    "volatility": "How much the price swings in a typical year.",
    "beta": "How much the stock moves when the market moves 1%.",
    "max_drawdown": "The worst fall from a peak over 3 years.",
}


def clean(x):
    """JSON-safe values: NaN -> None, numpy -> python."""
    if isinstance(x, dict):
        return {k: clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean(v) for v in x]
    if isinstance(x, (np.floating, float)):
        return None if np.isnan(x) else float(x)
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, pd.Timestamp):
        return x.strftime("%Y-%m-%d")
    return x


def main() -> None:
    T = settings.TABLES_DIR
    metrics = pd.read_csv(T / "metrics_all.csv", index_col=0)
    ranking = pd.read_csv(T / "ranking.csv", index_col=0)
    robust = pd.read_csv(T / "robustness.csv", index_col=0)
    elig = pd.read_csv(T / "universe_eligibility.csv", index_col=0)
    flags = pd.read_csv(T / "data_flags.csv")
    summary = pd.read_csv(T / "valuation_summary.csv", index_col=0)
    rates = pd.read_csv(T / "risk_free_rates.csv")
    assumptions = pd.read_csv(settings.MANUAL_DIR / "valuation_assumptions.csv", index_col=0)
    sector_of = {t: g for g, ts in settings.UNIVERSE.items() for t in ts}
    finalists = pd.read_csv(T / "finalists.csv", index_col=0).index.tolist()
    risk_return = pd.read_csv(T / "risk_return.csv", index_col=0)      # from Session 4

    companies = []
    for t in ranking.index:
        m, r = metrics.loc[t], ranking.loc[t]
        companies.append({
            "ticker": t, "name": NAMES[t], "sector": sector_of[t], "what": WHAT_THEY_MAKE[t],
            "rank": int(r["rank"]), "total": r["total"],
            "groups": {g: r[g] for g in ["Quality", "Growth", "Value", "Momentum", "Risk"]},
            "metrics": {k: {"value": m[k], "pct": r[f"pct_{k}"]} for k in settings.METRICS},
            "p_top3": robust.loc[t, "p_top"], "rank_p5": robust.loc[t, "rank_p5"], "rank_p95": robust.loc[t, "rank_p95"],
            "price": m["price"], "market_cap_bn": m["market_cap_bn"], "fiscal_year_end": m["fiscal_year_end"],
            "sharpe": risk_return.loc[t, "sharpe"], "annual_return": risk_return.loc[t, "annual_return"],
            "volatility": risk_return.loc[t, "volatility"], "finalist": t in finalists,
            "flags": flags.loc[flags["ticker"] == t, "detail"].tolist(),
        })

    excluded = [{"ticker": t, "name": NAMES[t], "reason": row["reason_if_out"]}
                for t, row in elig.iterrows() if not row["eligible"]]

    valuations = {}
    for t in finalists:
        i, record, table = session6.build_inputs(t, metrics.loc[t], rates, assumptions.loc[t])
        peers = session6.peer_multiples(settings.PEERS[t], metrics)
        latest = table.iloc[-1]
        s = summary.loc[t]
        valuations[t] = {
            "inputs": asdict(i),
            "record": record,
            "price": metrics.loc[t, "price"],
            "ebitda0": latest["ebitda"], "revenue0": latest["revenue"],
            "beta_raw": metrics.loc[t, "beta"],
            "peers": [{"ticker": p, "name": NAMES[p], "ev_ebitda": peers.loc[p, "EV/EBITDA"],
                       "ev_sales": peers.loc[p, "EV/Sales"]} for p in peers.index],
            "python": {k: s[k] for k in ["dcf_bear", "dcf_base", "dcf_bull", "mc_median", "mc_p10", "mc_p90",
                                          "p_value_above_price", "implied_year1_growth", "decision",
                                          "comps_ev_ebitda_mid", "comps_ev_sales_mid"]},
            "reasoning": assumptions.loc[t, "reasoning"], "source": assumptions.loc[t, "source"],
        }

    payload = {
        "valuation_date": settings.VALUATION_DATE,
        "weights": settings.WEIGHTS,
        "metric_specs": {k: {**v, "help": METRIC_HELP[k]} for k, v in settings.METRICS.items()},
        "scenarios": settings.SCENARIOS,
        "rule": {"buy_upside": settings.BUY_MIN_UPSIDE, "buy_probability": settings.BUY_MIN_PROBABILITY,
                 "sell_downside": settings.SELL_MIN_DOWNSIDE},
        "settings": {"erp": settings.EQUITY_RISK_PREMIUM, "credit_spread": settings.CREDIT_SPREAD,
                     "terminal_growth": settings.TERMINAL_GROWTH, "years": settings.FORECAST_YEARS,
                     "n_sims": settings.N_SIMULATIONS, "weight_spread": settings.WEIGHT_SPREAD},
        "rates": rates.to_dict(orient="records"),
        "benchmarks": [{"ticker": t, "name": n, **risk_return.loc[t, ["annual_return", "volatility", "sharpe"]].to_dict()}
                       for t, n in [(settings.MARKET_BENCHMARK, "S&P 500"), (settings.SECTOR_BENCHMARK, "Device sector (IHI)")]],
        "companies": companies, "excluded": excluded, "finalists": finalists, "valuations": valuations,
    }
    APP_DIR.mkdir(exist_ok=True)
    js = "// Generated by `python -m src.export_app`. Do not edit by hand.\nwindow.APP_DATA = " + \
         json.dumps(clean(payload), indent=1) + ";\n"
    (APP_DIR / "data.js").write_text(js, encoding="utf-8")
    print(f"Wrote {APP_DIR / 'data.js'}: {len(companies)} companies, {len(valuations)} valuations")


if __name__ == "__main__":
    main()
