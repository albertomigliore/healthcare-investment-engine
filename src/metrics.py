"""
The formulas. Each function does one calculation, with no downloading and no
printing, so each one can be tested on its own (see tests/test_metrics.py).

Two rules apply everywhere:
- A number that can't be calculated meaningfully comes back as NaN (missing),
  never as zero or as a misleading value (README section 5).
- Money amounts can be in any unit (dollars, millions) as long as the inputs
  of one formula use the same unit.
"""
import numpy as np
import pandas as pd


def _missing(*values) -> bool:
    """True if any input is missing (None or NaN)."""
    return any(v is None or pd.isna(v) for v in values)


# ===========================================================================
# GROWTH
# ===========================================================================
def cagr(value_now: float, value_before: float, years: float) -> float:
    """
    Compound annual growth rate: the steady yearly growth that turns
    `value_before` into `value_now` over `years` years.

        (value_now / value_before) ** (1 / years) - 1

    Growth from a negative or zero starting value has no meaning, so we return
    NaN (missing) instead of a misleading number (README section 7).
    """
    if _missing(value_now, value_before, years):
        return np.nan
    if value_before <= 0 or value_now <= 0:
        return np.nan
    return (value_now / value_before) ** (1 / years) - 1


# ===========================================================================
# QUALITY
# ===========================================================================
def effective_tax_rate(tax: pd.Series, pretax_income: pd.Series,
                       cap: float = 0.35, fallback: float = 0.21) -> float:
    """
    The share of pre-tax profit actually paid as tax, pooled over several years:

        total tax / total pre-tax profit

    Pooling smooths out one-off years. If total pre-tax profit is negative or
    missing, the rate is meaningless and `fallback` is used. Results are kept
    between 0 and `cap`.
    """
    total_tax, total_pretax = tax.sum(min_count=1), pretax_income.sum(min_count=1)
    if _missing(total_tax, total_pretax) or total_pretax <= 0:
        return fallback
    return float(np.clip(total_tax / total_pretax, 0.0, cap))


def roic(operating_income: float, tax_rate: float,
         debt: float, equity: float, cash: float) -> float:
    """
    Return on invested capital: the after-tax operating profit earned on each
    dollar put into the business by lenders and shareholders.

        operating income x (1 - tax rate) / (debt + equity - cash)

    Missing if invested capital is zero or negative (the ratio would be meaningless).
    """
    if _missing(operating_income, tax_rate, debt, equity, cash):
        return np.nan
    invested_capital = debt + equity - cash
    if invested_capital <= 0:
        return np.nan
    return operating_income * (1 - tax_rate) / invested_capital


def free_cash_flow(operating_cash_flow: float, capital_expenditure: float) -> float:
    """
    Cash from operations minus spending on equipment.
    Capex is subtracted whatever its sign in the source (Yahoo stores it as negative).
    """
    if _missing(operating_cash_flow, capital_expenditure):
        return np.nan
    return operating_cash_flow - abs(capital_expenditure)


def fcf_margin(fcf: float, revenue: float) -> float:
    """Out of every $1 of sales, how much is left as free cash: FCF / revenue."""
    if _missing(fcf, revenue) or revenue <= 0:
        return np.nan
    return fcf / revenue


def net_debt_to_ebitda(debt: float, cash: float, ebitda: float) -> float:
    """
    Years of earnings needed to pay off the debt: (debt - cash) / EBITDA.
    Can be negative (more cash than debt), which is good.
    Missing if EBITDA is zero or negative (the ratio would flip meaning).
    """
    if _missing(debt, cash, ebitda) or ebitda <= 0:
        return np.nan
    return (debt - cash) / ebitda


# ===========================================================================
# VALUE
# ===========================================================================
def enterprise_value(market_cap: float, debt: float, cash: float) -> float:
    """What it costs to buy the whole company: shares + debt taken on - cash received."""
    if _missing(market_cap, debt, cash):
        return np.nan
    return market_cap + debt - cash


def ev_to_ebitda(ev: float, ebitda: float) -> float:
    """Years of earnings you pay for the whole company. Missing if EBITDA <= 0."""
    if _missing(ev, ebitda) or ebitda <= 0:
        return np.nan
    return ev / ebitda


def fcf_yield(fcf: float, market_cap: float) -> float:
    """The cash return on the share price: FCF / market value of the shares."""
    if _missing(fcf, market_cap) or market_cap <= 0:
        return np.nan
    return fcf / market_cap


