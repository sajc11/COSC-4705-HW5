# evaluate_accuracy.py

def evaluate_predictions(filepath):
    correct = 0
    total = 0

    with open(filepath, "r") as f:
        for line in f:
            if "→ predicted:" in line and ", actual:" in line:
                parts = line.strip().split("→ predicted:")[1]
                pred, actual = parts.split(", actual:")
                pred = pred.strip()
                actual = actual.strip()
                total += 1
                if pred == actual:
                    correct += 1

    print(f"✅ Accuracy: {correct}/{total} = {correct / total:.2%}")

if __name__ == "__main__":
    evaluate_predictions("./output/test_predictions.txt")
