import json
import csv
from pathlib import Path

import matplotlib.pyplot as plt


SOURCE = Path(
    "/home/research/open-unlearning/"
    "saves/unlearn/"
    "tofu_Llama-3.2-1B-Instruct_forget01_GradAscent_test/"
    "trainer_state.json"
)

RESULT_ROOT = Path(
    "/home/research/research/reproduction/"
    "01-openunlearning/results/gradascent_forget01"
)

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

steps = [x["step"] for x in records]
epochs = [x["epoch"] for x in records]
losses = [x["loss"] for x in records]
grad_norms = [x["grad_norm"] for x in records]
learning_rates = [x["learning_rate"] for x in records]


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
# Plot training loss
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
plt.ylabel("GradAscent Loss")

plt.title(
    "GradAscent Training Loss\n"
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


print("Saved CSV:")
print(csv_path)

print("\nSaved figure:")
print(png_path)

print("\nNumber of loss records:", len(records))
print("First loss:", losses[0])
print("Final logged loss:", losses[-1])

