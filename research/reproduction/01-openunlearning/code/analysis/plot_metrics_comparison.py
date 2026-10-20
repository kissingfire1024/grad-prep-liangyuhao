import json
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(
    "/home/research/research/reproduction/01-openunlearning"
)

RETAIN_PATH = ROOT / "results/retain99/TOFU_SUMMARY.json"

GA_PATH = (
    ROOT
    / "results/gradascent_forget01/TOFU_SUMMARY.json"
)

FIGURE_DIR = (
    ROOT
    / "results/gradascent_forget01/figures"
)

TABLE_DIR = (
    ROOT
    / "results/gradascent_forget01/tables"
)

FIGURE_DIR.mkdir(parents=True, exist_ok=True)
TABLE_DIR.mkdir(parents=True, exist_ok=True)


with RETAIN_PATH.open() as f:
    retain = json.load(f)

with GA_PATH.open() as f:
    grad = json.load(f)


metrics = [
    ("forget_Q_A_Prob", "Forget Q/A Prob"),
    ("forget_Q_A_ROUGE", "Forget Q/A ROUGE"),
    ("forget_truth_ratio", "Forget Truth Ratio"),
    ("model_utility", "Model Utility"),
    ("extraction_strength", "Extraction Strength"),
]


# -----------------------------
# Collect real values
# -----------------------------

rows = []

for key, label in metrics:
    rows.append({
        "metric": label,
        "retain99": retain.get(key),
        "gradascent": grad.get(key),
    })


# -----------------------------
# Save CSV
# -----------------------------

csv_path = TABLE_DIR / "metrics_comparison.csv"

with csv_path.open("w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow([
        "metric",
        "retain99",
        "gradascent"
    ])

    for row in rows:
        writer.writerow([
            row["metric"],
            row["retain99"],
            row["gradascent"]
        ])


# -----------------------------
# Plot
# -----------------------------

labels = [r["metric"] for r in rows]

retain_values = [
    float(r["retain99"])
    for r in rows
]

grad_values = [
    float(r["gradascent"])
    for r in rows
]


x = np.arange(len(labels))

width = 0.36


fig, ax = plt.subplots(figsize=(11, 6))

bars1 = ax.bar(
    x - width / 2,
    retain_values,
    width,
    label="Retain99 Reference"
)

bars2 = ax.bar(
    x + width / 2,
    grad_values,
    width,
    label="GradAscent"
)


ax.set_ylabel("Metric Value")

ax.set_title(
    "TOFU Evaluation: Retain99 vs GradAscent\n"
    "Llama-3.2-1B-Instruct · forget01"
)

ax.set_xticks(x)

ax.set_xticklabels(
    labels,
    rotation=15,
    ha="right"
)

ax.legend()

ax.grid(
    axis="y",
    alpha=0.25
)


# -----------------------------
# Value labels
# -----------------------------

for bars in [bars1, bars2]:

    for bar in bars:

        value = bar.get_height()

        ax.annotate(
            f"{value:.3g}",
            xy=(
                bar.get_x() + bar.get_width() / 2,
                value
            ),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8
        )


plt.tight_layout()

png_path = (
    FIGURE_DIR
    / "02_metrics_comparison.png"
)

plt.savefig(
    png_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("Saved CSV:")
print(csv_path)

print("\nSaved figure:")
print(png_path)

print("\nMetrics:")

for row in rows:
    print(
        row["metric"],
        "| retain99:",
        row["retain99"],
        "| GradAscent:",
        row["gradascent"]
    )
