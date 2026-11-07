"""
Every choice from the README, in one place.

If a number here changes, the README decision log (section 12) must say why.
The rest of the code only reads from this file. It never hard-codes these values.
"""
from pathlib import Path

# ---------------------------------------------------------------------------
# Folders
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"              # downloads, never edited
MANUAL_DIR = PROJECT_ROOT / "data" / "manual"        # numbers typed in from official filings
CHARTS_DIR = PROJECT_ROOT / "outputs" / "charts"
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"

# ---------------------------------------------------------------------------
# Time settings (README section 6)
# ---------------------------------------------------------------------------
VALUATION_DATE = "2026-11-06"
PRICE_START = "2023-11-06"     # 3 years before the valuation date
TRADING_DAYS_PER_YEAR = 252
MARKET_TIMEZONE = "America/New_York"
MARKET_CLOSE_TIME = "16:30"    # market closes at 16:00 New York time; +30 min for final prices to settle
GROWTH_YEARS = 3               # growth measured over the last 3 financial years (4 annual reports)

# ---------------------------------------------------------------------------
# Universe (README section 3)
# Still to confirm in Session 3: every company is still listed in the same form
# (in particular Hologic and Teleflex, which had deals in progress in 2025).
# ---------------------------------------------------------------------------
UNIVERSE = {
    "Large diversified":        ["MDT", "ABT", "BDX", "GEHC"],
    "Orthopaedics and surgery": ["SYK", "ZBH", "ISRG", "GMED"],
    "Heart and blood vessels":  ["BSX", "EW", "PEN"],
    "Diabetes":                 ["DXCM", "PODD"],
    "Breathing and sleep":      ["RMD"],
    "Hospital products":        ["BAX", "TFX", "STE", "MASI"],
    "Diagnostics and imaging":  ["HOLX"],
    "Eye care and dental":      ["COO", "ALGN"],
}
TICKERS = [t for group in UNIVERSE.values() for t in group]

TEST_COMPANY = "SYK"           # Stryker: used to build and check the pipeline, NOT a pick

# ---------------------------------------------------------------------------
# Benchmarks (README section 4)
# ---------------------------------------------------------------------------
MARKET_BENCHMARK = "SPY"       # S&P 500, used for beta
SECTOR_BENCHMARK = "IHI"       # US medical devices ETF, used for relative momentum

# ---------------------------------------------------------------------------
# Risk-free rates (README section 4), from FRED (Federal Reserve Bank of St. Louis),
# which republishes the US Treasury's daily rates.
# ---------------------------------------------------------------------------
RISK_FREE_SHORT = "DTB3"       # 3-month Treasury bill: for the Sharpe ratio
RISK_FREE_LONG = "DGS10"       # 10-year Treasury yield: for the DCF (Session 6)
RATES_AS_OF = "2026-11-05"     # latest FRED value published before the valuation date (FRED lags a day);
                              # pinned so re-runs are reproducible (4.90% on 4 Nov, 4.84% on 5 Nov)

# ---------------------------------------------------------------------------
# Tax rate used in ROIC
# One year's tax rate can be distorted by one-offs (Stryker: 14% in 2024, 28% in 2025),
# so we pool the last 3 years: total tax paid / total pre-tax profit.
# ---------------------------------------------------------------------------
TAX_RATE_YEARS = 3
TAX_RATE_FALLBACK = 0.21       # US federal rate, used if pre-tax profit is negative
TAX_RATE_CAP = 0.35            # anything above this is treated as distorted and capped

# ---------------------------------------------------------------------------
# The 12 metrics (README section 7)
# higher_is_better tells the scoring (Session 5) which way to rank.
# Max drawdown is stored as a negative number (-0.30 = a 30% fall), so for it
# "higher is better": -10% beats -30%.
# ---------------------------------------------------------------------------
METRICS = {
    "roic":                  {"name": "ROIC",                     "group": "Quality",  "higher_is_better": True,  "unit": "%"},
    "fcf_margin":            {"name": "FCF margin",               "group": "Quality",  "higher_is_better": True,  "unit": "%"},
    "net_debt_to_ebitda":    {"name": "Net debt / EBITDA",        "group": "Quality",  "higher_is_better": False, "unit": "x"},
    "revenue_cagr":          {"name": "Revenue growth (3-yr)",    "group": "Growth",   "higher_is_better": True,  "unit": "%"},
    "operating_income_cagr": {"name": "Operating profit growth (3-yr)", "group": "Growth", "higher_is_better": True, "unit": "%"},
    "ev_to_ebitda":          {"name": "EV / EBITDA",              "group": "Value",    "higher_is_better": False, "unit": "x"},
    "fcf_yield":             {"name": "FCF yield",                "group": "Value",    "higher_is_better": True,  "unit": "%"},
    "momentum_12_1":         {"name": "12-1 month return",        "group": "Momentum", "higher_is_better": True,  "unit": "%"},
    "return_vs_sector":      {"name": "Return vs sector (12m)",   "group": "Momentum", "higher_is_better": True,  "unit": "%"},
    "volatility":            {"name": "Volatility",               "group": "Risk",     "higher_is_better": False, "unit": "%"},
    "beta":                  {"name": "Beta",                     "group": "Risk",     "higher_is_better": False, "unit": ""},
    "max_drawdown":          {"name": "Max drawdown",             "group": "Risk",     "higher_is_better": True,  "unit": "%"},
}

