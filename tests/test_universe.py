"""Checks on the eligibility rules (README section 3)."""
import pandas as pd

from src import universe

VD = "2026-11-06"
EVENTS = pd.DataFrame(
    [{"ticker": "TAKE", "event": "Agreed takeover", "status_at_valuation_date": "Pending",
      "decision": "OUT", "reason": "Pending takeover"},
     {"ticker": "SOLD", "event": "Sold a division", "status_at_valuation_date": "Completed",
      "decision": "IN (flagged)", "reason": "Still mainly devices"}]).set_index("ticker")


def prices(start="2023-11-06", end=VD, last=100.0):
    idx = pd.bdate_range(start, end)
    return pd.Series(last, index=idx)


def fundamentals(op_income=500.0, fcf=400.0, shares=100e6, years=4):
    idx = pd.to_datetime([f"{2022 + i}-12-31" for i in range(years)])
    return pd.DataFrame({"operating_income": op_income, "free_cash_flow": fcf, "shares": shares}, index=idx)


def test_healthy_company_is_in():
    row = universe.check_company("OK", prices(), fundamentals(), "USD", EVENTS, VD)
    assert row["eligible"]
    assert row["market_cap_bn"] == 10.0               # $100 x 100m shares


def test_pending_takeover_is_out():
    row = universe.check_company("TAKE", prices(), fundamentals(), "USD", EVENTS, VD)
    assert not row["eligible"] and "takeover" in row["reason_if_out"]


def test_flagged_event_stays_in():
    assert universe.check_company("SOLD", prices(), fundamentals(), "USD", EVENTS, VD)["eligible"]


def test_delisted_company_is_out():
    row = universe.check_company("GONE", None, None, None, EVENTS, VD)
    assert not row["eligible"] and "Rule 1" in row["reason_if_out"]


def test_stopped_trading_before_valuation_date_is_out():
    row = universe.check_company("OLD", prices(end="2026-06-09"), fundamentals(), "USD", EVENTS, VD)
    assert "Rule 1" in row["reason_if_out"]


def test_small_company_is_out():
    row = universe.check_company("SMALL", prices(last=10.0), fundamentals(), "USD", EVENTS, VD)
    assert "Rule 2" in row["reason_if_out"]           # $10 x 100m = $1bn


def test_short_history_is_out():
    row = universe.check_company("NEW", prices(start="2024-06-03"), fundamentals(), "USD", EVENTS, VD)
    assert "Rule 3" in row["reason_if_out"]


def test_too_few_annual_reports_is_out():
    row = universe.check_company("FEW", prices(), fundamentals(years=3), "USD", EVENTS, VD)
    assert "Rule 3" in row["reason_if_out"]


def test_operating_loss_or_negative_fcf_is_out():
    assert "Rule 4" in universe.check_company("L", prices(), fundamentals(op_income=-1), "USD", EVENTS, VD)["reason_if_out"]
    assert "Rule 4" in universe.check_company("C", prices(), fundamentals(fcf=-1), "USD", EVENTS, VD)["reason_if_out"]


def test_non_usd_reporter_is_out():
    row = universe.check_company("EUR", prices(), fundamentals(), "EUR", EVENTS, VD)
    assert "Rule 5" in row["reason_if_out"]
