"""
Run the whole pipeline, in the order the steps depend on each other.

    python -m src.run_all             # downloads fresh data, then everything else
    python -m src.run_all --no-download   # re-run from the saved data (no internet needed)

Order and why:
  session3  data + eligibility + the 12 metrics for every company   (downloads)
  session5  ranking, robustness, finalists                          (needs session3)
  session4  correlations, volatility/Sharpe, risk over time          (needs session5 for the finalists)
  session6  valuation of the finalists                              (needs session5)
  export_app  data for the interactive report                       (needs all of the above)
Session 1 (Stryker's hand check against its 10-K and chart 01) is separate: python -m src.session1
"""
import sys
import time

from src import export_app, session3, session4, session5, session6


def main() -> None:
    steps = [("session3", session3.main), ("session5", session5.main), ("session4", session4.main),
             ("session6", session6.main), ("export_app", export_app.main)]
    if "--no-download" in sys.argv:
        steps = steps[1:]
        print("Skipping session3 (using the saved data and metrics).")
    for name, step in steps:
        start = time.time()
        print(f"\n=== {name} ===")
        step()
        print(f"--- {name} done in {time.time() - start:.0f}s")
    print("\nAll steps finished. Run the tests with: python -m pytest")


if __name__ == "__main__":
    main()
