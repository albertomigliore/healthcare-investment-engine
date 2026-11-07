"""
Cross-checking Yahoo's numbers against the official 10-K filings, for every company.

The SEC publishes each company's financial statements in a machine-readable
form (XBRL "company facts"). For each company we take the value that the
company itself reported in its 10-K for the same financial year, and compare it
with Yahoo's. Session 1 did this by hand for Stryker; this does it for everyone.

The SEC asks automated users to identify themselves and stay under 10 requests
per second; we make one request per company.
"""
import gzip
import json
import time

import pandas as pd
import requests

from config import settings

HEADERS = {"User-Agent": "healthcare-investment-engine student research project"}
SEC_DIR = settings.RAW_DIR / "sec"

# XBRL tags to try, best first. Companies choose different tags for the same item.
TAGS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
                "SalesRevenueNet", "RevenueFromContractWithCustomerIncludingAssessedTax"],
    "operating_income": ["OperatingIncomeLoss"],
}


def _get(url: str) -> requests.Response:
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    time.sleep(0.15)   # stay well under the SEC's rate limit
    return response


def cik_lookup() -> dict[str, int]:
    """
    Ticker -> SEC company number (CIK), from data/manual/sec_ciks.csv.
    Each CIK was verified against the company name the SEC returns for it
    (the SEC's own ticker list requires a personal contact email to download).
    """
    table = pd.read_csv(settings.MANUAL_DIR / "sec_ciks.csv")
    return dict(zip(table["ticker"], table["cik"]))


def company_facts(ticker: str, cik: int) -> dict:
    """All XBRL facts a company has filed. The download is saved (compressed) in data/raw/sec/."""
    SEC_DIR.mkdir(parents=True, exist_ok=True)
    raw = _get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json").content
    (SEC_DIR / f"{ticker}_companyfacts_downloaded_{pd.Timestamp.today():%Y-%m-%d}.json.gz").write_bytes(gzip.compress(raw))
    return json.loads(raw)


def annual_value(facts: dict, tags: list[str], fiscal_year_end: pd.Timestamp) -> dict | None:
    """
    The value reported in a 10-K for a full year ending on `fiscal_year_end`
    (within 10 days, because some years end on "the last Friday of April").
    Tries each tag in order. If a year appears in several filings (later 10-Ks
    repeat earlier years), the most recently filed value is used.
    """
    us_gaap = facts.get("facts", {}).get("us-gaap", {})
    for tag in tags:
        candidates = []
        for fact in us_gaap.get(tag, {}).get("units", {}).get("USD", []):
            if not fact.get("form", "").startswith("10-K") or "start" not in fact:
                continue
            start, end = pd.Timestamp(fact["start"]), pd.Timestamp(fact["end"])
            full_year = 350 <= (end - start).days <= 380
            same_year = abs((end - fiscal_year_end).days) <= 10
            if full_year and same_year:
                candidates.append(fact)
        if candidates:
            best = max(candidates, key=lambda f: f["filed"])
            return {"tag": tag, "value": best["val"], "accession": best["accn"],
                    "filed": best["filed"], "period_end": best["end"]}
    return None


RESTATEMENT_THRESHOLD = 0.02


def revenue_history(facts: dict) -> pd.DataFrame:
    """
    Every full-year revenue figure in every 10-K, one row per (year, filing).
    Later 10-Ks repeat the two previous years, so the same year usually appears
    in several filings. If a company sells a business, later filings restate
    earlier years without it.
    """
    us_gaap = facts.get("facts", {}).get("us-gaap", {})
    for tag in TAGS["revenue"]:
        rows = [f for f in us_gaap.get(tag, {}).get("units", {}).get("USD", [])
                if f.get("form", "").startswith("10-K") and "start" in f
                and 350 <= (pd.Timestamp(f["end"]) - pd.Timestamp(f["start"])).days <= 380]
        if rows:
            df = pd.DataFrame(rows)[["end", "val", "filed", "accn"]]
            df["end"] = pd.to_datetime(df["end"])
            return df
    return pd.DataFrame(columns=["end", "val", "filed", "accn"])


def comparable_growth_years(facts: dict, fundamentals: pd.DataFrame, years: int) -> tuple[int, str]:
    """
    How many years of growth can be measured like-for-like?

    Growth compares the latest year with a base year. If a later year in that
    window was restated (a business sold, so revenue re-reported without it)
    but the base year never was, the base year still includes the business and
    the comparison is not like-for-like. Found in Session 3: Teleflex's 2022
    revenue ($2,791m) includes businesses being sold; 2023 was restated from
    $2,974m to $1,712m.

    Returns the longest window (<= `years`) whose base year is on the latest
    basis, and an explanation ("" if the full window is fine).
    """
    history = revenue_history(facts)
    if history.empty:
        return years, ""

    def restated(end) -> bool:
        vals = history.loc[(history["end"] - end).abs() <= pd.Timedelta(days=10), "val"]
        return len(vals) > 1 and vals.max() / vals.min() - 1 > RESTATEMENT_THRESHOLD

    index = fundamentals.index
    for n in range(years, 0, -1):
        if len(index) <= n:
            continue
        base = index[-1 - n]
        later_restated = any(restated(end) for end in index[-n:-1])
        if not later_restated or restated(base):
            note = "" if n == years else (
                f"growth measured over {n} years ({base:%Y}-{index[-1]:%Y}): later years were restated "
                f"after a divestiture, but {index[-1 - years]:%Y} was never restated, so it is not like-for-like")
            return n, note
    return years, "no like-for-like window found"


def crosscheck(ticker: str, facts: dict, fundamentals: pd.DataFrame) -> list[dict]:
    """Compare Yahoo's latest-year revenue and operating income with the 10-K."""
    fy = fundamentals.index[-1]
    rows = []
    for item, tags in TAGS.items():
        yahoo = fundamentals.loc[fy, item]
        official = annual_value(facts, tags, fy)
        row = {"ticker": ticker, "item": item, "fiscal_year_end": f"{fy:%Y-%m-%d}",
               "yahoo_musd": round(yahoo / 1e6, 1)}
        if official is None:
            row.update({"sec_musd": None, "difference": None, "match": "not in XBRL",
                        "sec_tag": None, "accession": None})
        else:
            diff = yahoo / official["value"] - 1
            row.update({"sec_musd": round(official["value"] / 1e6, 1), "difference": round(diff, 4),
                        "match": "yes" if abs(diff) < settings.MATCH_TOLERANCE else "NO",
                        "sec_tag": official["tag"], "accession": official["accession"]})
        rows.append(row)
    return rows
