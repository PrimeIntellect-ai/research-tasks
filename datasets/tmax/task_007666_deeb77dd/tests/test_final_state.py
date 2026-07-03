# test_final_state.py

import os
import csv
import math
import pytest

def compute_ground_truth():
    data_path = '/home/user/raw_data.csv'
    if not os.path.exists(data_path):
        return None

    data = []
    with open(data_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'id': int(row['id']),
                'value': float(row['value']),
                'label': int(row['label']),
                'fold': int(row['fold'])
            })

    results = {}
    for T in [2, 3, 4]:
        fold_accuracies = []
        for k in [1, 2, 3]:
            # Train
            train_vals = [d['value'] for d in data if d['fold'] != k and d['label'] == 0]
            n = len(train_vals)
            if n > 0:
                mean = sum(train_vals) / n
            else:
                mean = 0
            if n > 1:
                variance = sum((x - mean) ** 2 for x in train_vals) / (n - 1)
            else:
                variance = 0

            if variance == 0:
                std = 0.0001
            else:
                std = math.sqrt(variance)

            # Test
            test_data = [d for d in data if d['fold'] == k]
            correct = 0
            for d in test_data:
                pred = 1 if abs(d['value'] - mean) > T * std else 0
                if pred == d['label']:
                    correct += 1
            fold_accuracies.append(correct / len(test_data))

        results[T] = sum(fold_accuracies) / 3.0

    best_t = max(results.keys(), key=lambda t: (results[t], -t))
    return results, best_t

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/clean_pipeline.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_cv_results():
    results_path = "/home/user/cv_results.txt"
    assert os.path.exists(results_path), f"Results file {results_path} does not exist."

    gt = compute_ground_truth()
    assert gt is not None, "raw_data.csv is missing, cannot compute ground truth."
    expected_results, _ = gt

    with open(results_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"Expected 3 lines in {results_path}, got {len(lines)}."

    for i, T in enumerate([2, 3, 4]):
        expected_line = f"T={T}, Accuracy={expected_results[T]:.4f}"
        assert lines[i] == expected_line, f"Line {i+1} mismatch. Expected '{expected_line}', got '{lines[i]}'."

def test_best_t():
    best_t_path = "/home/user/best_t.txt"
    assert os.path.exists(best_t_path), f"Best T file {best_t_path} does not exist."

    gt = compute_ground_truth()
    assert gt is not None, "raw_data.csv is missing, cannot compute ground truth."
    _, expected_best_t = gt

    with open(best_t_path, 'r') as f:
        content = f.read().strip()

    assert content == str(expected_best_t), f"Expected best T to be '{expected_best_t}', got '{content}'."