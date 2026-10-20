import csv
import json
import re
import textwrap
from pathlib import Path

import matplotlib.pyplot as plt


BASE = Path("/home/research/research/reproduction")

RETAIN_PATH = (
    BASE /
    "01-openunlearning/results/retain99/TOFU_EVAL.json"
)

GD_PATH = (
    BASE /
    "02-graddiff/results/graddiff_forget01/TOFU_EVAL.json"
)

RESULT_ROOT = (
    BASE /
    "02-graddiff/results/graddiff_forget01"
)

FIG_DIR = RESULT_ROOT / "figures"
TABLE_DIR = RESULT_ROOT / "tables"

FIG_DIR.mkdir(parents=True, exist_ok=True)
TABLE_DIR.mkdir(parents=True, exist_ok=True)


with RETAIN_PATH.open() as f:
    retain = json.load(f)

with GD_PATH.open() as f:
    gd = json.load(f)


retain_rouge = retain["forget_Q_A_ROUGE"]["value_by_index"]
gd_rouge = gd["forget_Q_A_ROUGE"]["value_by_index"]

retain_prob = retain["forget_Q_A_Prob"]["value_by_index"]
gd_prob = gd["forget_Q_A_Prob"]["value_by_index"]


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
    g = gd_rouge[idx]

    rp = retain_prob[idx]
    gp = gd_prob[idx]

    rows.append({
        "sample_id": int(idx),
        "question": extract_question(r["input"]),
        "ground_truth": r["ground_truth"],

        "retain_generation": r["generation"],
        "graddiff_generation": g["generation"],

        "retain_rougeL_f1": r["rougeL_f1"],
        "graddiff_rougeL_f1": g["rougeL_f1"],

        "retain_prob": rp["prob"],
        "graddiff_prob": gp["prob"],

        "retain_avg_loss": rp["avg_loss"],
        "graddiff_avg_loss": gp["avg_loss"],
    })


# ---------------------------------
# Objective example selection
# ---------------------------------

for row in rows:
    row["rouge_drop"] = (
        float(row["retain_rougeL_f1"])
        - float(row["graddiff_rougeL_f1"])
    )


# ---------------------------------
# Save every forget example
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

    gd_text = textwrap.fill(
        clean_generation(
            row["graddiff_generation"]
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
        f"Prob = "
        f"{float(row['retain_prob']):.4f}\n\n"

        f"GradDiff Generation:\n{gd_text}\n"
        f"ROUGE-L F1 = "
        f"{float(row['graddiff_rougeL_f1']):.4f}   "
        f"Prob = "
        f"{float(row['graddiff_prob']):.4e}"
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
    "Retain99 vs GradDiff",
    fontsize=15
)

plt.tight_layout(
    rect=[0, 0, 1, 0.97]
)


png_path = (
    FIG_DIR /
    "03_forget_examples.png"
)

plt.savefig(
    png_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("Total forget samples:", len(rows))

print("\nSources:")
print("Retain99:", RETAIN_PATH)
print("GradDiff:", GD_PATH)

print("\nSaved CSV:")
print(csv_path)

print("\nSelected samples:")

for row in selected:
    print(
        "sample",
        row["sample_id"],
        "| retain ROUGE:",
        row["retain_rougeL_f1"],
        "| GradDiff ROUGE:",
        row["graddiff_rougeL_f1"],
        "| drop:",
        row["rouge_drop"]
    )

    print(
        "  GradDiff generation preview:",
        repr(
            clean_generation(
                row["graddiff_generation"]
            )[:180]
        )
    )

print("\nSaved figure:")
print(png_path)
