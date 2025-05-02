# classify_site_knn.py

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
from collections import Counter
import os

CSV_PATH = "./output/stats.csv"
OUTPUT_PATH = "./output/test_predictions_knn.txt"
K = 3  # Number of neighbors

def load_data(csv_path):
    df = pd.read_csv(csv_path)
    train_df = df[df['file'].str.contains("train")]
    test_df = df[df['file'].str.contains("test")]
    return train_df, test_df

def classify_knn(test_vector, train_df, k=3):
    distances = []

    for _, row in train_df.iterrows():
        label = row['label']
        vector = row.iloc[2:].values
        dist = euclidean_distances([test_vector], [vector])[0][0]
        distances.append((dist, label))

    # Sort by distance, take top k
    top_k = sorted(distances)[:k]
    top_labels = [label for _, label in top_k]

    # Majority vote
    vote = Counter(top_labels).most_common(1)[0][0]
    return vote

def main():
    if not os.path.exists(CSV_PATH):
        print("[!] stats.csv not found.")
        return

    train_df, test_df = load_data(CSV_PATH)

    with open(OUTPUT_PATH, "w") as f_out:
        for _, row in test_df.iterrows():
            fname = row['file']
            true_label = row['label']
            test_vector = row.iloc[2:].values
            predicted_label = classify_knn(test_vector, train_df, k=K)

            result = f"{fname} → predicted: {predicted_label}, actual: {true_label}"
            print(result)
            f_out.write(result + "\n")

    print(f"\n[✓] k-NN classification (k={K}) complete. Results saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
