# test_final_state.py

import os
import json
import math
import pytest

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_results_json():
    json_path = "/home/user/results.json"
    assert os.path.isfile(json_path), f"Results file {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    dataset_path = "/home/user/dataset.csv"
    assert os.path.isfile(dataset_path), f"Dataset file {dataset_path} missing."

    with open(dataset_path, "r") as f:
        lines = f.readlines()

    data = []
    for line in lines[1:]:
        parts = line.strip().split(',')
        if len(parts) == 2:
            data.append((float(parts[0]), float(parts[1])))

    assert len(data) == 100, f"Expected 100 data rows in dataset, got {len(data)}"

    train_data = data[:80]
    test_data = data[80:]

    train_x = [d[0] for d in train_data]
    train_y = [d[1] for d in train_data]
    test_x = [d[0] for d in test_data]
    test_y = [d[1] for d in test_data]

    mean_x = sum(train_x) / len(train_x)
    mean_y = sum(train_y) / len(train_y)

    std_x = math.sqrt(sum((x - mean_x)**2 for x in train_x) / len(train_x))
    std_y = math.sqrt(sum((y - mean_y)**2 for y in train_y) / len(train_y))

    train_x_scaled = [(x - mean_x) / std_x for x in train_x]
    train_y_scaled = [(y - mean_y) / std_y for y in train_y]

    test_x_scaled = [(x - mean_x) / std_x for x in test_x]
    test_y_scaled = [(y - mean_y) / std_y for y in test_y]

    sum_x2 = sum(x**2 for x in train_x_scaled)
    sum_xy = sum(x * y for x, y in zip(train_x_scaled, train_y_scaled))

    m = sum_xy / sum_x2
    b = (sum(train_y_scaled) - m * sum(train_x_scaled)) / len(train_x_scaled)

    preds = [m * x + b for x in test_x_scaled]
    mse = sum((act - pred)**2 for act, pred in zip(test_y_scaled, preds)) / len(test_y_scaled)

    expected = {
        "train_mean_X": mean_x,
        "train_std_X": std_x,
        "train_mean_Y": mean_y,
        "train_std_Y": std_y,
        "model_m": m,
        "model_b": b,
        "test_mse": mse
    }

    for key, expected_val in expected.items():
        assert key in results, f"Key '{key}' missing in results.json"
        try:
            actual_val = float(results[key])
        except ValueError:
            pytest.fail(f"Value for {key} in results.json is not a valid float: {results[key]}")

        assert abs(actual_val - expected_val) <= 0.0002, (
            f"Value for {key} expected ~{expected_val:.4f}, got {actual_val}"
        )