# ===========================================================================
# PRICES: returns and momentum
# ===========================================================================
def price_on(prices: pd.Series, date) -> float:
    """
    The closing price on `date`, or on the last trading day before it if the
    market was closed that day (weekend, holiday).
    """
    available = prices.dropna().loc[:pd.Timestamp(date)]
    if available.empty:
        return np.nan
    return available.iloc[-1]


def return_between(prices: pd.Series, start, end) -> float:
    """Return from `start` to `end`: price at end / price at start - 1."""
    return price_on(prices, end) / price_on(prices, start) - 1


def momentum_12_1(prices: pd.Series, as_of) -> float:
    """
    Last year's trend, skipping the most recent month (very recent moves tend
    to reverse): price 1 month ago / price 12 months ago - 1.
    """
    as_of = pd.Timestamp(as_of)
    return return_between(prices, as_of - pd.DateOffset(months=12), as_of - pd.DateOffset(months=1))


def relative_return(prices: pd.Series, benchmark: pd.Series, start, end) -> float:
    """How much the stock beat (+) or trailed (-) a benchmark between two dates."""
    return return_between(prices, start, end) - return_between(benchmark, start, end)


def total_return(prices: pd.Series) -> float:
    """Return from the first to the last price: last / first - 1."""
    prices = prices.dropna()
    return prices.iloc[-1] / prices.iloc[0] - 1


def annualised_return(prices: pd.Series) -> float:
    """The steady yearly return that matches the total return over the period (a CAGR)."""
    prices = prices.dropna()
    years = (prices.index[-1] - prices.index[0]).days / 365.25
    return cagr(prices.iloc[-1], prices.iloc[0], years)


def rebase(prices: pd.DataFrame | pd.Series, start_value: float = 100) -> pd.DataFrame | pd.Series:
    """
    Rescale price series so they all start at 100. This puts a $300 stock and
    a $600 fund on the same scale: 121 means "up 21% since the start".
    """
    prices = prices.dropna()
    return prices / prices.iloc[0] * start_value


# ===========================================================================
# RISK
# ===========================================================================
def daily_returns(prices: pd.Series) -> pd.Series:
    """Percentage change from one trading day to the next."""
    return prices.dropna().pct_change().dropna()


def weekly_returns(prices: pd.Series) -> pd.Series:
    """Percentage change from one Friday close to the next (last trading day of each week)."""
    return prices.dropna().resample("W-FRI").last().pct_change().dropna()


def annualised_volatility(prices: pd.Series, periods_per_year: int = 252) -> float:
    """
    How much the price jumps around in a typical year:
    standard deviation of daily returns x sqrt(252).
    """
    return daily_returns(prices).std() * np.sqrt(periods_per_year)


def beta(prices: pd.Series, market_prices: pd.Series) -> float:
    """
    How much the stock tends to move when the market moves 1%, from weekly returns:

        covariance(stock, market) / variance(market)

    which is the slope of the line through a scatter of weekly stock returns
    against weekly market returns.
    """
    both = pd.concat([weekly_returns(prices), weekly_returns(market_prices)], axis=1).dropna()
    stock, market = both.iloc[:, 0], both.iloc[:, 1]
    return stock.cov(market) / market.var()


def sharpe_ratio(prices: pd.Series, risk_free_rate: float, periods_per_year: int = 252) -> float:
    """
    Return earned per unit of risk taken:
    (yearly return - risk-free rate) / yearly volatility.
    """
    return (annualised_return(prices) - risk_free_rate) / annualised_volatility(prices, periods_per_year)


def drawdown(prices: pd.Series) -> pd.Series:
    """
    For every day: how far the price is below its highest point so far.
    0 means "at a new high"; -0.25 means "25% below the previous peak".
    """
    running_peak = prices.cummax()
    return prices / running_peak - 1


def max_drawdown(prices: pd.Series) -> dict:
    """
    The biggest fall from a peak to a later low.

    Returns the size of the fall plus the peak and trough dates, because
    "-32% between July 2025 and September 2026" is more useful than "-32%".
    """
    prices = prices.dropna()
    dd = drawdown(prices)
    trough_date = dd.idxmin()
    peak_date = prices.loc[:trough_date].idxmax()
    return {
        "max_drawdown": dd.min(),
        "peak_date": peak_date,
        "peak_price": prices.loc[peak_date],
        "trough_date": trough_date,
        "trough_price": prices.loc[trough_date],
    }
