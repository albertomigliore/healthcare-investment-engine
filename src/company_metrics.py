"""
The 12 screening metrics (README section 7) for one company.

`compute_company_metrics` returns two things:
- the metric values, ready for the ranking;
- the workings: every formula with the actual numbers plugged in, so each
  result can be checked by hand with a calculator.

The same function will run on all ~20 companies in Session 3.
"""
from dataclasses import dataclass, field

import pandas as pd

from config import settings
from src import metrics


@dataclass
class CompanyResult:
    ticker: str
    values: dict = field(default_factory=dict)     # metric key -> number
    workings: list = field(default_factory=list)   # one row per metric, for the hand check
    context: dict = field(default_factory=dict)    # supporting numbers (price, market cap, ...)

    def add(self, key: str, value: float, formula: str) -> None:
        self.values[key] = value
        spec = settings.METRICS.get(key, {"name": key, "group": "Reported only", "unit": ""})
        self.workings.append({
            "Group": spec["group"],
            "Metric": spec["name"],
            "Workings": formula,
            "Result": _fmt(value, spec["unit"]),
        })


# ---------------------------------------------------------------------------
# Formatting helpers for the workings ($ millions, percentages, multiples)
# ---------------------------------------------------------------------------
def _m(x: float) -> str:
    return "n/a" if pd.isna(x) else f"{x / 1e6:,.0f}"


def _pct(x: float) -> str:
    return "n/a" if pd.isna(x) else f"{x:.1%}"


def _fmt(x: float, unit: str) -> str:
    if pd.isna(x):
        return "n/a"
    if unit == "%":
        return f"{x:.1%}"
    return f"{x:.2f}{unit}"     # "x" for multiples (23.02x), nothing for beta (0.51)


