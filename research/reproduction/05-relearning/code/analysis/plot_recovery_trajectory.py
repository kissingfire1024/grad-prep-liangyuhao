from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path("/home/research/research/reproduction/05-relearning")
df = pd.read_csv(ROOT / "results/recovery_trajectory.csv")

# Figure 1: Forget Q/A Probability
plt.figure(figsize=(7, 4.5))
plt.plot(df["step"], df["forget_Q_A_Prob"], marker="o")
plt.xlabel("Cumulative Relearning Optimizer Steps")
plt.ylabel("Forget Q/A Probability")
plt.title("RMU Relearning Recovery: Target-Answer Probability")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(ROOT / "figures/01_relearning_probability.png", dpi=300)
plt.close()

# Figure 2: Forget Q/A ROUGE
plt.figure(figsize=(7, 4.5))
plt.plot(df["step"], df["forget_Q_A_ROUGE"], marker="o")
plt.xlabel("Cumulative Relearning Optimizer Steps")
plt.ylabel("Forget Q/A ROUGE")
plt.title("RMU Relearning Recovery: Free-Generation ROUGE")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(ROOT / "figures/02_relearning_rouge.png", dpi=300)
plt.close()

# Figure 3: Extraction Strength
plt.figure(figsize=(7, 4.5))
plt.plot(df["step"], df["extraction_strength"], marker="o")
plt.xlabel("Cumulative Relearning Optimizer Steps")
plt.ylabel("Extraction Strength")
plt.title("RMU Relearning Recovery: Extraction Strength")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.savefig(ROOT / "figures/03_relearning_extraction.png", dpi=300)
plt.close()

print(df.to_string(index=False))
print("\nSaved:")
for p in sorted((ROOT / "figures").glob("*.png")):
    print(p)
