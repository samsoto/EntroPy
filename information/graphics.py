"""Publication-friendly figures with a consistent, editable vector output."""

from pathlib import Path
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

PAPER = "#F5F1E8"
INK = "#26231F"
MUTED = "#686158"
ORANGE = "#BE4726"
BLUE = "#385FA0"
RULE = "#D6CFC2"


def _style():
    return plt.rc_context({
        "font.family": "DejaVu Sans",
        "text.color": INK,
        "axes.labelcolor": MUTED,
        "xtick.color": MUTED,
        "ytick.color": INK,
        "figure.facecolor": PAPER,
        "axes.facecolor": PAPER,
        "font.size": 11,
        "svg.fonttype": "none",
        "svg.hashsalt": "entropy-signal-audit",
    })


def _save(fig, stem):
    stem = Path(stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(stem.with_suffix(".svg"), metadata={"Date": None})
    fig.savefig(stem.with_suffix(".png"), dpi=160)
    plt.close(fig)


def _axes(ax):
    for side in ["top", "right", "left"]:
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(RULE)
    ax.tick_params(axis="both", length=0, pad=9)
    ax.xaxis.grid(True, color=RULE, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.xaxis.set_major_locator(MaxNLocator(4))


def plot_audit(report, stem):
    """Plot top 12 feature associations and marginal drift; full data stays in JSON."""
    with _style():
        fig = plt.figure(figsize=(13.6, 8.2))
        fig.text(0.06, 0.935, "ENTROPY  /  SIGNAL AUDIT", fontsize=11, weight="bold", color=ORANGE)
        fig.text(0.06, 0.855, "Find the signal in your data.", fontsize=32, fontfamily="DejaVu Serif")
        target = textwrap.shorten(str(report["target"]), width=44, placeholder="...")
        fig.text(0.06, 0.798, f"{report['rows']:,} observations  /  target: {target}", fontsize=12, color=MUTED)
        fig.text(0.06, 0.706, f"{report['target_entropy_bits']:.3f}", fontsize=35, weight="bold")
        fig.text(0.215, 0.718, "bits of target uncertainty", fontsize=12)
        fig.text(0.215, 0.686, "How much is left to explain?", fontsize=10, color=MUTED)
        left = fig.add_axes([0.19, 0.245, 0.29, 0.32])
        right = fig.add_axes([0.68, 0.245, 0.25, 0.32])
        fig.text(0.06, 0.615, "01  /  WHICH FEATURES HELP?", fontsize=11, weight="bold")
        fig.text(0.56, 0.615, "02  /  WHAT HAS SHIFTED?", fontsize=11, weight="bold")
        for ax in [left, right]:
            _axes(ax)
        features = report["features"][:12]
        if features:
            values = [row["mutual_information_bits"] for row in features]
            left.barh(range(len(features)), values, height=0.46, color=ORANGE)
            left.set_yticks(range(len(features)), [textwrap.shorten(row["feature"], 20, placeholder="...") for row in features])
            left.invert_yaxis()
            limit = max(report["target_entropy_bits"], max(values), 0.1)
            left.set_xlim(0, limit * 1.3)
            for i, value in enumerate(values):
                left.text(value + limit * 0.035, i, f"{value:.3f}", va="center", fontsize=10)
        else:
            left.text(0.5, 0.5, "No feature columns", ha="center", transform=left.transAxes)
            left.set_yticks([])
        left.set_xlabel("Mutual information with target (bits)", labelpad=13, fontsize=10)
        drift = report["drift"][:12]
        if drift:
            finite = [row["kl_bits"] for row in drift if row["kl_bits"] is not None]
            limit = max(finite + [0.1])
            values = [row["kl_bits"] or 0 for row in drift]
            right.barh(range(len(drift)), values, height=0.46, color=BLUE)
            right.set_yticks(range(len(drift)), [textwrap.shorten(row["column"], 20, placeholder="...") for row in drift])
            right.invert_yaxis()
            right.set_xlim(0, limit * 1.5)
            for i, row in enumerate(drift):
                value = row["kl_bits"]
                label = f"{value:.3f}" if value is not None else "infinite*"
                right.text((value or 0) + limit * 0.04, i, label, va="center", fontsize=10)
        else:
            right.text(0.5, 0.5, "Add a reference sample\nto measure drift.", ha="center", va="center", transform=right.transAxes, color=MUTED)
            right.set_yticks([])
        right.set_xlabel("KL divergence: current || reference (bits)", labelpad=13, fontsize=10)
        fig.text(0.06, 0.125, "READ THE NUMBERS", fontsize=9, color=ORANGE, weight="bold")
        fig.text(0.06, 0.086, "Shared information describes association, not causation. Sparse data can overstate a signal.", fontsize=10, color=MUTED)
        footer = "* Infinite drift means an observed state is absent from the reference; no smoothing is applied."
        if not any(row["kl_bits"] is None for row in drift):
            footer = "Discrete empirical estimates. Inspect audit.json for all columns, settings, and interpretation notes."
        if len(report["features"]) > 12 or len(report["drift"]) > 12:
            footer = "Showing the top 12 entries in each plot. Full results and infinite-drift explanations: audit.json."
        fig.text(0.06, 0.053, footer, fontsize=9, color=MUTED)
        _save(fig, stem)
