"""
Session 3: the whole universe. Every company x every metric, with every check.

Run from the project folder:
    python -m src.session3

For each of the ~20 candidate companies:
  1. download prices and financial statements (raw files saved);
  2. check the eligibility rules (README section 3);
  3. for eligible companies, compute the 12 metrics with workings;
  4. cross-check revenue and operating income against the company's own 10-K (SEC XBRL);
  5. flag anything missing, stale or implausible for a hand check.

Outputs (outputs/tables/):
  universe_eligibility.csv   every company, every rule, IN or OUT and why
  metrics_all.csv            eligible companies x 12 metrics (+ Sharpe and context)
  sec_crosscheck.csv         Yahoo vs 10-K, revenue and operating income, every company
  data_flags.csv             everything that needs a human look
  workings/{TICKER}.md       hand-check document per company
"""
import warnings

import pandas as pd
import yfinance as yf

from config import settings
from src import data, fundamentals, report, sec, universe
from src.company_metrics import compute_company_metrics

WORKINGS_DIR = settings.TABLES_DIR / "workings"


def try_prices(ticker: str) -> pd.Series | None:
    try:
        return data.load_close_prices([ticker])[ticker]
    except Exception as e:                       # delisted tickers return nothing
        print(f"  {ticker}: no prices ({type(e).__name__})")
        return None


def try_financials(ticker: str) -> tuple[pd.DataFrame | None, dict, list[str]]:
    """Statements -> clean table, labels used, and notes on any hand-checked overrides applied."""
    try:
        table, sources = fundamentals.extract_fundamentals(data.download_financials(ticker))
    except Exception as e:
        print(f"  {ticker}: no financial statements ({type(e).__name__})")
        return None, {}, []
    table, notes = fundamentals.apply_overrides(ticker, table, sources)
    return table, sources, notes


def reporting_currency(ticker: str) -> str | None:
    try:
        return yf.Ticker(ticker).info.get("financialCurrency")
    except Exception:
        return None


def plausibility_flags(ticker: str, values: dict) -> list[dict]:
    flags = []
    for key, (low, high) in settings.PLAUSIBLE_RANGES.items():
        v = values.get(key)
        if v is None or pd.isna(v):
            flags.append({"ticker": ticker, "type": "missing metric", "detail": f"{key} could not be calculated"})
        elif not low <= v <= high:
            flags.append({"ticker": ticker, "type": "outside plausible range",
                          "detail": f"{key} = {v:.3f} (expected {low} to {high})"})
    return flags


def main() -> None:
    warnings.simplefilter("ignore", FutureWarning)
    WORKINGS_DIR.mkdir(parents=True, exist_ok=True)
    vd = pd.Timestamp(settings.VALUATION_DATE)

    print("Benchmarks and risk-free rates...")
    bench = data.load_close_prices([settings.MARKET_BENCHMARK, settings.SECTOR_BENCHMARK])
    rates = data.risk_free_rates()
    rates.to_csv(settings.TABLES_DIR / "risk_free_rates.csv", index=False)
    events = universe.load_corporate_events()
    ciks = sec.cik_lookup()

    eligibility, metric_rows, sec_rows, flags = [], [], [], []
    for ticker in settings.TICKERS:
        print(f"{ticker}...")
        close = try_prices(ticker)
        table, sources, override_notes = try_financials(ticker) if close is not None else (None, {}, [])
        currency = reporting_currency(ticker) if close is not None else None
        check = universe.check_company(ticker, close, table, currency, events)
        eligibility.append(check)
        if not check["eligible"]:
            print(f"  OUT: {check['reason_if_out']}")
            continue

        # --- official filings: cross-check, and is the growth window like-for-like? ---
        company_flags = fundamentals.missing_items(table, sources) + override_notes
        growth_years = settings.GROWTH_YEARS
        try:
            facts = sec.company_facts(ticker, ciks[ticker])
            sec_rows += sec.crosscheck(ticker, facts, table)
            growth_years, note = sec.comparable_growth_years(facts, table, settings.GROWTH_YEARS)
            if note:
                company_flags.append(note)
        except Exception as e:
            flags.append({"ticker": ticker, "type": "sec", "detail": f"SEC data unavailable: {e}"})

        # --- metrics ---
        result = compute_company_metrics(
            ticker, table, stock=close,
            market=bench[settings.MARKET_BENCHMARK], sector=bench[settings.SECTOR_BENCHMARK],
            risk_free_short=rates.loc[0, "value"], growth_years=growth_years)
        (WORKINGS_DIR / f"{ticker}.md").write_text(
            report.company_workings(result, sources, company_flags, rates), encoding="utf-8")

        fy = table.index[-1]
        metric_rows.append({
            "ticker": ticker,
            "fiscal_year_end": f"{fy:%Y-%m-%d}",
            "price": round(close.iloc[-1], 2),
            "market_cap_bn": round(result.context["Market cap ($m)"] / 1e3, 1),
            "ev_bn": round(result.context["Enterprise value ($m)"] / 1e3, 1),
            "growth_years": growth_years,
            **result.values,
        })

        # --- flags ---
        flags += [{"ticker": ticker, "type": "data", "detail": f} for f in company_flags]
        flags += plausibility_flags(ticker, result.values)
        if (vd - fy).days > settings.MAX_REPORT_AGE_DAYS:
            flags.append({"ticker": ticker, "type": "stale", "detail": f"latest annual report ends {fy:%Y-%m-%d}"})
        if ticker in events.index:
            flags.append({"ticker": ticker, "type": "corporate event", "detail": events.loc[ticker, "event"]})

    sec_df = pd.DataFrame(sec_rows)
    for _, r in sec_df[sec_df["match"] != "yes"].iterrows():
        flags.append({"ticker": r["ticker"], "type": "sec mismatch",
                      "detail": f"{r['item']}: Yahoo {r['yahoo_musd']} vs 10-K {r['sec_musd']} ({r['match']})"})

    # --- save ---
    pd.DataFrame(eligibility).to_csv(settings.TABLES_DIR / "universe_eligibility.csv", index=False)
    metrics_df = pd.DataFrame(metric_rows).set_index("ticker")
    metrics_df.to_csv(settings.TABLES_DIR / "metrics_all.csv")
    sec_df.to_csv(settings.TABLES_DIR / "sec_crosscheck.csv", index=False)
    pd.DataFrame(flags).to_csv(settings.TABLES_DIR / "data_flags.csv", index=False)

    # --- print summary ---
    elig = pd.DataFrame(eligibility)
    print(f"\n{elig['eligible'].sum()} of {len(elig)} companies eligible")
    print(elig.loc[~elig["eligible"], ["ticker", "reason_if_out"]].to_string(index=False))
    with pd.option_context("display.width", 250, "display.max_columns", 30):
        print("\n", metrics_df.round(3).to_string())
        print("\nSEC cross-check:", (sec_df["match"] == "yes").sum(), "of", len(sec_df), "match")
        print(sec_df[sec_df["match"] != "yes"].to_string(index=False))
        print("\nFlags:")
        print(pd.DataFrame(flags).to_string(index=False))


if __name__ == "__main__":
    main()
