"""
Session 1: Stryker data, loaded and checked.

Run from the project folder:
    python -m src.session1

What it does:
1. Downloads 3 years of prices for Stryker, the S&P 500 (SPY) and the device sector (IHI).
2. Downloads Stryker's three financial statements.
3. Checks Yahoo's key numbers against Stryker's official 10-K.
4. Calculates a first set of numbers (return, CAGR, volatility, drawdown, FCF margin).
5. Saves two tables and one chart to outputs/.
"""
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import FuncFormatter, PercentFormatter

from config import settings
from src import data, metrics

TICKER = settings.TEST_COMPANY
FY = "2025-12-31"   # latest financial year

# Chart colours (validated categorical palette, slots 1-3, light mode)
COLOURS = {TICKER: "#2a78d6", settings.MARKET_BENCHMARK: "#eb6834", settings.SECTOR_BENCHMARK: "#1baf7a"}
SURFACE, INK, INK_SOFT, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
LABELS = {TICKER: "Stryker (SYK)", settings.MARKET_BENCHMARK: "S&P 500 (SPY)",
          settings.SECTOR_BENCHMARK: "Med-device sector (IHI)"}


# ---------------------------------------------------------------------------
# 1. 10-K check
# ---------------------------------------------------------------------------
def check_against_10k(statements: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Put Yahoo's figures next to the official 10-K figures and flag any gap over 1%."""
    ten_k = pd.read_csv(settings.MANUAL_DIR / f"{TICKER}_10K_FY2025.csv")
    rows = []
    for _, r in ten_k.iterrows():
        yahoo = statements[r["yahoo_statement"]].loc[r["yahoo_label"], FY] / 1e6
        diff = yahoo / r["value_musd"] - 1
        rows.append({
            "Item": r["item"],
            "Yahoo ($m)": round(yahoo, 1),
            "10-K ($m)": r["value_musd"],
            "Difference": f"{diff:+.1%}",
            "Match": "yes" if abs(diff) < settings.MATCH_TOLERANCE else "NO",
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 2. Headline numbers
# ---------------------------------------------------------------------------
def snapshot(closes: pd.DataFrame, statements: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, pd.Series]:
    """A first look at Stryker: price behaviour vs benchmarks, and business numbers."""
    rows = {}
    for t in closes.columns:
        p = closes[t].dropna()
        dd = metrics.max_drawdown(p)
        rows[LABELS[t]] = {
            "3-yr total return": metrics.total_return(p),
            "Return per year": metrics.cagr(p.iloc[-1], p.iloc[0], years=3),
            "Volatility (yearly)": metrics.annualised_volatility(p, settings.TRADING_DAYS_PER_YEAR),
            "Max drawdown": dd["max_drawdown"],
            "Drawdown peak": dd["peak_date"].date(),
            "Drawdown low": dd["trough_date"].date(),
        }
    prices_table = pd.DataFrame(rows).T

    inc, cf = statements["income"], statements["cashflow"]
    revenue = inc.loc["Total Revenue"]
    fcf = cf.loc["Operating Cash Flow", FY] + cf.loc["Capital Expenditure", FY]
    business = pd.Series({
        "Revenue FY2025 ($bn)": revenue[FY] / 1e9,
        "Revenue CAGR 2022-25": metrics.cagr(revenue[FY], revenue["2022-12-31"], years=3),
        "Free cash flow FY2025 ($bn)": fcf / 1e9,
        "FCF margin FY2025": fcf / revenue[FY],
    })
    return prices_table, business


# ---------------------------------------------------------------------------
# 3. Chart
# ---------------------------------------------------------------------------
def plot_vs_benchmarks(closes: pd.DataFrame, path) -> None:
    """
    Top: growth of $100 in Stryker vs the market vs the sector (one shared scale).
    Bottom: Stryker's drawdown, i.e. how far below its previous peak it was each day.
    """
    rebased = metrics.rebase(closes.dropna())
    dd = metrics.drawdown(closes[TICKER].dropna())
    worst = metrics.max_drawdown(closes[TICKER])

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), sharex=True,
                                   gridspec_kw={"height_ratios": [3, 1.3], "hspace": 0.08})
    fig.patch.set_facecolor(SURFACE)

    for ax in (ax1, ax2):
        ax.set_facecolor(SURFACE)
        ax.grid(axis="y", color=GRID, linewidth=0.8)
        ax.tick_params(colors=INK_SOFT, length=0)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(GRID)

    # --- top panel: growth of $100 ---
    ax1.axhline(100, color=INK_SOFT, linewidth=0.8, linestyle=(0, (2, 3)))
    for t in [settings.MARKET_BENCHMARK, settings.SECTOR_BENCHMARK, TICKER]:   # Stryker drawn last = on top
        ax1.plot(rebased.index, rebased[t], color=COLOURS[t], linewidth=2.4 if t == TICKER else 1.8,
                 label=LABELS[t])

    # Direct labels at the right end of each line, nudged apart so they never overlap
    ends = rebased.iloc[-1].sort_values()
    min_gap = (rebased.max().max() - rebased.min().min()) * 0.05
    label_y, previous = {}, -float("inf")
    for t, value in ends.items():
        label_y[t] = max(value, previous + min_gap)
        previous = label_y[t]
    for t, value in ends.items():
        ax1.annotate(f"{LABELS[t].split(' (')[0]}  {value:.0f}", xy=(rebased.index[-1], value),
                     xytext=(rebased.index[-1] + pd.Timedelta(days=12), label_y[t]),
                     va="center", color=INK, fontsize=9.5)

    ax1.set_ylabel("Value of $100 invested", color=INK_SOFT)
    ax1.legend(loc="upper left", frameon=False, labelcolor=INK)
    ax1.set_title(f"Stryker vs the market and its sector: $100 invested "
                  f"{closes.index[0]:%b %Y} – {closes.index[-1]:%b %Y}",
                  loc="left", color=INK, fontsize=13, fontweight="bold", pad=12)

    # --- bottom panel: drawdown ---
    ax2.fill_between(dd.index, dd, 0, color=COLOURS[TICKER], alpha=0.25, linewidth=0)
    ax2.plot(dd.index, dd, color=COLOURS[TICKER], linewidth=1.4)
    ax2.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax2.set_ylabel("Stryker below\nits peak", color=INK_SOFT)
    ax2.annotate(f"Worst fall {worst['max_drawdown']:.0%}\n"
                 f"{worst['peak_date']:%b %Y} → {worst['trough_date']:%b %Y}",
                 xy=(worst["trough_date"], worst["max_drawdown"]), xytext=(-230, 10),
                 textcoords="offset points", color=INK, fontsize=9,
                 arrowprops={"arrowstyle": "-", "color": INK_SOFT, "linewidth": 0.8})
    ax2.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

    fig.text(0.01, 0.005, "Source: Yahoo Finance, prices adjusted for dividends and splits. "
             "Stryker is the pipeline test company, not a pick.", color=INK_SOFT, fontsize=8)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)


