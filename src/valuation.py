"""
Valuing one company three ways (README section 9): DCF, reverse DCF, trading comparables,
plus bear/base/bull scenarios and a Monte Carlo simulation.

The DCF is the classic "unlevered free cash flow" model, laid out exactly like a
spreadsheet so it can be rebuilt by hand:

    Revenue_t        = Revenue_(t-1) x (1 + growth_t)
    EBITDA_t         = Revenue_t x EBITDA margin_t
    - D&A_t          = Revenue_t x D&A %_t             (depreciation and amortisation)
    = EBIT_t         (operating profit)
    - Tax            = EBIT_t x tax rate
    + D&A_t          (a cost in the accounts, but no cash leaves the company)
    - Capex_t        = Revenue_t x capex %             (cash spent on equipment)
    - Change in NWC  = NWC % x (Revenue_t - Revenue_(t-1))  (cash tied up in stock and receivables)
    = Free cash flow_t (FCFF)

    Enterprise value = sum of FCFF_t / (1 + WACC)^t  +  terminal value / (1 + WACC)^N
    Terminal value   = FCFF_(N+1) / (WACC - terminal growth)   (all years after year N)
    Equity value     = Enterprise value - debt + cash ;  per share = equity / shares

Paths over the N forecast years:
- growth falls in equal steps from year-1 growth towards terminal growth (reached in year N+1);
- EBITDA margin moves in equal steps from today's to the target (reached in year N);
- D&A % moves to the capex % by year N: in a steady state depreciation roughly equals
  spending on equipment, and amortisation of past acquisitions runs off.

Why EBITDA margin and not operating margin (changed 7 Nov 2026, see README): amortisation
of acquired intangibles is a non-cash cost. Holding the OPERATING margin flat while
amortisation runs off would wrongly shrink cash flow; holding EBITDA flat lets operating
profit rise as amortisation ends, which is what actually happens.

Every function accepts numbers OR numpy arrays, so the Monte Carlo can value
10,000 versions of the company in one call.
"""
from dataclasses import dataclass, replace

import numpy as np
import pandas as pd
from scipy.optimize import brentq


# ===========================================================================
# Cost of capital
# ===========================================================================
def adjusted_beta(raw_beta: float, weight: float = 0.67) -> float:
    """Blume adjustment: measured betas drift towards 1 over time, so blend them with 1."""
    return weight * raw_beta + (1 - weight)


def wacc(risk_free: float, beta: float, erp: float, credit_spread: float, tax_rate: float,
         market_cap: float, debt: float) -> dict:
    """
    Weighted average cost of capital: the return lenders and shareholders
    together require, weighted by how much each has put in (at market value).

        cost of equity = risk-free + beta x equity risk premium      (CAPM)
        cost of debt   = (risk-free + credit spread) x (1 - tax rate) (interest is tax-deductible)
        WACC           = E/(D+E) x cost of equity + D/(D+E) x cost of debt
    """
    cost_equity = risk_free + beta * erp
    cost_debt = (risk_free + credit_spread) * (1 - tax_rate)
    w_equity = market_cap / (market_cap + debt)
    return {
        "cost_of_equity": cost_equity,
        "cost_of_debt_after_tax": cost_debt,
        "weight_equity": w_equity,
        "weight_debt": 1 - w_equity,
        "wacc": w_equity * cost_equity + (1 - w_equity) * cost_debt,
    }


# ===========================================================================
# The DCF
# ===========================================================================
@dataclass
class DCFInputs:
    revenue0: float           # latest financial year
    g1: float                 # year-1 revenue growth
    g_term: float             # terminal growth (after year N)
    margin0: float            # latest EBITDA margin
    margin_target: float      # EBITDA margin reached in year N
    tax_rate: float
    da_pct0: float            # D&A as % of revenue today
    capex_pct: float          # capex as % of revenue
    nwc_pct: float            # net working capital as % of revenue
    wacc: float
    debt: float
    cash: float
    shares: float
    years: int = 10


def _year(i: DCFInputs, t: int, revenue_prev, g1, margin_target, g_term):
    """One forecast year; works on numbers or arrays."""
    terminal_year = t == i.years + 1
    growth = g_term if terminal_year else g1 + (g_term - g1) * (t - 1) / i.years
    step = min(t, i.years) / i.years
    margin = i.margin0 + (margin_target - i.margin0) * step
    da_pct = i.da_pct0 + (i.capex_pct - i.da_pct0) * step
    revenue = revenue_prev * (1 + growth)
    ebitda = revenue * margin
    da = revenue * da_pct
    ebit = ebitda - da
    tax = ebit * i.tax_rate
    capex = revenue * i.capex_pct
    d_nwc = i.nwc_pct * (revenue - revenue_prev)
    fcff = ebit - tax + da - capex - d_nwc
    return dict(growth=growth, revenue=revenue, ebitda_margin=margin, ebitda=ebitda, da=da, ebit=ebit,
                tax=tax, capex=capex, change_nwc=d_nwc, fcff=fcff)


