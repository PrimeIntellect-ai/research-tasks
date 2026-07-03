# test_final_state.py

import os
import json
import csv
import math
from collections import Counter
import pytest

def compute_embedding(text):
    vowels = set("aeiouAEIOU")
    whitespaces = set(" \t\n\r")

    length = len(text)
    v_count = sum(1 for c in text if c in vowels)
    w_count = sum(1 for c in text if c in whitespaces)
    # Consonants are letters that are not vowels
    c_count = sum(1 for c in text if c.isalpha() and c not in vowels)
    ascii_sum = sum(ord(c) for c in text) % 100

    return [float(length), float(v_count), float(c_count), float(w_count), float(ascii_sum)]

def euclidean_distance(v1, v2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

def solve_knn():
    dataset_path = "/home/user/dataset.csv"
    assert os.path.isfile(dataset_path), "Dataset file missing."

    valid_data = []
    with open(dataset_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                int(row["id"])
            except ValueError:
                continue

            text = row["text"]
            if not text:
                continue

            label = row["label"]
            if not label:
                continue

            valid_data.append({
                "text": text,
                "label": label,
                "embedding": compute_embedding(text)
            })

    assert len(valid_data) == 20, f"Expected 20 valid rows, found {len(valid_data)}"

    folds = [valid_data[i:i+4] for i in range(0, 20, 4)]
    assert len(folds) == 5, "Expected exactly 5 folds."

    k_accuracies = {}
    for k in [1, 3, 5]:
        correct = 0
        total = 0

        for i in range(5):
            val_fold = folds[i]
            train_fold = []
            for j in range(5):
                if i != j:
                    train_fold.extend(folds[j])

            for val_item in val_fold:
                distances = []
                for train_item in train_fold:
                    dist = euclidean_distance(val_item["embedding"], train_item["embedding"])
                    distances.append((dist, train_item["label"]))

                distances.sort(key=lambda x: x[0])
                neighbors = distances[:k]

                label_counts = {}
                for _, lbl in neighbors:
                    label_counts[lbl] = label_counts.get(lbl, 0) + 1

                max_count = max(label_counts.values())
                best_labels = [lbl for lbl, count in label_counts.items() if count == max_count]
                best_labels.sort()
                predicted_label = best_labels[0]

                if predicted_label == val_item["label"]:
                    correct += 1
                total += 1

        k_accuracies[k] = correct / total

    best_k = None
    best_acc = -1.0
    for k in [1, 3, 5]:
        if k_accuracies[k] > best_acc:
            best_acc = k_accuracies[k]
            best_k = k

    return best_k, best_acc

def test_tuning_results():
    results_path = "/home/user/tuning_results.json"
    assert os.path.isfile(results_path), f"Output file {results_path} does not exist."

    with open(results_path, "r", encoding="utf-8") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("tuning_results.json is not valid JSON.")

    assert "best_k" in results, "Missing 'best_k' in tuning_results.json"
    assert "best_accuracy" in results, "Missing 'best_accuracy' in tuning_results.json"

    expected_k, expected_acc = solve_knn()

    actual_k = results["best_k"]
    actual_acc = results["best_accuracy"]

    assert actual_k == expected_k, f"Expected best_k to be {expected_k}, but got {actual_k}."
    assert abs(actual_acc - expected_acc) < 1e-5, f"Expected best_accuracy to be {expected_acc}, but got {actual_acc}."