import json
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


BASE = Path("/home/research/research/reproduction")

RETAIN = (
    BASE /
    "01-openunlearning/results/retain99/TOFU_SUMMARY.json"
)

GRAD_ASCENT = (
    BASE /
    "01-openunlearning/results/gradascent_forget01/TOFU_SUMMARY.json"
)

GRAD_DIFF = (
    BASE /
    "02-graddiff/results/graddiff_forget01/TOFU_SUMMARY.json"
)

RESULT_ROOT = (
    BASE /
    "02-graddiff/results/graddiff_forget01"
)

FIGURE_DIR = RESULT_ROOT / "figures"
TABLE_DIR = RESULT_ROOT / "tables"

FIGURE_DIR.mkdir(parents=True, exist_ok=True)
TABLE_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path):
    if not path.exists():
        raise FileNotFoundError(path)

    with path.open("r") as f:
        return json.load(f)


retain = load_json(RETAIN)
ga = load_json(GRAD_ASCENT)
gd = load_json(GRAD_DIFF)


metrics = [
    ("Forget Q/A Prob", "forget_Q_A_Prob"),
    ("Forget Q/A ROUGE", "forget_Q_A_ROUGE"),
    ("Forget Truth Ratio", "forget_truth_ratio"),
    ("Model Utility", "model_utility"),
    ("Extraction Strength", "extraction_strength"),
]


rows = []

for display_name, key in metrics:
    rows.append([
        display_name,
        retain.get(key),
        ga.get(key),
        gd.get(key),
    ])


# -----------------------------
# Save comparison table
# -----------------------------

csv_path = TABLE_DIR / "metrics_comparison.csv"

with csv_path.open("w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "metric",
        "retain99",
        "gradascent",
        "graddiff",
    ])

    writer.writerows(rows)


# -----------------------------
# Plot
# -----------------------------

labels = [x[0] for x in rows]

retain_values = np.array(
    [x[1] for x in rows],
    dtype=float
)

ga_values = np.array(
    [x[2] for x in rows],
    dtype=float
)

gd_values = np.array(
    [x[3] for x in rows],
    dtype=float
)


x = np.arange(len(labels))
width = 0.25

plt.figure(figsize=(11, 6))

plt.bar(
    x - width,
    retain_values,
    width,
    label="Retain99"
)

plt.bar(
    x,
    ga_values,
    width,
    label="GradAscent"
)

plt.bar(
    x + width,
    gd_values,
    width,
    label="GradDiff"
)

plt.xticks(
    x,
    labels,
    rotation=15,
    ha="right"
)

plt.ylabel("Metric Value")

plt.title(
    "TOFU forget01: Retain99 vs GradAscent vs GradDiff\n"
    "Llama-3.2-1B-Instruct"
)

plt.legend()

plt.grid(
    axis="y",
    alpha=0.25
)

plt.tight_layout()

png_path = FIGURE_DIR / "02_metrics_comparison.png"

plt.savefig(
    png_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("Sources:")
print("Retain99:   ", RETAIN)
print("GradAscent: ", GRAD_ASCENT)
print("GradDiff:   ", GRAD_DIFF)

print("\nSaved CSV:")
print(csv_path)

print("\nSaved figure:")
print(png_path)

print("\nValues:")

for row in rows:
    print(row)
