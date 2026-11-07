"""Checks on the intraday guard (Session 1 finding: a mid-day price disguised as a close)."""
import pandas as pd
import pytest

from src import data

NY = "America/New_York"


def prices_ending(day):
    idx = pd.bdate_range(end=day, periods=3)
    return pd.DataFrame({"Close": [1.0, 2.0, 3.0]}, index=idx)


def test_drops_last_day_if_downloaded_during_trading():
    p = prices_ending("2026-11-06")
    with pytest.warns(UserWarning, match="intraday"):
        out = data.drop_unfinished_day(p, pd.Timestamp("2026-11-06 12:04", tz=NY))
    assert out.index[-1] == pd.Timestamp("2026-11-05")


def test_keeps_last_day_if_downloaded_after_close():
    p = prices_ending("2026-11-06")
    out = data.drop_unfinished_day(p, pd.Timestamp("2026-11-06 17:00", tz=NY))
    assert out.index[-1] == pd.Timestamp("2026-11-06")


def test_keeps_last_day_if_downloaded_on_a_later_day():
    p = prices_ending("2026-11-06")
    out = data.drop_unfinished_day(p, pd.Timestamp("2026-11-08 09:00", tz=NY))
    assert len(out) == 3


# --- empty last close (Session 3 finding) --------------------------------------
def close_with_empty_last_day():
    c = prices_ending("2026-11-06")["Close"]
    c.iloc[-1] = float("nan")
    return c


def test_fills_empty_last_close_from_a_quote_set_after_the_close():
    quote = (325.87, pd.Timestamp("2026-11-06 16:03", tz=NY))
    filled, record = data.fill_missing_last_close("SYK", close_with_empty_last_day(), quote)
    assert filled.iloc[-1] == 325.87
    assert record["source"].startswith("Yahoo quote feed")


def test_rejects_quote_from_another_day():
    quote = (330.0, pd.Timestamp("2026-11-09 16:03", tz=NY))    # Monday's price must not fill Friday
    with pytest.warns(UserWarning):
        filled, record = data.fill_missing_last_close("SYK", close_with_empty_last_day(), quote)
    assert filled.index[-1] == pd.Timestamp("2026-11-05") and record is None


def test_rejects_quote_set_before_the_close():
    quote = (320.0, pd.Timestamp("2026-11-06 12:00", tz=NY))
    with pytest.warns(UserWarning):
        filled, _ = data.fill_missing_last_close("SYK", close_with_empty_last_day(), quote)
    assert filled.index[-1] == pd.Timestamp("2026-11-05")


def test_leaves_complete_data_alone():
    c = prices_ending("2026-11-06")["Close"]
    filled, record = data.fill_missing_last_close("SYK", c, quote=(999.0, pd.Timestamp("2026-11-06 16:03", tz=NY)))
    assert filled.iloc[-1] == 3.0 and record is None
