"""
From 12 metrics to one score and a ranking (README sections 7 and 8).

1. Percentile rank every metric: 0 = worst company, 100 = best.
   "Lower is better" metrics are flipped first, so 100 always means best.
2. Group score = average of the group's metric ranks (missing metrics are skipped).
3. Total score = weighted average of the group scores.
4. Robustness: redo step 3 with 10,000 random sets of weights and count how
   often each company finishes in the top 3.
"""
import numpy as np
import pandas as pd

GROUPS = ["Quality", "Growth", "Value", "Momentum", "Risk"]


def percentile_scores(values: pd.DataFrame, specs: dict) -> pd.DataFrame:
    """
    For each metric: the share of the other companies this company beats, 0-100.
    With 17 companies, the best scores 100, the worst 0, the middle one 50.
    Ties share the average rank. Missing values stay missing.
    """
    out = {}
    for metric, spec in specs.items():
        s = values[metric] if spec["higher_is_better"] else -values[metric]
        n = s.notna().sum()
        out[metric] = (s.rank(method="average") - 1) / (n - 1) * 100
    return pd.DataFrame(out, index=values.index)


def group_scores(pct: pd.DataFrame, specs: dict) -> pd.DataFrame:
    """Average of the metric ranks in each group (skipping missing ones)."""
    return pd.DataFrame({g: pct[[m for m, s in specs.items() if s["group"] == g]].mean(axis=1)
                         for g in GROUPS})


def total_scores(groups: pd.DataFrame, weights: dict) -> pd.Series:
    """
    Weighted average of group scores. If a company is missing a whole group,
    the remaining weights are rescaled to sum to 1 for that company (and the
    gap is visible in the group table).
    """
    w = pd.Series(weights)[GROUPS]
    available = groups[GROUPS].notna()
    weighted = groups[GROUPS].fillna(0).mul(w, axis=1).sum(axis=1)
    return weighted / available.mul(w, axis=1).sum(axis=1)


def contributions(groups: pd.DataFrame, weights: dict) -> pd.DataFrame:
    """Points each group adds to the total score (they sum to the total)."""
    return groups[GROUPS].mul(pd.Series(weights)[GROUPS], axis=1)


def random_weights(base: dict, spread: float, n: int, rng: np.random.Generator) -> np.ndarray:
    """
    n random weight sets. Each group's weight is drawn uniformly within
    +/- `spread` of its chosen weight (never below 0), then all five are
    rescaled to add up to 1.
    """
    w = np.array([base[g] for g in GROUPS])
    draws = rng.uniform(np.maximum(w - spread, 0), w + spread, size=(n, len(GROUPS)))
    return draws / draws.sum(axis=1, keepdims=True)


def robustness(groups: pd.DataFrame, base: dict, n: int, spread: float, seed: int,
               top: int = 3) -> pd.DataFrame:
    """
    How much does the ranking depend on the exact weights?
    For each company: probability of finishing in the top `top`, and its
    median and 5th-95th percentile rank across all simulations.
    """
    rng = np.random.default_rng(seed)
    W = random_weights(base, spread, n, rng)                      # n x 5
    G = groups[GROUPS].to_numpy()
    available = ~np.isnan(G)
    scores = (np.nan_to_num(G) @ W.T) / (available @ W.T)          # companies x n
    ranks = (-scores).argsort(axis=0).argsort(axis=0) + 1          # 1 = best, per simulation
    return pd.DataFrame({
        "p_top": (ranks <= top).mean(axis=1),
        "median_rank": np.median(ranks, axis=1),
        "rank_p5": np.percentile(ranks, 5, axis=1),
        "rank_p95": np.percentile(ranks, 95, axis=1),
    }, index=groups.index)
