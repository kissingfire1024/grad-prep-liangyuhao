import json
import csv
from pathlib import Path

import matplotlib.pyplot as plt

STATE_PATH = Path(
    "/home/research/open-unlearning/saves/unlearn/"
    "tofu_Llama-3.2-1B-Instruct_forget01_RMU_test/"
    "trainer_state.json"
)

RESULT_DIR = Path(
    "/home/research/research/reproduction/"
    "04-rmu/results/rmu_forget01"
)

TABLE_DIR = RESULT_DIR / "tables"
FIGURE_DIR = RESULT_DIR / "figures"

TABLE_DIR.mkdir(parents=True, exist_ok=True)
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

with open(STATE_PATH, "r") as f:
    state = json.load(f)

logs = [
    x for x in state["log_history"]
    if "loss" in x
]

# -------------------------
# Export CSV
# -------------------------

csv_path = TABLE_DIR / "training_loss.csv"

with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "step",
        "epoch",
        "loss",
        "learning_rate",
        "grad_norm"
    ])

    for x in logs:
        writer.writerow([
            x.get("step"),
            x.get("epoch"),
            x.get("loss"),
            x.get("learning_rate"),
            x.get("grad_norm")
        ])

# -------------------------
# Plot training loss
# -------------------------

steps = [x["step"] for x in logs]
losses = [x["loss"] for x in logs]

plt.figure(figsize=(8, 5))

plt.plot(
    steps,
    losses,
    marker="o",
    linewidth=2
)

plt.xlabel("Training Step")
plt.ylabel("RMU Training Loss")
plt.title("Experiment 004: RMU Training Loss")

plt.grid(alpha=0.25)
plt.tight_layout()

fig_path = FIGURE_DIR / "01_training_loss.png"

plt.savefig(
    fig_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("Loss records:", len(logs))
print("First loss:", logs[0]["loss"])
print("Final loss:", logs[-1]["loss"])
print("Minimum loss:", min(losses))

print("\nSaved CSV:")
print(csv_path)

print("\nSaved figure:")
print(fig_path)