# ---------------------------------------------------------------------------
# Scoring weights (README section 7). Must add up to 1.
# ---------------------------------------------------------------------------
WEIGHTS = {
    "Quality":  0.30,
    "Growth":   0.25,
    "Value":    0.20,
    "Momentum": 0.15,
    "Risk":     0.10,
}

# ---------------------------------------------------------------------------
# Robustness check and Monte Carlo (README sections 8 and 9)
# ---------------------------------------------------------------------------
N_SIMULATIONS = 10_000
RANDOM_SEED = 42               # fixed so every run gives the same answer
WEIGHT_SPREAD = 0.10           # each group weight varies +/- 10 points (Quality 20%-40%), then rescaled to sum to 100%
N_FINALISTS = 3

# ---------------------------------------------------------------------------
# Valuation method (README section 9). Fixed on 7 Nov 2026 BEFORE any value was computed.
# Company-specific base assumptions (near-term growth, target margin) and their
# sources are in data/manual/valuation_assumptions.csv.
# ---------------------------------------------------------------------------
FORECAST_YEARS = 10           # changed from 5 on 7 Nov 2026 after the model sanity check (see README):
                              # 5 years forced 7-13% growers down to ~terminal growth too fast
TERMINAL_GROWTH = 0.025        # long-run growth after year 5: below the 10-year Treasury yield (4.9%)
EQUITY_RISK_PREMIUM = 0.050    # extra return investors demand for owning shares (typical range 4-6%)
CREDIT_SPREAD = 0.010          # pre-tax cost of debt = 10-year Treasury + 1% (large, investment-grade-like companies)
BETA_BLUME_WEIGHT = 0.67       # adjusted beta = 0.67 x measured beta + 0.33 x 1 (raw 3-year betas are noisy)

# Scenarios: the same shocks for every company, so no company gets a softer bear case
SCENARIOS = {
    #        year-1 growth     target EBITDA margin  WACC   terminal growth
    "bear": {"g1": -0.03,       "margin": -0.03, "wacc": +0.01, "g_term": 0.020},
    "base": {"g1":  0.00,       "margin":  0.00, "wacc":  0.00, "g_term": TERMINAL_GROWTH},
    "bull": {"g1": +0.03,       "margin": +0.03, "wacc": -0.01, "g_term": 0.030},
}
# Monte Carlo: growth, margin and WACC drawn from a triangle between bear and bull (most likely = base);
# terminal growth drawn uniformly between the bear and bull values.

# Trading comparables: 4-5 genuinely similar companies from the universe (a judgement call)
PEERS = {
    "GMED": ["SYK", "ZBH", "MDT", "ISRG"],          # spine/orthopaedic implants and surgical robotics
    "RMD":  ["DXCM", "PODD", "ABT", "MDT", "EW"],   # chronic-disease devices with recurring consumables
    "DXCM": ["PODD", "ABT", "RMD", "MDT", "EW"],    # diabetes (Insulet, Abbott's Libre, Medtronic) + home-use chronic care
}

# ---------------------------------------------------------------------------
# Decision rule (README section 9). Fixed before seeing any results.
# ---------------------------------------------------------------------------
BUY_MIN_UPSIDE = 0.15          # median value at least 15% above price...
BUY_MIN_PROBABILITY = 0.65     # ...and P(value > price) at least 65%
SELL_MIN_DOWNSIDE = 0.15       # median value at least 15% below price

# ---------------------------------------------------------------------------
# Data checks
# ---------------------------------------------------------------------------
MATCH_TOLERANCE = 0.01         # Yahoo vs 10-K: under 1% difference counts as a match

# Plausibility ranges: a value outside these is not wrong by definition, but it
# is unusual enough for a large device company that it must be checked by hand.
PLAUSIBLE_RANGES = {
    "roic":                  (0.00, 0.40),
    "fcf_margin":            (0.00, 0.40),
    "net_debt_to_ebitda":    (-3.0, 5.0),
    "revenue_cagr":          (-0.10, 0.30),
    "operating_income_cagr": (-0.25, 0.50),
    "ev_to_ebitda":          (5.0, 60.0),
    "fcf_yield":             (0.00, 0.12),
    "momentum_12_1":         (-0.60, 1.00),
    "return_vs_sector":      (-0.60, 1.00),
    "volatility":            (0.10, 0.60),
    "beta":                  (0.00, 2.00),
    "max_drawdown":          (-0.70, 0.00),
}
MAX_REPORT_AGE_DAYS = 15 * 30  # latest annual report older than ~15 months -> flag
