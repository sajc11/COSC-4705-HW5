# confusion_matrix_knn.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def build_confusion_matrix(filepath, output_png):
    y_true = []
    y_pred = []

    with open(filepath, "r") as f:
        for line in f:
            if "→ predicted:" in line and ", actual:" in line:
                parts = line.strip().split("→ predicted:")[1]
                pred, actual = parts.split(", actual:")
                y_pred.append(pred.strip())
                y_true.append(actual.strip())

    df = pd.DataFrame({'Actual': y_true, 'Predicted': y_pred})
    cm = pd.crosstab(df['Actual'], df['Predicted'], rownames=['Actual'], colnames=['Predicted'])

    print("\n k-NN Confusion Matrix:\n")
    print(cm)

    # Plot
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Greens', cbar=False)
    plt.title('k-NN Confusion Matrix')
    plt.tight_layout()
    plt.savefig(output_png)
    print(f"\n Saved to: {output_png}")

if __name__ == "__main__":
    build_confusion_matrix("./output/test_predictions_knn.txt", "./output/confusion_matrix_knn.png")
