"""
Automatic checks on the formulas, using tiny made-up examples where the right
answer is known in advance. Run from the project folder with:  python -m pytest
"""
import numpy as np
import pandas as pd
import pytest

from src import metrics


def make_prices(values):
    dates = pd.bdate_range("2024-01-01", periods=len(values))
    return pd.Series(values, index=dates, dtype=float)


# --- CAGR -------------------------------------------------------------------
def test_cagr_doubling_in_one_year_is_100_percent():
    assert metrics.cagr(200, 100, years=1) == pytest.approx(1.0)


def test_cagr_compounds_rather_than_averages():
    # 10% a year for 3 years: 100 -> 133.1. Simple average would wrongly say 11%.
    assert metrics.cagr(133.1, 100, years=3) == pytest.approx(0.10)


def test_cagr_is_missing_for_negative_or_zero_start():
    # README section 7: growth from a loss can't be calculated -> missing, not a number
    assert np.isnan(metrics.cagr(50, -10, years=3))
    assert np.isnan(metrics.cagr(50, 0, years=3))


def test_cagr_is_missing_when_input_missing():
    assert np.isnan(metrics.cagr(np.nan, 100, years=3))


# --- Returns ----------------------------------------------------------------
def test_total_return():
    assert metrics.total_return(make_prices([100, 90, 120])) == pytest.approx(0.20)


def test_volatility_is_zero_for_steady_growth():
    # Same +1% every day -> returns never vary -> zero volatility
    steady = make_prices(100 * 1.01 ** np.arange(50))
    assert metrics.annualised_volatility(steady) == pytest.approx(0.0, abs=1e-12)


def test_volatility_scales_with_square_root_of_252():
    # Alternating +10% / -10%-ish returns: check the annualisation factor
    p = make_prices([100, 110, 100, 110, 100])
    daily_std = p.pct_change().dropna().std()
    assert metrics.annualised_volatility(p) == pytest.approx(daily_std * np.sqrt(252))


# --- Drawdown ---------------------------------------------------------------
def test_max_drawdown_finds_peak_and_trough():
    p = make_prices([100, 150, 120, 75, 90, 160])
    dd = metrics.max_drawdown(p)
    assert dd["max_drawdown"] == pytest.approx(-0.50)    # 150 -> 75
    assert dd["peak_price"] == 150
    assert dd["trough_price"] == 75


def test_drawdown_is_zero_when_price_only_rises():
    assert metrics.drawdown(make_prices([1, 2, 3, 4])).min() == 0


def test_rebase_starts_at_100():
    rebased = metrics.rebase(make_prices([250, 300, 275]))
    assert rebased.iloc[0] == 100
    assert rebased.iloc[1] == pytest.approx(120)


# --- Quality ----------------------------------------------------------------
def test_roic_textbook_example():
    # 100 profit, 20% tax -> 80 after tax, on 400 + 600 - 200 = 800 invested -> 10%
    assert metrics.roic(100, 0.20, debt=400, equity=600, cash=200) == pytest.approx(0.10)


def test_roic_missing_when_invested_capital_not_positive():
    assert np.isnan(metrics.roic(100, 0.2, debt=0, equity=100, cash=500))


def test_effective_tax_rate_is_pooled_not_averaged():
    # Year rates 10% and 50%, but the big year dominates: (10 + 5) / (100 + 10) = 13.6%
    tax, pretax = pd.Series([10, 5]), pd.Series([100, 10])
    assert metrics.effective_tax_rate(tax, pretax) == pytest.approx(15 / 110)


def test_effective_tax_rate_falls_back_and_caps():
    assert metrics.effective_tax_rate(pd.Series([5]), pd.Series([-100])) == 0.21   # loss -> fallback
    assert metrics.effective_tax_rate(pd.Series([90]), pd.Series([100])) == 0.35   # 90% -> capped


def test_free_cash_flow_handles_either_capex_sign():
    assert metrics.free_cash_flow(500, -100) == 400   # Yahoo style (negative)
    assert metrics.free_cash_flow(500, 100) == 400    # 10-K style (positive payment)


def test_fcf_margin():
    assert metrics.fcf_margin(17, 100) == pytest.approx(0.17)


