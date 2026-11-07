"""
Session 4: market risk across the universe (reported, not scored).

The scored risk metrics (volatility, beta, max drawdown) were computed in
Session 3. This adds what the README reports but does not score:
- the correlation table: which companies move together (weekly returns);
- volatility and the Sharpe ratio side by side, as a table and a chart,
  with the S&P 500 and the device sector as reference points.

Run:  python -m src.session4    (uses the price files saved by Session 3)
"""
import warnings

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from config import settings
from src import data, metrics

NAMES = {"MDT": "Medtronic", "ABT": "Abbott", "BDX": "Becton Dickinson", "GEHC": "GE HealthCare",
         "SYK": "Stryker", "ZBH": "Zimmer Biomet", "ISRG": "Intuitive Surgical", "GMED": "Globus Medical",
         "BSX": "Boston Scientific", "EW": "Edwards", "DXCM": "DexCom", "PODD": "Insulet", "RMD": "ResMed",
         "TFX": "Teleflex", "STE": "STERIS", "COO": "Cooper", "ALGN": "Align"}
SURFACE, INK, INK_SOFT, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
BLUE, GREY = "#2a78d6", "#b5b4ae"


def risk_return_table(closes: pd.DataFrame, tickers: list[str], risk_free: float) -> pd.DataFrame:
    """Yearly return, yearly volatility and Sharpe ratio over the 3-year window, companies and benchmarks."""
    rows = {}
    for t in tickers + [settings.MARKET_BENCHMARK, settings.SECTOR_BENCHMARK]:
        p = closes[t].dropna()
        ret = metrics.annualised_return(p)
        vol = metrics.annualised_volatility(p, settings.TRADING_DAYS_PER_YEAR)
        rows[t] = {"annual_return": ret, "volatility": vol, "sharpe": (ret - risk_free) / vol}
    return pd.DataFrame(rows).T


def plot_volatility_sharpe(table: pd.DataFrame, tickers: list[str], finalists: list[str], path) -> None:
    """
    Left: yearly volatility (how much the price swings). Right: Sharpe ratio
    (return above the risk-free rate per unit of volatility). Same company order
    in both panels (best Sharpe at the top), so each row can be read across.
    Dashed lines: S&P 500 and the device sector (IHI).
    """
    comp = table.loc[tickers].sort_values("sharpe")            # best at the top of a horizontal chart
    labels = [NAMES[t] for t in comp.index]
    colours = [BLUE if t in finalists else GREY for t in comp.index]
    refs = [(settings.MARKET_BENCHMARK, "S&P 500", (0, (4, 3))), (settings.SECTOR_BENCHMARK, "Device sector", (0, (1, 2)))]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 7), sharey=True, gridspec_kw={"wspace": 0.08})
    fig.patch.set_facecolor(SURFACE)
    for ax in (ax1, ax2):
        ax.set_facecolor(SURFACE)
        ax.grid(axis="x", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.tick_params(colors=INK_SOFT, length=0)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(GRID)

    ax1.barh(labels, comp["volatility"], color=colours, height=0.66)
    for y, v in enumerate(comp["volatility"]):
        ax1.text(v + 0.006, y, f"{v:.0%}", va="center", fontsize=8.5, color=INK)
    ax1.set_xlim(0, comp["volatility"].max() * 1.2)
    ax1.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:.0%}"))
    ax1.set_xlabel("Volatility: yearly standard deviation of daily returns", color=INK_SOFT)

    ax2.barh(labels, comp["sharpe"], color=colours, height=0.66)
    ax2.axvline(0, color=INK_SOFT, linewidth=0.9)
    for y, v in enumerate(comp["sharpe"]):
        ax2.text(v + (0.02 if v >= 0 else -0.02), y, f"{v:.2f}", va="center",
                 ha="left" if v >= 0 else "right", fontsize=8.5, color=INK)
    lo, hi = comp["sharpe"].min(), max(comp["sharpe"].max(), table.loc[settings.MARKET_BENCHMARK, "sharpe"])
    ax2.set_xlim(lo - 0.25, hi + 0.25)
    ax2.set_xlabel("Sharpe ratio: (yearly return − risk-free rate) ÷ volatility", color=INK_SOFT)

    for ax, col in ((ax1, "volatility"), (ax2, "sharpe")):
        for k, (t, name, style) in enumerate(refs):
            v = table.loc[t, col]
            ax.axvline(v, color=INK, linestyle=style, linewidth=1)
            # labels staggered in height so close lines don't overprint each other
            ax.text(v, len(comp) - 0.4 + 0.6 * k, f" {name} {v:.0%}" if col == "volatility" else f" {name} {v:.2f}",
                    color=INK, fontsize=8, va="bottom")
        ax.set_ylim(-0.6, len(comp) + 0.9)

    fig.suptitle("Risk and risk-adjusted return, Nov 2023 – Nov 2026", x=0.01, y=0.97, ha="left",
                 color=INK, fontsize=13, fontweight="bold")
    fig.subplots_adjust(top=0.9)
    fig.text(0.01, 0.005, "Blue = finalists. Dashed lines: S&P 500 and the device-sector fund (IHI). "
             "Risk-free rate = average 3-month T-bill over the period. Ordered by Sharpe ratio.",
             color=INK_SOFT, fontsize=8)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)


