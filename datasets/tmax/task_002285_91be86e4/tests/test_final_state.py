# test_final_state.py

import os
import csv
import json
import math
import pytest

EVALUATE_GO_PATH = "/home/user/evaluate.go"
METRICS_JSON_PATH = "/home/user/metrics.json"
DATASET_PATH = "/home/user/dataset.csv"

def compute_embedding(text):
    counts = [0.0] * 26
    total = 0
    for char in text:
        if 'a' <= char <= 'z':
            counts[ord(char) - ord('a')] += 1
            total += 1
        elif 'A' <= char <= 'Z':
            counts[ord(char) - ord('A')] += 1
            total += 1
    if total == 0:
        return counts
    return [c / total for c in counts]

def compute_l2_distance(v1, v2):
    return sum((a - b) ** 2 for a, b in zip(v1, v2))

def get_expected_metrics():
    rows = []
    with open(DATASET_PATH, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({
                'id': int(row['id']),
                'category': row['category'],
                'embedding': compute_embedding(row['text'])
            })

    folds_accuracy = []

    for fold in range(5):
        test_start = fold * 20
        test_end = test_start + 20

        test_set = rows[test_start:test_end]
        train_set = rows[:test_start] + rows[test_end:]

        correct = 0
        for test_item in test_set:
            best_dist = float('inf')
            best_train_item = None

            for train_item in train_set:
                dist = compute_l2_distance(test_item['embedding'], train_item['embedding'])

                # Update if strictly better, or if equal distance and smaller id
                if dist < best_dist:
                    best_dist = dist
                    best_train_item = train_item
                elif math.isclose(dist, best_dist, rel_tol=1e-9, abs_tol=1e-11):
                    if train_item['id'] < best_train_item['id']:
                        best_train_item = train_item

            if best_train_item['category'] == test_item['category']:
                correct += 1

        folds_accuracy.append(correct / 20.0)

    mean_accuracy = sum(folds_accuracy) / 5.0
    return folds_accuracy, mean_accuracy

def test_evaluate_go_exists():
    assert os.path.exists(EVALUATE_GO_PATH), f"Go file {EVALUATE_GO_PATH} does not exist."
    assert os.path.isfile(EVALUATE_GO_PATH), f"Path {EVALUATE_GO_PATH} is not a file."

def test_metrics_json_exists_and_valid():
    assert os.path.exists(METRICS_JSON_PATH), f"Metrics file {METRICS_JSON_PATH} does not exist."

    try:
        with open(METRICS_JSON_PATH, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {METRICS_JSON_PATH} is not valid JSON.")

    assert "folds_accuracy" in data, "Missing 'folds_accuracy' in metrics.json"
    assert "mean_accuracy" in data, "Missing 'mean_accuracy' in metrics.json"
    assert "avg_inference_us" in data, "Missing 'avg_inference_us' in metrics.json"

    assert isinstance(data["folds_accuracy"], list), "'folds_accuracy' must be a list"
    assert len(data["folds_accuracy"]) == 5, "'folds_accuracy' must have exactly 5 elements"
    assert isinstance(data["mean_accuracy"], (int, float)), "'mean_accuracy' must be a number"
    assert isinstance(data["avg_inference_us"], int), "'avg_inference_us' must be an integer"
    assert data["avg_inference_us"] > 0, "'avg_inference_us' must be > 0"

def test_metrics_accuracy_values():
    with open(METRICS_JSON_PATH, 'r') as f:
        data = json.load(f)

    expected_folds, expected_mean = get_expected_metrics()

    actual_folds = data["folds_accuracy"]
    actual_mean = data["mean_accuracy"]

    for i, (actual, expected) in enumerate(zip(actual_folds, expected_folds)):
        assert math.isclose(actual, expected, abs_tol=1e-5), \
            f"Fold {i+1} accuracy mismatch. Expected {expected}, got {actual}"

    assert math.isclose(actual_mean, expected_mean, abs_tol=1e-5), \
        f"Mean accuracy mismatch. Expected {expected_mean}, got {actual_mean}"