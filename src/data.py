"""
Getting data in, and keeping it honest.

Rules from README section 5:
- raw downloads are saved untouched in data/raw/, with the download date in the file name
- a missing number stays missing (never replaced with zero)
"""
import warnings
from pathlib import Path

import pandas as pd
import yfinance as yf

from config import settings


def _today() -> str:
    return pd.Timestamp.today().strftime("%Y-%m-%d")


def _end_date_exclusive(valuation_date: str) -> str:
    """Yahoo's `end` date is NOT included, so ask for the day after the valuation date."""
    return (pd.Timestamp(valuation_date) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")


# ---------------------------------------------------------------------------
# Prices
# ---------------------------------------------------------------------------
def download_prices(ticker: str,
                    start: str = settings.PRICE_START,
                    valuation_date: str = settings.VALUATION_DATE,
                    save: bool = True) -> pd.DataFrame:
    """
    Daily prices for one ticker, adjusted for dividends and splits.
    Saves the untouched download to data/raw/{TICKER}_prices_downloaded_{date}.csv.
    """
    prices = yf.download(ticker, start=start, end=_end_date_exclusive(valuation_date),
                         auto_adjust=True, progress=False, multi_level_index=False)
    if prices.empty:
        raise ValueError(f"No price data returned for {ticker}")
    if save:
        settings.RAW_DIR.mkdir(parents=True, exist_ok=True)
        prices.to_csv(settings.RAW_DIR / f"{ticker}_prices_downloaded_{_today()}.csv")
    return prices


def drop_unfinished_day(prices: pd.DataFrame, downloaded_at: pd.Timestamp | None = None) -> pd.DataFrame:
    """
    If the data was downloaded while the US market was still open, the last row
    is a price from the middle of the day, not a closing price. Remove it and
    say so loudly.

    Found in Session 1: a download at 17:04 UK time (12:04 New York) gave a
    "closing" price for 6 Nov 2026 on a quarter of the normal volume.

    `downloaded_at` defaults to now (a fresh download). For a file loaded from
    disk, pass the time the file was written.
    """
    tz = settings.MARKET_TIMEZONE
    downloaded_at = pd.Timestamp.now(tz=tz) if downloaded_at is None else downloaded_at.tz_convert(tz)
    last_day = prices.index[-1]
    settled = pd.Timestamp(f"{last_day:%Y-%m-%d} {settings.MARKET_CLOSE_TIME}", tz=tz)
    if downloaded_at < settled:
        warnings.warn(
            f"Last row ({last_day:%Y-%m-%d}) was downloaded at {downloaded_at:%H:%M} New York time, "
            f"before the close had settled ({settings.MARKET_CLOSE_TIME}). It is an intraday "
            f"price, so it is dropped. Re-download after the close to include it.",
            stacklevel=2,
        )
        return prices.iloc[:-1]
    return prices


def load_close_prices(tickers: list[str], download: bool = True) -> pd.DataFrame:
    """
    One table of closing prices: one column per ticker, one row per trading day.
    `download=False` uses the latest saved raw file instead of downloading.
    Unfinished trading days are removed either way (see drop_unfinished_day),
    and an empty last close is filled from the quote feed if possible
    (see fill_missing_last_close).
    """
    closes, quotes_used = {}, []
    for ticker in tickers:
        if download:
            prices = drop_unfinished_day(download_prices(ticker))
        else:
            path = latest_raw_path(ticker, "prices")
            written_at = pd.Timestamp(path.stat().st_mtime, unit="s", tz="UTC")
            prices = drop_unfinished_day(pd.read_csv(path, index_col=0, parse_dates=True), written_at)
        close, quote = fill_missing_last_close(ticker, prices["Close"])
        if quote:
            quotes_used.append(quote)
        closes[ticker] = close
    if quotes_used:
        settings.RAW_DIR.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(quotes_used).to_csv(settings.RAW_DIR / f"quote_closes_downloaded_{_today()}.csv", index=False)
    return pd.DataFrame(closes)


def quote_close(ticker: str) -> tuple[float, pd.Timestamp]:
    """Yahoo's quote feed: last regular-session price and the time it was set (New York time)."""
    info = yf.Ticker(ticker).info
    price, ts = info.get("regularMarketPrice"), info.get("regularMarketTime")
    if price is None or ts is None:
        return float("nan"), pd.NaT
    return float(price), pd.Timestamp(ts, unit="s", tz="UTC").tz_convert(settings.MARKET_TIMEZONE)


def fill_missing_last_close(ticker: str, close: pd.Series, quote=None) -> tuple[pd.Series, dict | None]:
    """
    Found in Session 3: on Saturday 7 Nov 2026 Yahoo's price history returned an
    empty close for Friday 6 Nov (volume present, prices missing) for every ticker.

    On the most recent day, an adjusted close equals the actual close (adjustment
    only rescales *earlier* prices), so the gap can be filled from Yahoo's quote
    feed, a separate system. This is done only if the quote was set on that same
    day after the market closed; otherwise the empty day is dropped. The quote
    feed was checked against three known 6 Nov closes (SYK, SPY, IHI): exact match.

    `quote` can be passed in as (price, time) for testing; otherwise it is fetched.
    Returns the (possibly filled) series and a record of the quote used, or None.
    """
    close = close.copy()
    last_day = close.index[-1]
    if pd.notna(close.iloc[-1]):
        return close, None
    price, ts = quote if quote is not None else quote_close(ticker)
    close_time = pd.Timestamp(f"{last_day:%Y-%m-%d} 16:00", tz=settings.MARKET_TIMEZONE)
    if pd.notna(price) and pd.notna(ts) and ts.date() == last_day.date() and ts >= close_time:
        close.iloc[-1] = price
        return close, {"ticker": ticker, "date": f"{last_day:%Y-%m-%d}", "close": price,
                       "quote_time_new_york": f"{ts:%Y-%m-%d %H:%M}", "source": "Yahoo quote feed (regularMarketPrice)"}
    warnings.warn(f"{ticker}: empty close on {last_day:%Y-%m-%d} and no valid quote to fill it. Day dropped.",
                  stacklevel=2)
    return close.iloc[:-1], None


# ---------------------------------------------------------------------------
# Financial statements
# ---------------------------------------------------------------------------
STATEMENTS = {
    "income": "income_stmt",
    "balance": "balance_sheet",
    "cashflow": "cashflow",
}


def download_financials(ticker: str, save: bool = True) -> dict[str, pd.DataFrame]:
    """
    The three annual financial statements from Yahoo Finance, in plain US dollars.
    Rows are line items ("Total Revenue"...), columns are financial years.
    """
    stock = yf.Ticker(ticker)
    statements = {}
    for name, attribute in STATEMENTS.items():
        table = getattr(stock, attribute)
        if table is None or table.empty:
            raise ValueError(f"No {name} statement returned for {ticker}")
        if save:
            settings.RAW_DIR.mkdir(parents=True, exist_ok=True)
            table.to_csv(settings.RAW_DIR / f"{ticker}_{name}_downloaded_{_today()}.csv")
        # Drop financial years where (almost) everything is missing.
        # Seen in Session 1: Yahoo's oldest column for SYK was 45/46 empty.
        mostly_empty = table.isna().mean() > 0.9
        statements[name] = table.loc[:, ~mostly_empty]
    return statements


def load_financials(ticker: str, download: bool = False) -> dict[str, pd.DataFrame]:
    """
    The three statements, from the latest saved raw files (or a fresh download
    if there are none, or if download=True).
    """
    if download:
        return download_financials(ticker)
    try:
        return {name: load_latest_raw(ticker, name) for name in STATEMENTS}
    except FileNotFoundError:
        return download_financials(ticker)


# ---------------------------------------------------------------------------
# Interest rates (FRED)
# ---------------------------------------------------------------------------
FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"


def download_fred(series: str, save: bool = True) -> pd.Series:
    """
    A daily interest-rate series from FRED, converted from percent to a decimal
    (4.25 -> 0.0425). Days without a value (holidays) stay missing.
    """
    raw = pd.read_csv(FRED_URL.format(series=series), index_col=0, parse_dates=True, na_values=".")
    if save:
        settings.RAW_DIR.mkdir(parents=True, exist_ok=True)
        raw.to_csv(settings.RAW_DIR / f"FRED_{series}_downloaded_{_today()}.csv")
    return raw.iloc[:, 0] / 100


def risk_free_rates(price_start: str = settings.PRICE_START,
                    valuation_date: str = settings.VALUATION_DATE) -> pd.DataFrame:
    """
    3-month T-bill: average over the 3-year price window (it is compared with a
    3-year average return in the Sharpe ratio).
    10-year Treasury: latest value on or before the valuation date (for the DCF).
    Row 0 is the Sharpe rate; row 2 is the DCF rate.
    """
    start, vd = pd.Timestamp(price_start), pd.Timestamp(valuation_date)
    short = download_fred(settings.RISK_FREE_SHORT).loc[start:vd].dropna()
    long = download_fred(settings.RISK_FREE_LONG).loc[:vd].dropna()
    return pd.DataFrame([
        {"rate": "3-month T-bill (Sharpe)", "series": settings.RISK_FREE_SHORT,
         "value": short.mean(), "basis": f"average {short.index[0]:%d %b %Y} – {short.index[-1]:%d %b %Y}"},
        {"rate": "3-month T-bill, latest", "series": settings.RISK_FREE_SHORT,
         "value": short.iloc[-1], "basis": f"as of {short.index[-1]:%d %b %Y}"},
        {"rate": "10-year Treasury (DCF)", "series": settings.RISK_FREE_LONG,
         "value": long.iloc[-1], "basis": f"as of {long.index[-1]:%d %b %Y}"},
    ])


# ---------------------------------------------------------------------------
# Reading saved raw files back
# ---------------------------------------------------------------------------
def latest_raw_path(ticker: str, kind: str) -> Path:
    """Path of the most recent raw download of a given kind ("prices", "income", ...)."""
    files = sorted(settings.RAW_DIR.glob(f"{ticker}_{kind}_downloaded_*.csv"))
    if not files:
        raise FileNotFoundError(f"No raw '{kind}' file for {ticker} in {settings.RAW_DIR}")
    return files[-1]


def load_latest_raw(ticker: str, kind: str) -> pd.DataFrame:
    """Load the most recent raw download of a given kind ("prices", "income", ...)."""
    return pd.read_csv(latest_raw_path(ticker, kind), index_col=0, parse_dates=(kind == "prices"))
