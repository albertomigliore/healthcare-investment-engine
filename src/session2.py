"""
Session 2: the 12 screening metrics for Stryker, with workings for a hand check.

Run from the project folder (after Session 1 has saved the statements):
    python -m src.session2

Outputs:
    outputs/tables/SYK_metrics.csv            the 12 metrics (+ Sharpe), machine-readable
    outputs/tables/SYK_metrics_workings.md    every formula with the numbers plugged in
    outputs/tables/risk_free_rates.csv        the rates used, with their dates
"""
import pandas as pd

from config import settings
from src import data, fundamentals, report
from src.company_metrics import compute_company_metrics

TICKER = settings.TEST_COMPANY


def metrics_rows(result) -> list[dict]:
    """The metric values as rows (metric, name, group, direction, value), Sharpe last."""
    rows = [{"metric": k, "name": settings.METRICS[k]["name"], "group": settings.METRICS[k]["group"],
             "higher_is_better": settings.METRICS[k]["higher_is_better"], "value": v}
            for k, v in result.values.items() if k in settings.METRICS]
    rows.append({"metric": "sharpe", "name": "Sharpe ratio", "group": "Reported only",
                 "higher_is_better": True, "value": result.values["sharpe"]})
    return rows


def main() -> None:
    settings.TABLES_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading data...")
    closes = data.load_close_prices([TICKER, settings.MARKET_BENCHMARK, settings.SECTOR_BENCHMARK])
    statements = data.load_financials(TICKER)
    table, sources = fundamentals.extract_fundamentals(statements)
    table, override_notes = fundamentals.apply_overrides(TICKER, table, sources)
    flags = fundamentals.missing_items(table, sources) + override_notes
    rates = data.risk_free_rates()
    rates.to_csv(settings.TABLES_DIR / "risk_free_rates.csv", index=False)

    result = compute_company_metrics(
        TICKER, table,
        stock=closes[TICKER], market=closes[settings.MARKET_BENCHMARK], sector=closes[settings.SECTOR_BENCHMARK],
        risk_free_short=rates.loc[0, "value"],
    )

    pd.DataFrame(metrics_rows(result)).to_csv(settings.TABLES_DIR / f"{TICKER}_metrics.csv", index=False)
    md = report.company_workings(result, sources, flags, rates)
    (settings.TABLES_DIR / f"{TICKER}_metrics_workings.md").write_text(md, encoding="utf-8")

    print(md)


if __name__ == "__main__":
    main()
