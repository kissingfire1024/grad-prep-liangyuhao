import csv
import json
import re
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(
    "/home/research/research/reproduction/01-openunlearning"
)

RETAIN_PATH = ROOT / "results/retain99/TOFU_EVAL.json"
GA_PATH = ROOT / "results/gradascent_forget01/TOFU_EVAL.json"

FIG_DIR = ROOT / "results/gradascent_forget01/figures"
TABLE_DIR = ROOT / "results/gradascent_forget01/tables"

FIG_DIR.mkdir(parents=True, exist_ok=True)
TABLE_DIR.mkdir(parents=True, exist_ok=True)


with RETAIN_PATH.open() as f:
    retain = json.load(f)

with GA_PATH.open() as f:
    ga = json.load(f)


retain_rouge = retain["forget_Q_A_ROUGE"]["value_by_index"]
ga_rouge = ga["forget_Q_A_ROUGE"]["value_by_index"]

retain_prob = retain["forget_Q_A_Prob"]["value_by_index"]
ga_prob = ga["forget_Q_A_Prob"]["value_by_index"]


def extract_question(input_text):
    match = re.search(
        r"user\s*\n+(.*?)assistant\s*$",
        input_text,
        flags=re.S
    )

    if match:
        return match.group(1).strip()

    return input_text.strip()


def clean_generation(text):
    text = text.strip()

    # Prevent extremely long degenerate outputs from
    # destroying the figure layout.
    if len(text) > 350:
        return text[:350] + " ... [truncated]"

    return text


rows = []

indices = sorted(
    retain_rouge.keys(),
    key=lambda x: int(x)
)

for idx in indices:

    r = retain_rouge[idx]
    g = ga_rouge[idx]

    rp = retain_prob[idx]
    gp = ga_prob[idx]

    rows.append({
        "sample_id": int(idx),
        "question": extract_question(r["input"]),
        "ground_truth": r["ground_truth"],
        "retain_generation": r["generation"],
        "gradascent_generation": g["generation"],
        "retain_rougeL_f1": r["rougeL_f1"],
        "gradascent_rougeL_f1": g["rougeL_f1"],
        "retain_prob": rp["prob"],
        "gradascent_prob": gp["prob"],
        "retain_avg_loss": rp["avg_loss"],
        "gradascent_avg_loss": gp["avg_loss"],
    })


# ---------------------------------
# Save every forget example to CSV
# ---------------------------------

csv_path = TABLE_DIR / "forget_examples.csv"

with csv_path.open(
    "w",
    newline="",
    encoding="utf-8"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=rows[0].keys()
    )

    writer.writeheader()
    writer.writerows(rows)


# ---------------------------------
# Objective example selection
#
# Select samples with the largest
# decrease in ROUGE-L F1.
# ---------------------------------

for row in rows:
    row["rouge_drop"] = (
        float(row["retain_rougeL_f1"])
        - float(row["gradascent_rougeL_f1"])
    )

selected = sorted(
    rows,
    key=lambda x: x["rouge_drop"],
    reverse=True
)[:3]


# ---------------------------------
# Build qualitative figure
# ---------------------------------

fig, axes = plt.subplots(
    len(selected),
    1,
    figsize=(14, 12)
)

if len(selected) == 1:
    axes = [axes]


for ax, row in zip(axes, selected):

    ax.axis("off")

    question = textwrap.fill(
        row["question"],
        width=100
    )

    truth = textwrap.fill(
        row["ground_truth"],
        width=100
    )

    retain_text = textwrap.fill(
        clean_generation(
            row["retain_generation"]
        ),
        width=100
    )

    ga_text = textwrap.fill(
        clean_generation(
            row["gradascent_generation"]
        ),
        width=100
    )

    text = (
        f"Sample {row['sample_id']}\n\n"
        f"Question:\n{question}\n\n"
        f"Ground Truth:\n{truth}\n\n"
        f"Retain99 Generation:\n{retain_text}\n"
        f"ROUGE-L F1 = "
        f"{float(row['retain_rougeL_f1']):.4f}   "
        f"Prob = {float(row['retain_prob']):.4f}\n\n"
        f"GradAscent Generation:\n{ga_text}\n"
        f"ROUGE-L F1 = "
        f"{float(row['gradascent_rougeL_f1']):.4f}   "
        f"Prob = {float(row['gradascent_prob']):.4f}"
    )

    ax.text(
        0,
        1,
        text,
        va="top",
        ha="left",
        fontsize=9,
        family="monospace"
    )


fig.suptitle(
    "Qualitative Forget Examples: "
    "Retain99 vs GradAscent",
    fontsize=15
)

plt.tight_layout(
    rect=[0, 0, 1, 0.97]
)

png_path = (
    FIG_DIR
    / "03_forget_examples.png"
)

plt.savefig(
    png_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("Total forget samples:", len(rows))

print("\nSaved CSV:")
print(csv_path)

print("\nSelected samples:")

for row in selected:
    print(
        "sample",
        row["sample_id"],
        "| retain ROUGE:",
        row["retain_rougeL_f1"],
        "| GradAscent ROUGE:",
        row["gradascent_rougeL_f1"],
        "| drop:",
        row["rouge_drop"]
    )

print("\nSaved figure:")
print(png_path)
