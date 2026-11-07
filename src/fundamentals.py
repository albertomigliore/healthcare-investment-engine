"""
From Yahoo's raw statements to one clean table of the numbers we need.

Yahoo's statements have dozens of lines with Yahoo's own labels, and not every
company has every label. This file:
1. picks the lines we need, trying alternative labels in order of preference;
2. records which label was actually used, so every number can be traced;
3. builds the derived numbers (free cash flow, EBITDA, net debt).

The result has one row per financial year (oldest first) and one column per item.
"""
import pandas as pd

from config import settings
from src import metrics

# For each item: the statement it lives in, and the labels to try, best first.
FIELDS = {
    "revenue": ("income", ["Total Revenue", "Operating Revenue"]),
    # "As reported" matches the 10-K. Yahoo's plain "Operating Income" adds back
    # charges it considers one-offs (Session 2 finding), so it is only a fallback.
    "operating_income": ("income", ["Total Operating Income As Reported", "Operating Income"]),
    "pretax_income": ("income", ["Pretax Income"]),
    "tax": ("income", ["Tax Provision"]),
    "depreciation_amortisation": ("cashflow", ["Depreciation And Amortization",
                                               "Depreciation Amortization Depletion"]),
    "operating_cash_flow": ("cashflow", ["Operating Cash Flow",
                                         "Cash Flow From Continuing Operating Activities"]),
    "capital_expenditure": ("cashflow", ["Capital Expenditure", "Purchase Of PPE"]),
    "total_debt": ("balance", ["Total Debt"]),
    # Cash plus short-term investments: both turn into cash within a year (Session 3 decision;
    # e.g. Medtronic $1.9bn cash alone vs $9.2bn including short-term investments).
    "cash": ("balance", ["Cash Cash Equivalents And Short Term Investments", "Cash And Cash Equivalents"]),
    "equity": ("balance", ["Stockholders Equity", "Common Stock Equity"]),
    "shares": ("balance", ["Ordinary Shares Number", "Share Issued"]),
}


def _by_year(statement: pd.DataFrame) -> pd.DataFrame:
    """Columns as real dates, oldest year first (statements may come from Yahoo or a CSV)."""
    statement = statement.copy()
    statement.columns = pd.to_datetime(statement.columns)
    return statement.sort_index(axis=1)


def extract_fundamentals(statements: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, dict]:
    """
    Returns
    -------
    table : one row per financial year, one column per item (plus derived items)
    sources : for each item, the Yahoo label used, or None if no label was found
    """
    statements = {name: _by_year(df) for name, df in statements.items()}
    columns, sources = {}, {}

    for field, (statement_name, labels) in FIELDS.items():
        statement = statements[statement_name]
        found = next((label for label in labels if label in statement.index), None)
        sources[field] = found
        if found is None:
            columns[field] = pd.Series(float("nan"), index=statement.columns)
        else:
            columns[field] = statement.loc[found]

    table = pd.DataFrame(columns)
    table.index.name = "fiscal_year_end"

    # A year without revenue is an (almost) empty column from Yahoo: drop it.
    table = table.dropna(subset=["revenue"])

    # Derived items
    table["free_cash_flow"] = [metrics.free_cash_flow(o, c) for o, c in
                               zip(table["operating_cash_flow"], table["capital_expenditure"])]
    table["ebitda"] = table["operating_income"] + table["depreciation_amortisation"]
    table["net_debt"] = table["total_debt"] - table["cash"]
    return table, sources


def apply_overrides(ticker: str, table: pd.DataFrame, sources: dict) -> tuple[pd.DataFrame, list[str]]:
    """
    Fill gaps from data/manual/overrides.csv: values checked by hand in the
    company's 10-K, each with its source. An override may only fill a MISSING
    value; it never replaces a number Yahoo provided. Derived items are rebuilt.
    """
    path = settings.MANUAL_DIR / "overrides.csv"
    if not path.exists():
        return table, []
    overrides = pd.read_csv(path)
    overrides = overrides[overrides["ticker"] == ticker]
    table, notes = table.copy(), []
    for _, o in overrides.iterrows():
        year = pd.Timestamp(o["fiscal_year_end"])
        if year in table.index and pd.isna(table.loc[year, o["item"]]):
            table.loc[year, o["item"]] = o["value"]
            sources[o["item"]] = f"override: {o['source']}"
            notes.append(f"{o['item']} {year:%Y}: filled with {o['value']:,.0f} from {o['source']}")
    if notes:
        table["free_cash_flow"] = [metrics.free_cash_flow(a, b) for a, b in
                                   zip(table["operating_cash_flow"], table["capital_expenditure"])]
        table["ebitda"] = table["operating_income"] + table["depreciation_amortisation"]
        table["net_debt"] = table["total_debt"] - table["cash"]
    return table, notes


def missing_items(table: pd.DataFrame, sources: dict) -> list[str]:
    """Plain-English list of gaps, for the data-quality flags."""
    flags = [f"{field}: no matching line in Yahoo's statements"
             for field, label in sources.items() if label is None]
    latest = table.iloc[-1]
    flags += [f"{field}: missing in latest year ({table.index[-1]:%Y})"
              for field, value in latest.items() if pd.isna(value) and sources.get(field) is not None]
    fallbacks = [f"{field}: used fallback label '{label}'"
                 for field, label in sources.items()
                 if label is not None and label != FIELDS[field][1][0] and not label.startswith("override:")]
    return flags + fallbacks
