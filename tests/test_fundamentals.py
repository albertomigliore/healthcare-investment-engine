"""Checks that numbers are pulled from the right lines of the statements."""
import numpy as np
import pandas as pd

from src import fundamentals

YEARS = ["2022-12-31", "2023-12-31", "2024-12-31", "2025-12-31"]


def fake_statements(include_as_reported=True):
    income = pd.DataFrame({y: {
        "Total Revenue": 1000 + 100 * i,
        "Operating Income": 250,                    # Yahoo's adjusted figure
        "Pretax Income": 180,
        "Tax Provision": 36,
    } for i, y in enumerate(YEARS)})
    if include_as_reported:
        income.loc["Total Operating Income As Reported"] = 200
    cashflow = pd.DataFrame({y: {
        "Depreciation And Amortization": 50,
        "Operating Cash Flow": 300,
        "Capital Expenditure": -60,
    } for y in YEARS})
    balance = pd.DataFrame({y: {
        "Total Debt": 400, "Cash And Cash Equivalents": 100,
        "Stockholders Equity": 900, "Ordinary Shares Number": 50,
    } for y in YEARS})
    income["2021-12-31"] = np.nan                   # the near-empty oldest year seen on Yahoo
    return {"income": income, "balance": balance, "cashflow": cashflow}


def test_prefers_as_reported_operating_income():
    table, sources = fundamentals.extract_fundamentals(fake_statements())
    assert sources["operating_income"] == "Total Operating Income As Reported"
    assert (table["operating_income"] == 200).all()


def test_falls_back_and_flags_it():
    table, sources = fundamentals.extract_fundamentals(fake_statements(include_as_reported=False))
    assert sources["operating_income"] == "Operating Income"
    flags = fundamentals.missing_items(table, sources)
    assert any("fallback" in f and "operating_income" in f for f in flags)


def test_years_are_oldest_first_and_empty_year_dropped():
    table, _ = fundamentals.extract_fundamentals(fake_statements())
    assert list(table.index.year) == [2022, 2023, 2024, 2025]


def test_derived_items():
    table, _ = fundamentals.extract_fundamentals(fake_statements())
    latest = table.iloc[-1]
    assert latest["free_cash_flow"] == 240          # 300 - 60
    assert latest["ebitda"] == 250                  # 200 as-reported + 50 D&A
    assert latest["net_debt"] == 300                # 400 - 100


def test_override_fills_a_gap_but_never_replaces_a_value(tmp_path, monkeypatch):
    from config import settings
    (tmp_path / "overrides.csv").write_text(
        "ticker,item,fiscal_year_end,value,source,reason\n"
        "TEST,total_debt,2025-12-31,0,10-K,no borrowings\n"
        "TEST,cash,2025-12-31,999,10-K,should be ignored: Yahoo has a value\n")
    monkeypatch.setattr(settings, "MANUAL_DIR", tmp_path)
    s = fake_statements()
    s["balance"] = s["balance"].drop("Total Debt")
    table, sources = fundamentals.extract_fundamentals(s)
    table, notes = fundamentals.apply_overrides("TEST", table, sources)
    latest = table.iloc[-1]
    assert latest["total_debt"] == 0                # gap filled
    assert latest["cash"] == 100                    # existing value untouched
    assert latest["net_debt"] == -100               # derived item rebuilt
    assert len(notes) == 1


def test_missing_line_stays_missing_and_is_flagged():
    s = fake_statements()
    s["balance"] = s["balance"].drop("Total Debt")
    table, sources = fundamentals.extract_fundamentals(s)
    assert table["total_debt"].isna().all()         # never filled with zero
    assert any("total_debt" in f for f in fundamentals.missing_items(table, sources))
