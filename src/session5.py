"""
Session 5: the ranking, and how robust it is.

Run:  python -m src.session5     (uses outputs/tables/metrics_all.csv from Session 3)

Outputs:
  outputs/tables/ranking.csv        metric ranks, group scores, contributions, total, rank
  outputs/tables/robustness.csv     P(top 3), median rank and rank range over 10,000 weight sets
  outputs/tables/finalists.csv      the 3 companies for the deep dive, and why
  outputs/charts/02_ranking.png     what drives each score, and how robust each rank is
"""
import matplotlib.pyplot as plt
import pandas as pd

from config import settings
from src import scoring

NAMES = {"MDT": "Medtronic", "ABT": "Abbott", "BDX": "Becton Dickinson", "GEHC": "GE HealthCare",
         "SYK": "Stryker", "ZBH": "Zimmer Biomet", "ISRG": "Intuitive Surgical", "GMED": "Globus Medical",
         "BSX": "Boston Scientific", "EW": "Edwards", "DXCM": "DexCom", "PODD": "Insulet", "RMD": "ResMed",
         "TFX": "Teleflex", "STE": "STERIS", "COO": "Cooper", "ALGN": "Align"}
# Companies whose latest annual report includes businesses since separated (decision log, 7 Nov 2026)
PERIMETER_FLAG = {"BDX", "TFX"}

# Validated categorical palette, slots 1-5 in fixed order (one per group)
GROUP_COLOURS = dict(zip(scoring.GROUPS, ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]))
SURFACE, INK, INK_SOFT, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"


def select_finalists(robust: pd.DataFrame, total: pd.Series, n: int) -> pd.DataFrame:
    """Top n by probability of finishing in the top 3; ties broken by the base-case score."""
    order = pd.DataFrame({"p_top": robust["p_top"], "score": total}).sort_values(["p_top", "score"], ascending=False)
    chosen = order.head(n).copy()
    chosen["note"] = ["re-measure on post-separation figures before valuation (decision log)"
                      if t in PERIMETER_FLAG else "" for t in chosen.index]
    return chosen


def plot(ranking: pd.DataFrame, robust: pd.DataFrame, finalists: list, path) -> None:
    order = ranking.sort_values("total").index        # best at the top of a horizontal chart
    contrib = ranking.loc[order, [f"pts_{g}" for g in scoring.GROUPS]]
    labels = [f"{NAMES[t]} ({t})" for t in order]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 7.2), sharey=True,
                                   gridspec_kw={"width_ratios": [2.3, 1], "wspace": 0.06})
    fig.patch.set_facecolor(SURFACE)
    for ax in (ax1, ax2):
        ax.set_facecolor(SURFACE)
        ax.grid(axis="x", color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)
        ax.tick_params(colors=INK_SOFT, length=0)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(GRID)

    # Left: stacked contributions (white edges = the 2px gap between segments)
    left = pd.Series(0.0, index=order)
    for g in scoring.GROUPS:
        ax1.barh(labels, contrib[f"pts_{g}"], left=left, color=GROUP_COLOURS[g], height=0.68,
                 edgecolor=SURFACE, linewidth=1.2, label=f"{g} ({settings.WEIGHTS[g]:.0%})")
        left += contrib[f"pts_{g}"]
    for y, t in enumerate(order):
        ax1.text(ranking.loc[t, "total"] + 0.8, y, f"{ranking.loc[t, 'total']:.0f}", va="center",
                 color=INK, fontsize=9, fontweight="bold" if t in finalists else "normal")
    ax1.set_xlabel("Total score (0-100): points contributed by each group", color=INK_SOFT)
    ax1.set_xlim(0, 100)
    ax1.set_xticks([0, 20, 40, 60, 80])
    ax1.legend(loc="lower right", frameon=False, fontsize=8.5, labelcolor=INK, title="Group (weight)",
               title_fontsize=8.5)
    for lbl in ax1.get_yticklabels():
        t = lbl.get_text().split("(")[-1].rstrip(")")
        lbl.set_color(INK if t in finalists else INK_SOFT)
        lbl.set_fontweight("bold" if t in finalists else "normal")

    # Right: probability of a top-3 finish across 10,000 weight sets
    p = robust.loc[order, "p_top"]
    ax2.barh(labels, p, color=[INK if t in finalists else "#b5b4ae" for t in order], height=0.68)
    for y, (t, v) in enumerate(p.items()):
        ax2.text(v + 0.02, y, f"{v:.0%}", va="center", color=INK, fontsize=9)
    ax2.set_xlim(0, 1.15)
    ax2.set_xticks([0, 0.5, 1])
    ax2.set_xticklabels(["0%", "50%", "100%"])
    ax2.set_xlabel(f"P(top 3) over {settings.N_SIMULATIONS:,} random weight sets", color=INK_SOFT)

    fig.suptitle("The screen: what drives each company's score, and how robust its rank is",
                 x=0.01, y=0.95, ha="left", color=INK, fontsize=13, fontweight="bold")
    fig.subplots_adjust(top=0.91)
    fig.text(0.01, 0.005, f"Weights varied ±{settings.WEIGHT_SPREAD:.0%} around 30/25/20/15/10 and rescaled to 100%. "
             "Finalists (bold) = the 3 highest P(top 3). Data: close 6 Nov 2026, latest annual reports.",
             color=INK_SOFT, fontsize=8)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor=SURFACE)
    plt.close(fig)


def main() -> None:
    values = pd.read_csv(settings.TABLES_DIR / "metrics_all.csv", index_col=0)
    specs = settings.METRICS

    pct = scoring.percentile_scores(values[list(specs)], specs)
    groups = scoring.group_scores(pct, specs)
    total = scoring.total_scores(groups, settings.WEIGHTS)
    pts = scoring.contributions(groups, settings.WEIGHTS).add_prefix("pts_")
    ranking = pd.concat([pct.add_prefix("pct_"), groups, pts], axis=1)
    ranking["total"] = total
    ranking["rank"] = total.rank(ascending=False, method="min").astype(int)
    ranking = ranking.sort_values("rank")
    ranking.round(2).to_csv(settings.TABLES_DIR / "ranking.csv")

    robust = scoring.robustness(groups, settings.WEIGHTS, settings.N_SIMULATIONS,
                                settings.WEIGHT_SPREAD, settings.RANDOM_SEED, top=settings.N_FINALISTS)
    robust = robust.loc[ranking.index]
    robust.to_csv(settings.TABLES_DIR / "robustness.csv")

    finalists = select_finalists(robust, total, settings.N_FINALISTS)
    finalists.to_csv(settings.TABLES_DIR / "finalists.csv")

    settings.CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    plot(ranking, robust, finalists.index.tolist(), settings.CHARTS_DIR / "02_ranking.png")

    view = pd.concat([ranking[["rank", "total"] + scoring.GROUPS], robust], axis=1)
    with pd.option_context("display.width", 200):
        print(view.round(2).to_string())
    print("\nFinalists:\n", finalists.to_string())


if __name__ == "__main__":
    main()
