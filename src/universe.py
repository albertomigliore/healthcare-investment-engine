"""
Which companies are in the screen? (README section 3)

Every rule is checked the same way for every company, and the result of every
check is kept, so the table shows *why* a company is in or out.

Rules checked from data:
  1. Still listed: prices up to the valuation date.
  2. Market value above $5bn on the valuation date.
  3. At least 3 years of price history and 4 annual reports.
  4. Not loss-making: latest-year operating income and free cash flow both positive.
     (Clarified in Session 3, before any results: losses make a DCF meaningless;
      a net loss caused only by a one-off write-down does not.)
  5. Reports in US dollars.
Rules checked from the corporate-events file (data/manual/corporate_events.csv):
  6. Not delisted or under a pending agreed takeover.
Rule judged when the list was written (README section 3), not re-checked here:
  devices are the main business (more than about half of revenue).
"""
import pandas as pd

from config import settings

MIN_MARKET_CAP = 5e9
MIN_HISTORY_DAYS = 7          # first price may be up to a week after the window start (holidays)


def load_corporate_events() -> pd.DataFrame:
    return pd.read_csv(settings.MANUAL_DIR / "corporate_events.csv").set_index("ticker")


def check_company(ticker: str,
                  close: pd.Series | None,
                  fundamentals: pd.DataFrame | None,
                  currency: str | None,
                  events: pd.DataFrame,
                  valuation_date: str = settings.VALUATION_DATE) -> dict:
    """One row of the eligibility table: every check, its result, and the final decision."""
    vd = pd.Timestamp(valuation_date)
    row = {"ticker": ticker}
    reasons = []

    # 6. Corporate events (checked first: a delisted company has no data to check)
    if ticker in events.index:
        event = events.loc[ticker]
        row["corporate_event"] = f"{event['event']} ({event['status_at_valuation_date']})"
        if event["decision"] == "OUT":
            reasons.append(event["reason"])
    else:
        row["corporate_event"] = ""

    # 1 & 3. Listed, with 3 years of prices
    has_prices = close is not None and not close.dropna().empty
    if has_prices:
        close = close.dropna()
        row["first_price"] = f"{close.index[0]:%Y-%m-%d}"
        row["last_price_date"] = f"{close.index[-1]:%Y-%m-%d}"
        listed = close.index[-1] == vd
        enough_history = (close.index[0] - pd.Timestamp(settings.PRICE_START)).days <= MIN_HISTORY_DAYS
    else:
        row["first_price"] = row["last_price_date"] = None
        listed = enough_history = False
    if not listed and not reasons:
        reasons.append("Rule 1: no price on the valuation date (not listed)")
    if has_prices and not enough_history:
        reasons.append("Rule 3: less than 3 years of price history")

    # 3. Four annual reports
    n_years = 0 if fundamentals is None else len(fundamentals)
    row["annual_reports"] = n_years
    if fundamentals is not None and n_years < settings.GROWTH_YEARS + 1:
        reasons.append(f"Rule 3: only {n_years} annual reports (need {settings.GROWTH_YEARS + 1})")

    # 2, 4 & 5 need both prices and statements
    if has_prices and fundamentals is not None and n_years:
        latest = fundamentals.iloc[-1]
        market_cap = close.iloc[-1] * latest["shares"]
        row["market_cap_bn"] = round(market_cap / 1e9, 1)
        row["operating_income_m"] = round(latest["operating_income"] / 1e6)
        row["free_cash_flow_m"] = round(latest["free_cash_flow"] / 1e6)
        if not market_cap >= MIN_MARKET_CAP:
            reasons.append("Rule 2: market value below $5bn")
        if not latest["operating_income"] > 0:
            reasons.append("Rule 4: operating loss in the latest year")
        if not latest["free_cash_flow"] > 0:
            reasons.append("Rule 4: negative free cash flow in the latest year")
    row["currency"] = currency
    if currency is not None and currency != "USD":
        reasons.append(f"Rule 5: reports in {currency}, not USD")

    row["eligible"] = not reasons
    row["reason_if_out"] = "; ".join(reasons)
    return row
