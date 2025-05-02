# `report.md`

```markdown
# Tor Website Fingerprinting

**Name:** Alivia Castor 
**Course:** COSC 4705  
**Assignment:** Homework 5  
**Date:** April 2025

---

## Overview

This project demonstrates how a traffic analysis attack known as website fingerprinting can be used to identify websites visited over the Tor network. While Tor encrypts payloads and anonymizes IPs, traffic patterns such as packet size, direction, and timing still leak enough information to infer a user’s destination.

---

## Methodology

### Data Collection

- **Websites:** `amazon.com`, `github.com`, `google.com`, `nytimes.com`, `steam.com`, `youtube.com`
- For each site:
  - Collected **4 training** and **1 test** packet capture (`.pcap`) files using `tcpdump`
  - Captured only traffic between my client and the **guard relay**: `138.201.121.103`
  - Used a custom Bash script to start `tcpdump`, load the site in Tor Browser, and record for 15 seconds

---

### Feature Extraction

- Used `scapy` to parse each `.pcap`
- Extracted:
  - `up/down packet count`
  - `up/down total bytes`
  - `inter-packet arrival mean`, `median`, `std` (in each direction)
- Saved all features to `stats.csv`

---

## Classifiers

### 1. **Centroid Classifier**
- Calculated average feature vector for each site (centroid)
- Classified test files by nearest centroid (Euclidean distance)

**Accuracy:** 2 / 6 = **33.33%**  
See `confusion_matrix.png`

---

### 2. **k-Nearest Neighbors (k=3)**
- Compared each test vector to all training vectors
- Predicted label by majority vote of the 3 nearest neighbors

**Accuracy:** 4 / 6 = **66.67%**  
See `confusion_matrix_knn.png`

---

### 3. **k-Nearest Neighbors (k=5)**
- We also evaluated a `k=5` version of the k-NN classifier
- Surprisingly, results were **identical to k=3**
- **Accuracy:** 4 / 6 = **66.67%**
- This suggests that, for this dataset, additional neighbors did not significantly alter predictions
- Most misclassifications leaned toward `amazon`, indicating a bias worth exploring with more advanced models or better features

---

### Why This Is Better Than Random Guessing

There are 6 classes (websites), so a naive classifier choosing uniformly at random would achieve an expected accuracy of **1/6 ≈ 16.67%**. In contrast:

- Our **centroid classifier** achieved 33.33% (double random guessing)
- Our **k-NN classifiers** achieved 66.67% (4× better than random)

This clearly shows that meaningful structure exists in the extracted packet metadata — the classifiers are detecting real, distinguishable patterns in the traffic, despite encryption and anonymization. The consistent results across both `k=3` and `k=5` further reinforce that the features are predictive, and not noise-driven.

---

## Visual Results

- See `comparison_matrix.png` for a side-by-side comparison of confusion matrices
- `google` was the most frequent misclassification in the centroid model
- `k-NN` model improved performance by using multiple neighbors instead of a single mean vector

---

## How to Run the Code

```bash
# Extract features from .pcaps
python analysis/extract_features.py

# Run baseline centroid classifier
python classify/classify_site.py

# Run k-NN classifier (k=3)
python classify/classify_site_knn.py

# Evaluate accuracy
python classify/evaluate_accuracy.py
python classify/evaluate_accuracy_knn.py

# Generate confusion matrices
python evaluate/confusion_matrix.py
python evaluate/confusion_matrix_knn.py

# Compare both visually
python evaluate/compare_matrices.py
```

All outputs are saved in the `output/` folder.

---

## Conclusion

This project demonstrates that even with encrypted Tor traffic, website fingerprinting remains viable by analyzing packet metadata. While the centroid method had limited accuracy, a simple k-NN model significantly improved predictions. With more features or better models (e.g., SVM, deep learning), accuracy could improve further. 

While the k-NN classifier achieved only moderate accuracy (4/6), this performance is both statistically and practically significant compared to random guessing. The model was able to identify real, reproducible patterns in encrypted Tor traffic using only packet direction, timing, and volume, without access to payloads or destination IPs. This underscores how vulnerable Tor is to traffic analysis, and highlights the importance of defenses such as traffic shaping, padding, or cover traffic.



---

## Attachments (included in submission)

- `data/pcaps/*.pcap`
- `analysis/extract_features.py`
- `classify/classify_site.py`
- `classify/classify_site_knn.py`
- `output/stats.csv`
- `output/test_predictions.txt`, `test_predictions_knn.txt`
- `output/confusion_matrix.png`, `confusion_matrix_knn.png`, `comparison_matrix.png`
