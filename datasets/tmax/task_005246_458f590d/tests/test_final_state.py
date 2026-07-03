# test_final_state.py

import os
import json
import math
import pytest

def test_pipeline_output_and_logic():
    dataset_path = "/home/user/dataset.csv"
    metrics_path = "/home/user/metrics.json"
    cpp_path = "/home/user/pipeline.cpp"

    assert os.path.exists(cpp_path), f"C++ source file {cpp_path} is missing."
    assert os.path.exists(metrics_path), f"Metrics file {metrics_path} is missing."

    # Read dataset to compute the expected results dynamically
    assert os.path.exists(dataset_path), f"Dataset file {dataset_path} is missing."
    with open(dataset_path, 'r') as f:
        lines = f.read().strip().split('\n')

    data = []
    for line in lines[1:]:  # Skip header
        parts = line.split(',')
        data.append((int(parts[0]), float(parts[1]), float(parts[2]), int(parts[3])))

    # 2. Train/Test Split
    train = data[:80]
    test = data[80:]

    # 3. Leakage-Free Feature Engineering
    mean_f1 = sum(x[1] for x in train) / 80.0
    mean_f2 = sum(x[2] for x in train) / 80.0

    std_f1 = math.sqrt(sum((x[1] - mean_f1)**2 for x in train) / 79.0)
    std_f2 = math.sqrt(sum((x[2] - mean_f2)**2 for x in train) / 79.0)

    train_scaled = [(x[0], (x[1]-mean_f1)/std_f1, (x[2]-mean_f2)/std_f2, x[3]) for x in train]
    test_scaled = [(x[0], (x[1]-mean_f1)/std_f1, (x[2]-mean_f2)/std_f2, x[3]) for x in test]

    # 4. Model Inference (Similarity Search)
    correct = 0
    for ts in test_scaled:
        best_dist = float('inf')
        best_label = -1
        best_id = float('inf')
        for tr in train_scaled:
            dist = math.sqrt((ts[1] - tr[1])**2 + (ts[2] - tr[2])**2)
            if dist < best_dist:
                best_dist = dist
                best_label = tr[3]
                best_id = tr[0]
            elif dist == best_dist and tr[0] < best_id:
                best_dist = dist
                best_label = tr[3]
                best_id = tr[0]
        if best_label == ts[3]:
            correct += 1

    # 5. Experiment Tracking
    accuracy = correct / 20.0

    expected_json = {
        "train_mean_f1": round(mean_f1, 4),
        "train_mean_f2": round(mean_f2, 4),
        "test_accuracy": round(accuracy, 4)
    }

    # Parse actual metrics
    with open(metrics_path, 'r') as f:
        try:
            actual_json = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {metrics_path} is not valid JSON.")

    # Validate structure and values
    for key in expected_json:
        assert key in actual_json, f"Missing key '{key}' in {metrics_path}"
        assert math.isclose(actual_json[key], expected_json[key], abs_tol=1e-4), \
            f"Value for '{key}' is incorrect. Expected {expected_json[key]}, got {actual_json[key]}"