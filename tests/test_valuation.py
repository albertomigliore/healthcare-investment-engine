"""Checks on the valuation engine, against answers known from textbook formulas."""
from dataclasses import replace

import numpy as np
import pandas as pd
import pytest

from src import valuation as v


def steady_company(**changes):
    """Revenue 1,000, 24% EBITDA margin (20% after 4% D&A), 25% tax, D&A = capex, no working capital, 5% growth forever."""
    base = v.DCFInputs(revenue0=1000, g1=0.05, g_term=0.05, margin0=0.24, margin_target=0.24, tax_rate=0.25,
                       da_pct0=0.04, capex_pct=0.04, nwc_pct=0.0, wacc=0.09, debt=200, cash=50, shares=10)
    return replace(base, **changes)


def test_constant_growth_dcf_equals_gordon_formula():
    # FCFF in year 1 = 1,050 x 20% x (1 - 25%) = 157.5; value of a growing perpetuity = 157.5 / (9% - 5%)
    out = v.dcf(steady_company())
    assert out["enterprise_value"] == pytest.approx(157.5 / (0.09 - 0.05))
    assert out["value_per_share"] == pytest.approx((157.5 / 0.04 - 200 + 50) / 10)


def test_working_capital_reduces_cash_flow():
    a = v.project(steady_company())
    b = v.project(steady_company(nwc_pct=0.20))
    assert b.loc[1, "change_nwc"] == pytest.approx(0.20 * 50)       # 20% of the 50 extra revenue
    assert b.loc[1, "fcff"] == pytest.approx(a.loc[1, "fcff"] - 10)


def test_growth_fades_to_terminal_and_margin_reaches_target():
    p = v.project(steady_company(g1=0.15, g_term=0.025, margin_target=0.30, years=10))
    assert p.loc[1, "growth"] == pytest.approx(0.15)
    assert p.loc[11, "growth"] == pytest.approx(0.025)
    assert p["growth"].is_monotonic_decreasing
    assert p.loc[10, "ebitda_margin"] == pytest.approx(0.30)


def test_da_converges_to_capex():
    p = v.project(steady_company(da_pct0=0.08, capex_pct=0.04, years=10))
    assert p.loc[10, "da"] == pytest.approx(p.loc[10, "capex"])


def test_amortisation_running_off_raises_operating_profit_not_cash():
    # Same EBITDA; D&A falls from 8% to 4%: operating profit rises, and only the extra tax reduces cash
    p = v.project(steady_company(margin0=0.24, margin_target=0.24, da_pct0=0.08, capex_pct=0.04, years=10))
    assert p.loc[10, "ebit"] / p.loc[10, "revenue"] == pytest.approx(0.20)
    assert p.loc[1, "ebit"] / p.loc[1, "revenue"] < 0.20


def test_higher_wacc_lowers_value():
    assert v.dcf(steady_company(wacc=0.10))["value_per_share"] < v.dcf(steady_company())["value_per_share"]


def test_wacc_arithmetic():
    w = v.wacc(risk_free=0.04, beta=1.0, erp=0.05, credit_spread=0.01, tax_rate=0.20, market_cap=800, debt=200)
    assert w["cost_of_equity"] == pytest.approx(0.09)
    assert w["cost_of_debt_after_tax"] == pytest.approx(0.04)
    assert w["wacc"] == pytest.approx(0.8 * 0.09 + 0.2 * 0.04)


def test_adjusted_beta_pulls_towards_one():
    assert v.adjusted_beta(1.5) == pytest.approx(0.67 * 1.5 + 0.33)
    assert v.adjusted_beta(1.0) == pytest.approx(1.0)


def test_vectorised_dcf_matches_table_dcf():
    i = steady_company(g1=0.12, g_term=0.025, margin_target=0.29, da_pct0=0.07, nwc_pct=0.3)
    single = v.dcf(i)["value_per_share"]
    many = v.value_per_share_vectorised(i, [0.12], [0.29], [0.09], [0.025])
    assert many[0] == pytest.approx(single)


def test_reverse_dcf_recovers_the_growth_behind_a_price():
    i = steady_company(g1=0.10, g_term=0.025, margin_target=0.25)
    price = v.dcf(i)["value_per_share"]
    assert v.implied_growth(replace(i, g1=0.0), price) == pytest.approx(0.10, abs=1e-4)


def test_comparables():
    out = v.comparables_value(pd.Series([10.0, 12, 14]), metric=100, debt=200, cash=0, shares=10)
    assert out["mid"] == pytest.approx((12 * 100 - 200) / 10)
    assert out["low"] < out["mid"] < out["high"]


def test_decision_rule():
    rule = dict(buy_upside=0.15, buy_probability=0.65, sell_downside=0.15)
    assert v.decision(120, 0.70, 100, **rule) == "BUY"
    assert v.decision(120, 0.60, 100, **rule) == "HOLD"      # upside, but not confident enough
    assert v.decision(110, 0.90, 100, **rule) == "HOLD"      # confident, but not enough upside
    assert v.decision(84, 0.10, 100, **rule) == "SELL"


def test_monte_carlo_is_reproducible_and_centred():
    i = steady_company(g1=0.08, g_term=0.025, margin_target=0.22)
    bear = {"g1": 0.05, "margin_target": 0.19, "wacc": 0.10, "g_term": 0.02}
    bull = {"g1": 0.11, "margin_target": 0.25, "wacc": 0.08, "g_term": 0.03}
    a = v.monte_carlo(i, bear, bull, 5000, seed=7)
    b = v.monte_carlo(i, bear, bull, 5000, seed=7)
    pd.testing.assert_frame_equal(a, b)
    base = v.dcf(i)["value_per_share"]
    assert abs(a["value_per_share"].median() / base - 1) < 0.10
