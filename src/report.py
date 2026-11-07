"""Turning results into readable markdown documents (no calculations here)."""
import pandas as pd

from config import settings


def markdown_table(df: pd.DataFrame) -> str:
    """A pandas table as a GitHub markdown table (no extra library needed)."""
    lines = ["| " + " | ".join(str(c) for c in df.columns) + " |", "|" + "---|" * len(df.columns)]
    lines += ["| " + " | ".join("" if pd.isna(v) else str(v) for v in row) + " |"
              for row in df.itertuples(index=False)]
    return "\n".join(lines)


def company_workings(result, sources: dict, flags: list[str], rates: pd.DataFrame) -> str:
    """One company's hand-check document: inputs, rates, every formula with numbers, labels used, flags."""
    context = pd.DataFrame(list(result.context.items()), columns=["Input", "Value"])
    rates_view = rates.assign(value=rates["value"].map("{:.2%}".format))[["rate", "value", "basis"]]
    labels = pd.DataFrame([(k, v or "MISSING") for k, v in sources.items()], columns=["Item", "Yahoo label"])
    return "\n".join([
        f"# {result.ticker}: the 12 screening metrics, with workings",
        "",
        f"Valuation date {settings.VALUATION_DATE}. Money in $ millions.",
        "",
        "## Inputs", "", markdown_table(context), "",
        "## Risk-free rates (FRED)", "", markdown_table(rates_view), "",
        "## Metrics", "", markdown_table(pd.DataFrame(result.workings)), "",
        "## Yahoo labels used", "", markdown_table(labels), "",
        "## Data flags", "",
        *([f"- {f}" for f in flags] or ["- None: every item found under its preferred label."]),
    ])
