# test_final_state.py

import os
import json
import csv
import statistics
import pytest

def test_results_json_exists():
    assert os.path.exists('/home/user/results.json'), "/home/user/results.json does not exist."
    assert os.path.isfile('/home/user/results.json'), "/home/user/results.json is not a file."

def test_results_json_content():
    with open('/home/user/results.json', 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/results.json is not valid JSON.")

    # Recompute expected median from the dataset
    dataset_path = '/home/user/dataset.csv'
    assert os.path.exists(dataset_path), f"Dataset file missing at {dataset_path}"

    with open(dataset_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        vals = []
        for row in reader:
            val = row.get('feature_A')
            if val != "MISSING" and val is not None:
                vals.append(int(val))

    expected_median = int(statistics.median(vals))

    assert "median_A" in data, "Key 'median_A' missing in results.json"
    assert data["median_A"] == expected_median, f"Expected 'median_A' to be {expected_median}, got {data['median_A']}"

    assert "feature_A_dtype" in data, "Key 'feature_A_dtype' missing in results.json"
    assert data["feature_A_dtype"] == "int64", f"Expected 'feature_A_dtype' to be 'int64', got {data['feature_A_dtype']}"

    assert "accuracy" in data, "Key 'accuracy' missing in results.json"
    assert isinstance(data["accuracy"], (int, float)), "Key 'accuracy' must be a float"
    assert float(data["accuracy"]) == 1.0, f"Expected 'accuracy' to be 1.0, got {data['accuracy']}"

    assert "inference_time_sec" in data, "Key 'inference_time_sec' missing in results.json"
    assert isinstance(data["inference_time_sec"], (int, float)), "Key 'inference_time_sec' must be a float"
    assert float(data["inference_time_sec"]) > 0, "Expected 'inference_time_sec' to be greater than 0"