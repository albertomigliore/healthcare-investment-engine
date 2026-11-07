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
