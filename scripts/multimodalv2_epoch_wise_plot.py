from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
METRICS_DIR = PROJECT_ROOT / "outputs" / "metrics"
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Load CSV
df = pd.read_csv(METRICS_DIR / "epoch_wise_stats.csv")

# Smoothing using rolling average
window = 5

df["accuracy"] = df["accuracy"].rolling(window=window, center=True).mean()
df["val_accuracy"] = df["val_accuracy"].rolling(window=window, center=True).mean()
df["loss"] = df["loss"].rolling(window=window, center=True).mean()
df["val_loss"] = df["val_loss"].rolling(window=window, center=True).mean()

# -----------------------------
# Accuracy Plot
# -----------------------------
plt.figure(figsize=(8,5))
plt.plot(df["epoch"], df["accuracy"], linewidth=3, label="Training Accuracy")
plt.plot(df["epoch"], df["val_accuracy"], linewidth=3, label="Validation Accuracy")

plt.title("Training vs Validation Accuracy (Smoothed)")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "accuracy_smooth.png", dpi=300)
plt.show()

# -----------------------------
# Loss Plot
# -----------------------------
plt.figure(figsize=(8,5))
plt.plot(df["epoch"], df["loss"], linewidth=3, label="Training Loss")
plt.plot(df["epoch"], df["val_loss"], linewidth=3, label="Validation Loss")

plt.title("Training vs Validation Loss (Smoothed)")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig(FIGURES_DIR / "loss_smooth.png", dpi=300)
plt.show()