# ---------------------------------------------------------------------------
def main() -> None:
    for folder in (settings.TABLES_DIR, settings.CHARTS_DIR):
        folder.mkdir(parents=True, exist_ok=True)

    print("Downloading prices...")
    closes = data.load_close_prices([TICKER, settings.MARKET_BENCHMARK, settings.SECTOR_BENCHMARK])
    print(f"  {len(closes)} trading days, {closes.index[0]:%d %b %Y} to {closes.index[-1]:%d %b %Y}")

    print("Downloading financial statements...")
    statements = data.download_financials(TICKER)

    check = check_against_10k(statements)
    check.to_csv(settings.TABLES_DIR / f"{TICKER}_10K_check.csv", index=False)
    print("\nYahoo vs 10-K (FY2025):")
    print(check.to_string(index=False))

    prices_table, business = snapshot(closes, statements)
    prices_table.to_csv(settings.TABLES_DIR / f"{TICKER}_price_snapshot.csv")
    business.to_csv(settings.TABLES_DIR / f"{TICKER}_business_snapshot.csv", header=["value"])
    print("\nPrice behaviour:")
    print(prices_table.to_string(formatters={c: "{:.1%}".format for c in prices_table.columns[:4]}))
    print("\nBusiness:")
    print(business.round(3).to_string())

    chart = settings.CHARTS_DIR / "01_stryker_vs_benchmarks.png"
    plot_vs_benchmarks(closes, chart)
    print(f"\nChart saved to {chart.relative_to(settings.PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
