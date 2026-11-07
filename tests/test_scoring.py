"""Checks on the scoring and the robustness simulation."""
import numpy as np
import pandas as pd
import pytest

from src import scoring

SPECS = {
    "q1": {"group": "Quality", "higher_is_better": True},
    "q2": {"group": "Quality", "higher_is_better": False},
    "g1": {"group": "Growth", "higher_is_better": True},
    "v1": {"group": "Value", "higher_is_better": True},
    "m1": {"group": "Momentum", "higher_is_better": True},
    "r1": {"group": "Risk", "higher_is_better": False},
}
WEIGHTS = {"Quality": 0.30, "Growth": 0.25, "Value": 0.20, "Momentum": 0.15, "Risk": 0.10}


def values():
    return pd.DataFrame({
        "q1": [30, 20, 10], "q2": [1, 2, 3], "g1": [5, 10, 15],
        "v1": [3, 2, 1], "m1": [1, 2, 3], "r1": [0.1, 0.2, 0.3],
    }, index=["A", "B", "C"])


def test_percentiles_best_is_100_worst_is_0():
    pct = scoring.percentile_scores(values(), SPECS)
    assert list(pct["q1"]) == [100, 50, 0]


def test_lower_is_better_is_flipped():
    pct = scoring.percentile_scores(values(), SPECS)
    assert list(pct["q2"]) == [100, 50, 0]        # 1 is the lowest, so the best
    assert list(pct["r1"]) == [100, 50, 0]


def test_ties_share_the_average():
    v = values(); v["g1"] = [5, 5, 15]
    assert list(scoring.percentile_scores(v, SPECS)["g1"]) == [25, 25, 100]


def test_missing_metric_is_skipped_in_group_average():
    pct = scoring.percentile_scores(values(), SPECS)
    pct.loc["A", "q2"] = np.nan
    groups = scoring.group_scores(pct, SPECS)
    assert groups.loc["A", "Quality"] == 100        # only q1 counts


def test_total_is_weighted_average_and_contributions_add_up():
    groups = pd.DataFrame({g: [100.0, 0.0] for g in scoring.GROUPS}, index=["A", "B"])
    groups.loc["A", "Growth"] = 0
    total = scoring.total_scores(groups, WEIGHTS)
    assert total["A"] == pytest.approx(75)          # 100 x (1 - 0.25)
    assert scoring.contributions(groups, WEIGHTS).sum(axis=1)["A"] == pytest.approx(75)


def test_missing_group_reweights():
    groups = pd.DataFrame({g: [100.0] for g in scoring.GROUPS}, index=["A"])
    groups.loc["A", "Value"] = np.nan
    assert scoring.total_scores(groups, WEIGHTS)["A"] == pytest.approx(100)


def test_random_weights_sum_to_one_and_stay_near_the_base():
    w = scoring.random_weights(WEIGHTS, 0.10, 10_000, np.random.default_rng(0))
    assert np.allclose(w.sum(axis=1), 1)
    assert (w >= 0).all()
    assert w[:, 0].mean() == pytest.approx(0.30, abs=0.01)   # Quality centred on 30%


def test_dominant_company_is_always_top():
    groups = pd.DataFrame({g: [90.0, 50, 40, 30, 20] for g in scoring.GROUPS}, index=list("ABCDE"))
    r = scoring.robustness(groups, WEIGHTS, n=2000, spread=0.10, seed=1, top=1)
    assert r.loc["A", "p_top"] == 1.0
    assert r.loc["A", "median_rank"] == 1


def test_weight_sensitive_company_is_not_always_top():
    # A is great at Quality only, B at everything else: who wins depends on the weights
    groups = pd.DataFrame({"Quality": [100.0, 0], "Growth": [0.0, 60], "Value": [0.0, 60],
                           "Momentum": [0.0, 60], "Risk": [0.0, 60]}, index=["A", "B"])
    r = scoring.robustness(groups, WEIGHTS, n=5000, spread=0.10, seed=1, top=1)
    assert 0 < r.loc["A", "p_top"] < 1


def test_simulation_is_reproducible():
    groups = pd.DataFrame(np.random.default_rng(3).uniform(0, 100, (6, 5)), columns=scoring.GROUPS)
    a = scoring.robustness(groups, WEIGHTS, 1000, 0.1, seed=42)
    b = scoring.robustness(groups, WEIGHTS, 1000, 0.1, seed=42)
    pd.testing.assert_frame_equal(a, b)