# ---------------------------------------------------------------------------
def compute_company_metrics(ticker: str,
                            fundamentals: pd.DataFrame,
                            stock: pd.Series,
                            market: pd.Series,
                            sector: pd.Series,
                            valuation_date: str = settings.VALUATION_DATE,
                            risk_free_short: float = float("nan"),
                            growth_years: int = settings.GROWTH_YEARS) -> CompanyResult:
    """
    Parameters
    ----------
    fundamentals : output of fundamentals.extract_fundamentals (one row per year, oldest first)
    stock, market, sector : daily closing prices of the company, SPY and IHI
    risk_free_short : average 3-month T-bill rate over the price window (as a decimal)
    growth_years : normally 3; shorter only if the base year is not like-for-like
                   (see sec.comparable_growth_years)
    """
    result = CompanyResult(ticker)
    vd = pd.Timestamp(valuation_date)
    stock = stock.dropna().loc[:vd]

    latest = fundamentals.iloc[-1]
    fy = fundamentals.index[-1]
    m = growth_years
    base = fundamentals.iloc[-1 - m] if len(fundamentals) > m else None
    base_fy = fundamentals.index[-1 - m] if base is not None else None

    # Market value on the valuation date
    price = metrics.price_on(stock, vd)
    price_date = stock.index[-1]
    market_cap = price * latest["shares"]
    ev = metrics.enterprise_value(market_cap, latest["total_debt"], latest["cash"])

    def millions(x):
        return x if pd.isna(x) else round(x / 1e6)

    result.context = {
        "Financial year used": f"{fy:%Y} (ended {fy:%d %b %Y})",
        "Price date": f"{price_date:%d %b %Y}",
        "Share price ($)": round(price, 2),
        "Shares (m)": round(latest["shares"] / 1e6, 1),
        "Market cap ($m)": millions(market_cap),
        "Enterprise value ($m)": millions(ev),
        "EBITDA ($m)": millions(latest["ebitda"]),
        "Free cash flow ($m)": millions(latest["free_cash_flow"]),
    }

    # ---------------- QUALITY ----------------
    tax_years = fundamentals.iloc[-settings.TAX_RATE_YEARS:]
    tax_rate = metrics.effective_tax_rate(tax_years["tax"], tax_years["pretax_income"],
                                          cap=settings.TAX_RATE_CAP, fallback=settings.TAX_RATE_FALLBACK)
    result.context["Tax rate (pooled 3 yrs)"] = f"{tax_rate:.1%}"
    result.add("roic",
               metrics.roic(latest["operating_income"], tax_rate,
                            latest["total_debt"], latest["equity"], latest["cash"]),
               f"{_m(latest['operating_income'])} x (1 - {_pct(tax_rate)}) / "
               f"({_m(latest['total_debt'])} debt + {_m(latest['equity'])} equity - {_m(latest['cash'])} cash)")

    result.add("fcf_margin",
               metrics.fcf_margin(latest["free_cash_flow"], latest["revenue"]),
               f"({_m(latest['operating_cash_flow'])} op. cash flow - {_m(abs(latest['capital_expenditure']))} capex) "
               f"/ {_m(latest['revenue'])} revenue")

    result.add("net_debt_to_ebitda",
               metrics.net_debt_to_ebitda(latest["total_debt"], latest["cash"], latest["ebitda"]),
               f"({_m(latest['total_debt'])} debt - {_m(latest['cash'])} cash) / "
               f"({_m(latest['operating_income'])} op. income + {_m(latest['depreciation_amortisation'])} D&A)")

    # ---------------- GROWTH ----------------
    for key, col, label in [("revenue_cagr", "revenue", "revenue"),
                            ("operating_income_cagr", "operating_income", "op. income")]:
        if base is None:
            result.add(key, float("nan"), f"needs {m + 1} years of statements, only {len(fundamentals)} available")
        else:
            result.add(key, metrics.cagr(latest[col], base[col], m),
                       f"({_m(latest[col])} {label} {fy:%Y} / {_m(base[col])} in {base_fy:%Y}) ^ (1/{m}) - 1")

    # ---------------- VALUE ----------------
    result.add("ev_to_ebitda",
               metrics.ev_to_ebitda(ev, latest["ebitda"]),
               f"({_m(market_cap)} market cap + {_m(latest['total_debt'])} debt - {_m(latest['cash'])} cash) "
               f"/ {_m(latest['ebitda'])} EBITDA")

    result.add("fcf_yield",
               metrics.fcf_yield(latest["free_cash_flow"], market_cap),
               f"{_m(latest['free_cash_flow'])} FCF / {_m(market_cap)} market cap "
               f"(${price:.2f} x {latest['shares'] / 1e6:.1f}m shares)")

    # ---------------- MOMENTUM ----------------
    year_ago, month_ago = vd - pd.DateOffset(months=12), vd - pd.DateOffset(months=1)
    result.add("momentum_12_1",
               metrics.momentum_12_1(stock, vd),
               f"${metrics.price_on(stock, month_ago):.2f} ({month_ago:%d %b %Y}) / "
               f"${metrics.price_on(stock, year_ago):.2f} ({year_ago:%d %b %Y}) - 1")

    stock_12m = metrics.return_between(stock, year_ago, vd)
    sector_12m = metrics.return_between(sector, year_ago, vd)
    result.add("return_vs_sector",
               stock_12m - sector_12m,
               f"{ticker} {_pct(stock_12m)} minus IHI {_pct(sector_12m)} (12 months to {price_date:%d %b %Y})")

    # ---------------- RISK ----------------
    n_days = len(metrics.daily_returns(stock))
    result.add("volatility",
               metrics.annualised_volatility(stock, settings.TRADING_DAYS_PER_YEAR),
               f"std. dev. of {n_days} daily returns ({metrics.daily_returns(stock).std():.2%}) x sqrt(252)")

    n_weeks = len(pd.concat([metrics.weekly_returns(stock), metrics.weekly_returns(market)], axis=1).dropna())
    result.add("beta",
               metrics.beta(stock, market),
               f"covariance / variance of {n_weeks} weekly returns, {ticker} vs SPY")

    dd = metrics.max_drawdown(stock)
    result.add("max_drawdown",
               dd["max_drawdown"],
               f"${dd['trough_price']:.2f} ({dd['trough_date']:%d %b %Y}) / "
               f"${dd['peak_price']:.2f} peak ({dd['peak_date']:%d %b %Y}) - 1")

    # ---------------- REPORTED, NOT SCORED ----------------
    ann_return = metrics.annualised_return(stock)
    vol = result.values["volatility"]
    sharpe = metrics.sharpe_ratio(stock, risk_free_short, settings.TRADING_DAYS_PER_YEAR)
    result.values["sharpe"] = sharpe
    result.workings.append({
        "Group": "Reported only", "Metric": "Sharpe ratio",
        "Workings": f"({_pct(ann_return)} yearly return - {_pct(risk_free_short)} T-bill) / {_pct(vol)} volatility",
        "Result": f"{sharpe:.2f}",
    })
    return result
