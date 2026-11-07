"""Checks on reading the official 10-K data (SEC XBRL), using small made-up filings."""
import pandas as pd

from src import sec


def fact(start, end, val, filed, form="10-K", accn="x"):
    return {"start": start, "end": end, "val": val, "filed": filed, "form": form, "accn": accn}


def facts_with(revenue_facts, tag="Revenues"):
    return {"facts": {"us-gaap": {tag: {"units": {"USD": revenue_facts}}}}}


def years_table(*years):
    return pd.DataFrame({"revenue": 1.0}, index=pd.to_datetime([f"{y}-12-31" for y in years]))


# --- annual_value -------------------------------------------------------------
def test_picks_full_year_from_10k_and_ignores_quarters_and_10q():
    facts = facts_with([
        fact("2025-10-01", "2025-12-31", 25, "2026-02-01"),               # a quarter
        fact("2025-01-01", "2025-12-31", 999, "2025-11-01", form="10-Q"),  # wrong form
        fact("2025-01-01", "2025-12-31", 100, "2026-02-01"),               # the one we want
    ])
    assert sec.annual_value(facts, ["Revenues"], pd.Timestamp("2025-12-31"))["value"] == 100


def test_tolerates_52_53_week_years():
    # Year ending on the last Friday of April, Yahoo shows 30 April
    facts = facts_with([fact("2025-04-26", "2026-04-24", 100, "2026-06-20")])
    assert sec.annual_value(facts, ["Revenues"], pd.Timestamp("2026-04-30"))["value"] == 100


def test_uses_latest_filing_when_a_year_is_repeated():
    facts = facts_with([fact("2024-01-01", "2024-12-31", 90, "2025-02-01"),
                        fact("2024-01-01", "2024-12-31", 80, "2026-02-01")])   # restated later
    assert sec.annual_value(facts, ["Revenues"], pd.Timestamp("2024-12-31"))["value"] == 80


def test_tries_tags_in_order():
    facts = facts_with([fact("2025-01-01", "2025-12-31", 100, "2026-02-01")], tag="SalesRevenueNet")
    found = sec.annual_value(facts, sec.TAGS["revenue"], pd.Timestamp("2025-12-31"))
    assert found["tag"] == "SalesRevenueNet"


# --- comparable_growth_years ---------------------------------------------------
def test_full_window_when_nothing_restated():
    facts = facts_with([fact(f"{y}-01-01", f"{y}-12-31", 100, f"{y + 1}-02-01") for y in range(2022, 2026)])
    assert sec.comparable_growth_years(facts, years_table(2022, 2023, 2024, 2025), 3) == (3, "")


def test_full_window_when_base_year_was_also_restated():
    # Like Edwards: 2022 and 2023 both re-reported without the sold business
    facts = facts_with([
        fact("2022-01-01", "2022-12-31", 150, "2023-02-01"), fact("2022-01-01", "2022-12-31", 100, "2025-02-01"),
        fact("2023-01-01", "2023-12-31", 160, "2024-02-01"), fact("2023-01-01", "2023-12-31", 110, "2025-02-01"),
        fact("2024-01-01", "2024-12-31", 120, "2025-02-01"), fact("2025-01-01", "2025-12-31", 130, "2026-02-01"),
    ])
    assert sec.comparable_growth_years(facts, years_table(2022, 2023, 2024, 2025), 3)[0] == 3


def test_shorter_window_when_base_year_never_restated():
    # Like Teleflex: 2023 restated, 2022 never was -> 2023-2025 is the like-for-like window
    facts = facts_with([
        fact("2022-01-01", "2022-12-31", 2791, "2023-02-01"),
        fact("2023-01-01", "2023-12-31", 2974, "2024-02-01"), fact("2023-01-01", "2023-12-31", 1712, "2026-02-01"),
        fact("2024-01-01", "2024-12-31", 3047, "2025-02-01"), fact("2024-01-01", "2024-12-31", 1700, "2026-02-01"),
        fact("2025-01-01", "2025-12-31", 1993, "2026-02-01"),
    ])
    years, note = sec.comparable_growth_years(facts, years_table(2022, 2023, 2024, 2025), 3)
    assert years == 2
    assert "not like-for-like" in note
