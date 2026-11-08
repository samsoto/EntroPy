"""Regenerate the README's original figures from data and equations.

Run from the repository root after installing the project: python scripts/render_graphics.py
"""

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from information.audit import audit, demo_data
from information.graphics import BLUE, INK, MUTED, ORANGE, PAPER, RULE, _save, _style, plot_audit

OUTPUT = Path(__file__).resolve().parents[1] / "resources/images/guide"


def uncertainty():
    with _style():
        fig = plt.figure(figsize=(13.6, 5.8))
        fig.text(0.06, 0.91, "FIELD NOTE 01  /  UNCERTAINTY", fontsize=11, color=ORANGE, weight="bold")
        fig.text(0.06, 0.80, "Surprise, averaged over outcomes.", fontsize=27, fontfamily="DejaVu Serif")
        cases = [("Even odds", [0.25]*4), ("One likely outcome", [0.5, 0.25, 0.125, 0.125]), ("Already certain", [1, 0, 0, 0])]
        for i, (label, probabilities) in enumerate(cases):
            left = 0.07 + i * 0.315
            ax = fig.add_axes([left, 0.28, 0.245, 0.30])
            ax.bar(range(4), probabilities, color=ORANGE if i < 2 else BLUE, width=0.6)
            ax.set_ylim(0, 1.14)
            ax.set_xticks(range(4), ["A", "B", "C", "D"])
            ax.set_yticks([])
            ax.tick_params(length=0, pad=7)
            for spine in ax.spines.values():
                spine.set_visible(False)
            for j, p in enumerate(probabilities):
                ax.text(j, p + 0.035, f"{p:.0%}" if p != 0.125 else "12.5%", ha="center", fontsize=10)
            entropy = -sum(p * np.log2(p) for p in probabilities if p)
            fig.text(left, 0.65, label, fontsize=13, weight="bold")
            fig.text(left, 0.17, f"H(X) = {abs(entropy):.2f} bits", fontsize=16)
        fig.text(0.06, 0.06, r"$H(X) = -\sum_x p(x)\log_2 p(x)$", fontsize=15)
        fig.text(0.39, 0.067, "More predictable outcomes carry less average information.", fontsize=11, color=MUTED)
        _save(fig, OUTPUT / "uncertainty")


def relationships():
    with _style():
        fig = plt.figure(figsize=(13.6, 6.2))
        fig.text(0.06, 0.92, "FIELD NOTE 02  /  RELATIONSHIPS", fontsize=11, color=ORANGE, weight="bold")
        fig.text(0.06, 0.82, "What does knowing Y tell us about X?", fontsize=25, fontfamily="DejaVu Serif")
        fig.text(0.06, 0.71, "SAME OBSERVATION", fontsize=10, weight="bold")
        fig.text(0.57, 0.71, "ACROSS TIME", fontsize=10, weight="bold")
        ax = fig.add_axes([0.175, 0.34, 0.30, 0.26])
        mi = [0, 0.2780719051126377, 1]
        ax.barh(range(3), mi, height=0.5, color=ORANGE)
        ax.barh(range(3), [1-value for value in mi], left=mi, height=0.5, color=RULE)
        ax.set_yticks(range(3), ["Independent", "Noisy signal", "Perfect copy"])
        ax.invert_yaxis()
        ax.set_xlim(0, 1)
        ax.set_xticks([0, 0.5, 1], ["0", "0.5", "1 bit"])
        ax.tick_params(length=0, pad=8)
        for spine in ax.spines.values():
            spine.set_visible(False)
        for i, value in enumerate(mi):
            if value:
                ax.text(value/2, i, f"{value:.3f}", ha="center", va="center", color="white", fontsize=10)
        fig.text(0.06, 0.22, "Shared: I(X;Y)", fontsize=12, color=ORANGE)
        fig.text(0.25, 0.22, "Remaining: H(X|Y)", fontsize=12, color=MUTED)
        fig.text(0.06, 0.155, "Together they make H(X), here exactly 1 bit.", fontsize=11, color=MUTED)
        time = fig.add_axes([0.55, 0.32, 0.38, 0.33])
        time.set_xlim(0, 1)
        time.set_ylim(0, 1)
        time.axis("off")
        time.text(0.08, 0.80, r"$X_t$", fontsize=24, ha="center")
        time.text(0.08, 0.20, r"$Y_t$", fontsize=24, ha="center", color=ORANGE)
        time.text(0.80, 0.80, r"$X_{t+1}$", fontsize=24, ha="center")
        time.annotate("", xy=(0.66, 0.86), xytext=(0.20, 0.86), arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 2})
        time.annotate("", xy=(0.70, 0.73), xytext=(0.19, 0.28), arrowprops={"arrowstyle": "->", "color": ORANGE, "lw": 2})
        time.text(0.44, 0.96, "account for own past", ha="center", fontsize=9, color=MUTED)
        time.text(0.58, 0.31, "additional information", ha="center", fontsize=9, color=ORANGE)
        fig.text(0.57, 0.22, r"$T_{Y\to X}=I(X_{t+1};Y_t\mid X_t)$", fontsize=16)
        fig.text(0.57, 0.155, "API: transfer_entropy(target, source)", fontsize=11, color=MUTED)
        fig.text(0.06, 0.06, "Association and directional predictability are descriptive; neither alone establishes causation.", fontsize=10, color=MUTED)
        _save(fig, OUTPUT / "relationships")


if __name__ == "__main__":
    data, reference = demo_data()
    plot_audit(audit(data, "fault", reference), OUTPUT / "signal-audit")
    uncertainty()
    relationships()
    print(f"Wrote SVG and PNG figures to {OUTPUT}")