ROLL = 252   # 12-month moving window (trading days)
LINE_COLOURS = {"company": "#2a78d6", settings.MARKET_BENCHMARK: "#eb6834", settings.SECTOR_BENCHMARK: "#1baf7a"}


def rolling_risk(closes: pd.DataFrame, risk_free: pd.Series) -> pd.DataFrame:
    """
    For every ticker: price rebased to 100, 12-month rolling volatility and 12-month
    rolling Sharpe ratio. Columns are (ticker, measure); rows are trading days.
    """
    out = {}
    for t in closes.columns:
        p = closes[t].dropna()
        out[(t, "price_index")] = metrics.rebase(p)
        out[(t, "volatility_12m")] = metrics.rolling_volatility(p, ROLL)
        out[(t, "sharpe_12m")] = metrics.rolling_sharpe(p, risk_free, ROLL)
    return pd.DataFrame(out)


def plot_risk_over_time(roll: pd.DataFrame, ticker: str, path) -> None:
    """
    Three stacked panels on one time axis, like chart 01: price (rebased to 100),
    12-month volatility and 12-month Sharpe ratio, for one company against the
    S&P 500 and the device sector.
    """
    series = [(ticker, NAMES[ticker], LINE_COLOURS["company"], 2.2),
              (settings.MARKET_BENCHMARK, "S&P 500", LINE_COLOURS[settings.MARKET_BENCHMARK], 1.5),
              (settings.SECTOR_BENCHMARK, "Device sector (IHI)", LINE_COLOURS[settings.SECTOR_BENCHMARK], 1.5)]
    panels = [("price_index", "Value of $100 invested", lambda v: f"{v:.0f}"),
              ("volatility_12m", "Volatility, past 12 months", lambda v: f"{v:.0%}"),
              ("sharpe_12m", "Sharpe ratio, past 12 months", lambda v: f"{v:.2f}")]
    fig, axes = plt.subplots(3, 1, figsize=(11, 9), sharex=True, gridspec_kw={"height_ratios": [1.3, 1, 1], "hspace": 0.12})
    fig.patch.set_facecolor(SURFACE)
    for ax, (measure, label, fmt) in zip(axes, panels):
        ax.set_facecolor(SURFACE)
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.tick_params(colors=INK_SOFT, length=0)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
        for t, name, colour, width in reversed(series):          # company drawn last, on top
            s = roll[(t, measure)].dropna()
            ax.plot(s.index, s, color=colour, linewidth=width, label=name)
            ax.annotate(fmt(s.iloc[-1]), xy=(s.index[-1], s.iloc[-1]), xytext=(6, 0), textcoords="offset points",
                        va="center", fontsize=8.5, color=INK)
        if measure == "price_index":
            ax.axhline(100, color=INK_SOFT, linewidth=0.8, linestyle=(0, (2, 3)))
        if measure == "volatility_12m":
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
            ax.set_ylim(bottom=0)
        if measure == "sharpe_12m":
            ax.axhline(0, color=INK_SOFT, linewidth=0.9)
        ax.set_ylabel(label, color=INK_SOFT, fontsize=9)
    handles, labels_ = axes[0].get_legend_handles_labels()
    axes[0].legend(handles[::-1], labels_[::-1], loc="upper left", frameon=False, fontsize=9, labelcolor=INK)
    axes[2].xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
    axes[2].xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    fig.suptitle(f"{NAMES[ticker]}: price, volatility and Sharpe ratio over time", x=0.01, y=0.95, ha="left",
                 color=INK, fontsize=13, fontweight="bold")
    fig.subplots_adjust(top=0.9)
    fig.text(0.01, 0.005, "Volatility and Sharpe ratio are measured over the previous 12 months at each date, so they start "
             "one year after the price series (Nov 2024). Risk-free rate: 12-month average of the 3-month T-bill.",
             color=INK_SOFT, fontsize=8)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)


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

    # Volatility and Sharpe ratio, with the market and the sector for reference
    risk_free = pd.read_csv(settings.TABLES_DIR / "risk_free_rates.csv").loc[0, "value"]
    table = risk_return_table(closes, tickers, risk_free)
    table.round(4).to_csv(settings.TABLES_DIR / "risk_return.csv")
    finalists_file = settings.TABLES_DIR / "finalists.csv"     # written by Session 5 (if it has run)
    finalists = pd.read_csv(finalists_file, index_col=0).index.tolist() if finalists_file.exists() else []
    settings.CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    plot_volatility_sharpe(table, tickers, finalists, settings.CHARTS_DIR / "05_volatility_sharpe.png")
    print("\nRisk and return (3 years):\n", table.sort_values("sharpe", ascending=False).round(3).to_string())

    # Risk over time: 12-month rolling volatility and Sharpe, every company + benchmarks
    roll = rolling_risk(closes, data.load_fred(settings.RISK_FREE_SHORT))
    flat = roll.copy()
    flat.columns = [f"{t}_{m}" for t, m in roll.columns]
    flat.round(5).to_csv(settings.TABLES_DIR / "rolling_risk.csv")
    for t in finalists:
        plot_risk_over_time(roll, t, settings.CHARTS_DIR / f"06_risk_over_time_{t}.png")
    print(f"\nRolling risk saved; charts for {', '.join(finalists) or 'no finalists yet (run Session 5)'}")


if __name__ == "__main__":
    main()