def project(i: DCFInputs) -> pd.DataFrame:
    """The year-by-year forecast table (years 1-N, plus year N+1 for the terminal value)."""
    rows, revenue_prev = [], i.revenue0
    for t in range(1, i.years + 2):
        y = _year(i, t, revenue_prev, i.g1, i.margin_target, i.g_term)
        y["discount_factor"] = np.nan if t == i.years + 1 else 1 / (1 + i.wacc) ** t
        y["pv_fcff"] = y["fcff"] * y["discount_factor"]
        rows.append({"year": t, **y})
        revenue_prev = y["revenue"]
    return pd.DataFrame(rows).set_index("year")


def dcf(i: DCFInputs) -> dict:
    """Enterprise value, equity value and value per share, with the pieces that build them."""
    p = project(i)
    explicit = p.loc[1:i.years]
    terminal_value = p.loc[i.years + 1, "fcff"] / (i.wacc - i.g_term)
    pv_terminal = terminal_value / (1 + i.wacc) ** i.years
    ev = explicit["pv_fcff"].sum() + pv_terminal
    equity = ev - i.debt + i.cash
    return {
        "pv_explicit": explicit["pv_fcff"].sum(),
        "terminal_value": terminal_value,
        "pv_terminal": pv_terminal,
        "terminal_share_of_ev": pv_terminal / ev,
        "enterprise_value": ev,
        "equity_value": equity,
        "value_per_share": equity / i.shares,
        "implied_terminal_ev_ebitda": terminal_value / p.loc[i.years + 1, "ebitda"],   # sanity check
    }


def value_per_share_vectorised(i: DCFInputs, g1, margin_target, wacc_, g_term) -> np.ndarray:
    """Same DCF as above, for arrays of assumptions at once (used by the Monte Carlo)."""
    g1, margin_target, wacc_, g_term = (np.asarray(x, dtype=float) for x in (g1, margin_target, wacc_, g_term))
    revenue_prev, pv = np.full(g1.shape, i.revenue0, dtype=float), np.zeros(g1.shape)
    for t in range(1, i.years + 2):
        y = _year(i, t, revenue_prev, g1, margin_target, g_term)
        if t == i.years + 1:
            pv += y["fcff"] / (wacc_ - g_term) / (1 + wacc_) ** i.years
        else:
            pv += y["fcff"] / (1 + wacc_) ** t
        revenue_prev = y["revenue"]
    return (pv - i.debt + i.cash) / i.shares


# ===========================================================================
# Reverse DCF
# ===========================================================================
def implied_growth(i: DCFInputs, price: float, low: float = -0.30, high: float = 0.80) -> float:
    """
    The year-1 growth (with the same fade to terminal growth) that makes the
    DCF value equal today's share price, everything else unchanged. In words:
    "what growth is the market paying for?"
    """
    f = lambda g: dcf(replace(i, g1=g))["value_per_share"] - price
    if f(low) > 0 or f(high) < 0:
        return np.nan
    return brentq(f, low, high, xtol=1e-6)


def forecast_cagr(i: DCFInputs) -> float:
    """Average yearly revenue growth over the forecast years implied by the growth path."""
    p = project(i)
    return (p.loc[i.years, "revenue"] / i.revenue0) ** (1 / i.years) - 1


# ===========================================================================
# Trading comparables
# ===========================================================================
def comparables_value(peer_multiples: pd.Series, metric: float, debt: float, cash: float,
                      shares: float) -> dict:
    """
    Apply peers' multiples (e.g. EV/EBITDA) to the company's own metric:
    EV = multiple x metric; value per share = (EV - debt + cash) / shares.
    Returns the value at the peers' 25th percentile, median and 75th percentile.
    """
    q = peer_multiples.quantile([0.25, 0.50, 0.75])
    per_share = (q * metric - debt + cash) / shares
    return {"low": per_share[0.25], "mid": per_share[0.50], "high": per_share[0.75]}


# ===========================================================================
# Monte Carlo
# ===========================================================================
def monte_carlo(i: DCFInputs, bear: dict, bull: dict, n: int, seed: int) -> pd.DataFrame:
    """
    10,000 DCFs, each with assumptions drawn at random:
    year-1 growth, target EBITDA margin and WACC from a triangle (bear, base, bull),
    terminal growth uniformly between the bear and bull values.
    """
    rng = np.random.default_rng(seed)
    draws = pd.DataFrame({
        "g1": rng.triangular(bear["g1"], i.g1, bull["g1"], n),
        "margin_target": rng.triangular(bear["margin_target"], i.margin_target, bull["margin_target"], n),
        "wacc": rng.triangular(bull["wacc"], i.wacc, bear["wacc"], n),
        "g_term": rng.uniform(bear["g_term"], bull["g_term"], n),
    })
    draws["value_per_share"] = value_per_share_vectorised(i, draws["g1"], draws["margin_target"],
                                                          draws["wacc"], draws["g_term"])
    return draws


def decision(median_value: float, p_above_price: float, price: float,
             buy_upside: float, buy_probability: float, sell_downside: float) -> str:
    """The rule fixed in advance (README section 9)."""
    if median_value >= price * (1 + buy_upside) and p_above_price >= buy_probability:
        return "BUY"
    if median_value <= price * (1 - sell_downside):
        return "SELL"
    return "HOLD"
