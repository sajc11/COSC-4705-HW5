import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
import os

# === CONFIG ===
CSV_PATH = "./output/stats.csv"
OUTPUT_PATH = "./output/test_predictions.txt"

def load_data(csv_path):
    df = pd.read_csv(csv_path)
    
    # Split into training and test sets
    train_df = df[df['file'].str.contains("train")]
    test_df = df[df['file'].str.contains("test")]
    
    return train_df, test_df

def compute_centroids(train_df):
    centroids = {}

    for label in train_df['label'].unique():
        site_data = train_df[train_df['label'] == label]
        feature_matrix = site_data.iloc[:, 2:].values
        centroid = np.mean(feature_matrix, axis=0)
        centroids[label] = centroid

    return centroids

def classify(test_vector, centroids):
    min_dist = float("inf")
    best_label = None

    for label, centroid in centroids.items():
        dist = euclidean_distances([test_vector], [centroid])[0][0]
        if dist < min_dist:
            min_dist = dist
            best_label = label

    return best_label

def main():
    if not os.path.exists(CSV_PATH):
        print("[!] stats.csv not found.")
        return

    train_df, test_df = load_data(CSV_PATH)
    centroids = compute_centroids(train_df)

    with open(OUTPUT_PATH, "w") as f_out:
        for _, row in test_df.iterrows():
            fname = row['file']
            true_label = row['label']
            test_vector = row.iloc[2:].values
            predicted_label = classify(test_vector, centroids)

            result = f"{fname} → predicted: {predicted_label}, actual: {true_label}"
            print(result)
            f_out.write(result + "\n")

    print(f"\n[✓] Classification complete. Results saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
