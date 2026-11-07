"""
Session 4: market risk across the universe (reported, not scored).

The scored risk metrics (volatility, beta, max drawdown) were computed in
Session 3. This adds what the README reports but does not score:
- the correlation table: which companies move together (weekly returns);
- the Sharpe ratio side by side.

Run:  python -m src.session4    (uses the price files saved by Session 3)
"""
import warnings

import numpy as np
import pandas as pd

from config import settings
from src import data, metrics


def main() -> None:
    warnings.simplefilter("ignore")
    tickers = pd.read_csv(settings.TABLES_DIR / "metrics_all.csv", index_col=0).index.tolist()
    closes = data.load_close_prices(tickers + [settings.MARKET_BENCHMARK, settings.SECTOR_BENCHMARK],
                                    download=False)
    weekly = pd.DataFrame({t: metrics.weekly_returns(closes[t]) for t in closes.columns})
    corr = weekly.corr()
    corr.round(3).to_csv(settings.TABLES_DIR / "correlations_weekly.csv")

    companies = corr.loc[tickers, tickers]
    pairs = companies.where(np.triu(np.ones(companies.shape, dtype=bool), k=1)).stack()
    summary = pd.DataFrame({
        "corr_with_SPY": corr.loc[tickers, settings.MARKET_BENCHMARK],
        "corr_with_IHI": corr.loc[tickers, settings.SECTOR_BENCHMARK],
        "avg_corr_with_peers": (companies.sum() - 1) / (len(tickers) - 1),
    }).round(2)
    summary.to_csv(settings.TABLES_DIR / "correlation_summary.csv")

    print(f"Weekly returns, {len(weekly)} weeks")
    print(f"Average correlation between two device companies: {pairs.mean():.2f}")
    print(f"Average correlation with the S&P 500: {summary['corr_with_SPY'].mean():.2f}")
    print("\nMost correlated pairs:\n", pairs.sort_values(ascending=False).head(5).round(2).to_string())
    print("\nLeast correlated pairs:\n", pairs.sort_values().head(5).round(2).to_string())
    print("\n", summary.sort_values("avg_corr_with_peers").to_string())


if __name__ == "__main__":
    main()
