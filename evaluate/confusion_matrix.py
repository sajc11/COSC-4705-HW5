# confusion_matrix.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def build_confusion_matrix(filepath):
    y_true = []
    y_pred = []

    with open(filepath, "r") as f:
        for line in f:
            if "→ predicted:" in line and ", actual:" in line:
                parts = line.strip().split("→ predicted:")[1]
                pred, actual = parts.split(", actual:")
                y_pred.append(pred.strip())
                y_true.append(actual.strip())

    # Create DataFrame
    df = pd.DataFrame({'Actual': y_true, 'Predicted': y_pred})
    cm = pd.crosstab(df['Actual'], df['Predicted'], rownames=['Actual'], colnames=['Predicted'])

    print("\n Confusion Matrix:\n")
    print(cm)

    # Plot heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.title('Website Fingerprinting Confusion Matrix')
    plt.tight_layout()
    plt.savefig("./output/confusion_matrix.png")
    print("\n Saved heatmap to: output/confusion_matrix.png")

if __name__ == "__main__":
    build_confusion_matrix("./output/test_predictions.txt")
