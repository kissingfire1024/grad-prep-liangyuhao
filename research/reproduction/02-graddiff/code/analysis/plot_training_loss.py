import json
import csv
import sys
from pathlib import Path

import matplotlib.pyplot as plt


# Usage:
# python plot_training_loss.py <trainer_state.json> <result_root>

if len(sys.argv) != 3:
    print(
        "Usage: python plot_training_loss.py "
        "<trainer_state.json> <result_root>"
    )
    sys.exit(1)

SOURCE = Path(sys.argv[1])
RESULT_ROOT = Path(sys.argv[2])

if not SOURCE.exists():
    raise FileNotFoundError(f"trainer_state.json not found: {SOURCE}")

FIGURE_DIR = RESULT_ROOT / "figures"
TABLE_DIR = RESULT_ROOT / "tables"

FIGURE_DIR.mkdir(parents=True, exist_ok=True)
TABLE_DIR.mkdir(parents=True, exist_ok=True)


with SOURCE.open("r") as f:
    state = json.load(f)


records = [
    x for x in state["log_history"]
    if "loss" in x
]

if not records:
    raise RuntimeError("No training loss records found in trainer_state.json")


steps = [x["step"] for x in records]
epochs = [x["epoch"] for x in records]
losses = [x["loss"] for x in records]
grad_norms = [x.get("grad_norm") for x in records]
learning_rates = [x.get("learning_rate") for x in records]


# -----------------------------
# Save raw training data
# -----------------------------

csv_path = TABLE_DIR / "training_loss.csv"

with csv_path.open("w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "step",
        "epoch",
        "loss",
        "grad_norm",
        "learning_rate"
    ])

    for row in zip(
        steps,
        epochs,
        losses,
        grad_norms,
        learning_rates
    ):
        writer.writerow(row)


# -----------------------------
# Plot GradDiff training loss
# -----------------------------

plt.figure(figsize=(9, 5.5))

plt.plot(
    steps,
    losses,
    marker="o",
    linewidth=2,
    markersize=4
)

plt.xlabel("Training Step")
plt.ylabel("GradDiff Loss")

plt.title(
    "GradDiff Training Loss\n"
    "TOFU forget01 · Llama-3.2-1B-Instruct"
)

plt.grid(
    True,
    alpha=0.25
)

plt.tight_layout()

png_path = FIGURE_DIR / "01_training_loss.png"

plt.savefig(
    png_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("Source:")
print(SOURCE)

print("\nSaved CSV:")
print(csv_path)

print("\nSaved figure:")
print(png_path)

print("\nNumber of loss records:", len(records))
print("First loss:", losses[0])
print("Final logged loss:", losses[-1])