def test_net_debt_to_ebitda_can_be_negative_but_not_with_negative_ebitda():
    assert metrics.net_debt_to_ebitda(debt=100, cash=300, ebitda=100) == pytest.approx(-2.0)
    assert np.isnan(metrics.net_debt_to_ebitda(debt=300, cash=100, ebitda=-50))


# --- Value ------------------------------------------------------------------
def test_enterprise_value_and_multiple():
    ev = metrics.enterprise_value(market_cap=1000, debt=300, cash=100)
    assert ev == 1200
    assert metrics.ev_to_ebitda(ev, 100) == pytest.approx(12.0)
    assert np.isnan(metrics.ev_to_ebitda(ev, 0))


def test_fcf_yield():
    assert metrics.fcf_yield(50, 1000) == pytest.approx(0.05)


# --- Momentum ---------------------------------------------------------------
def daily_series(start, end, func):
    dates = pd.bdate_range(start, end)
    return pd.Series([func(d) for d in dates], index=dates, dtype=float)


def test_price_on_uses_last_trading_day_before_a_weekend():
    p = make_prices([10, 11, 12, 13, 14])          # Mon 1 Jan .. Fri 5 Jan 2024
    assert metrics.price_on(p, "2024-01-07") == 14  # Sunday -> Friday's price


def test_momentum_skips_the_last_month():
    # 50 until 12 months before as_of, then 100, then a jump to 1000 in the final month
    as_of = pd.Timestamp("2025-06-30")
    p = daily_series("2024-01-01", "2025-06-30",
                     lambda d: 50 if d <= as_of - pd.DateOffset(months=12)
                     else (100 if d <= as_of - pd.DateOffset(months=1) else 1000))
    assert metrics.momentum_12_1(p, as_of) == pytest.approx(1.0)   # 50 -> 100; the jump is ignored


def test_relative_return():
    p = make_prices([100, 120])
    bench = make_prices([100, 110])
    assert metrics.relative_return(p, bench, p.index[0], p.index[-1]) == pytest.approx(0.10)


# --- Risk: beta and annualised return ---------------------------------------
def random_walk(seed, n=800):
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2023-01-02", periods=n)
    return pd.Series(100 * np.exp(np.cumsum(rng.normal(0, 0.01, n))), index=dates)


def test_beta_of_market_with_itself_is_one():
    market = random_walk(1)
    assert metrics.beta(market, market) == pytest.approx(1.0)


def test_beta_of_double_returns_is_two():
    market = random_walk(2)
    weekly = market.resample("W-FRI").last()
    doubled = (1 + 2 * weekly.pct_change().fillna(0)).cumprod() * 100   # twice the market's move every week
    assert metrics.beta(doubled, market) == pytest.approx(2.0)


def test_beta_of_unrelated_stock_is_near_zero():
    assert abs(metrics.beta(random_walk(3), random_walk(4))) < 0.3


def test_annualised_return_over_exactly_two_years():
    p = pd.Series([100.0, 121.0], index=pd.to_datetime(["2023-01-01", "2025-01-01"]))
    assert metrics.annualised_return(p) == pytest.approx(0.10, abs=1e-3)


# --- Rolling (moving-window) risk -------------------------------------------
def test_rolling_volatility_is_zero_for_steady_growth_and_missing_before_window():
    steady = make_prices(100 * 1.001 ** np.arange(300))
    vol = metrics.rolling_volatility(steady, window=252)
    assert vol.iloc[:252].isna().all()                  # needs a full year of data first
    assert vol.iloc[-1] == pytest.approx(0.0, abs=1e-9)


def test_rolling_volatility_last_value_matches_last_year():
    p = random_walk(5, n=400)
    last_year = p.iloc[-253:]
    assert metrics.rolling_volatility(p, 252).iloc[-1] == pytest.approx(metrics.annualised_volatility(last_year))


def test_rolling_sharpe_matches_definition():
    p = random_walk(6, n=400)
    rf = pd.Series(0.04, index=p.index)
    expected = (p.iloc[-1] / p.iloc[-253] - 1 - 0.04) / metrics.annualised_volatility(p.iloc[-253:])
    assert metrics.rolling_sharpe(p, rf, 252).iloc[-1] == pytest.approx(expected)
