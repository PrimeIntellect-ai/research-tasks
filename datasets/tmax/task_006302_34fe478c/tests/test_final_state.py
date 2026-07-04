# test_final_state.py
import os
import json
import csv
import math
import pytest

def get_csv_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def calculate_imputed_A(data):
    sensor_a = []
    for row in data:
        val = row['sensor_A']
        if val == '' or val.lower() == 'nan':
            sensor_a.append(None)
        else:
            sensor_a.append(float(val))

    # Linear interpolation
    for i in range(len(sensor_a)):
        if sensor_a[i] is None:
            prev_idx = i - 1
            while prev_idx >= 0 and sensor_a[prev_idx] is None:
                prev_idx -= 1
            next_idx = i + 1
            while next_idx < len(sensor_a) and sensor_a[next_idx] is None:
                next_idx += 1

            if prev_idx >= 0 and next_idx < len(sensor_a):
                prev_val = sensor_a[prev_idx]
                next_val = sensor_a[next_idx]
                sensor_a[i] = prev_val + (next_val - prev_val) * (i - prev_idx) / (next_idx - prev_idx)

    # Forward fill
    for i in range(1, len(sensor_a)):
        if sensor_a[i] is None and sensor_a[i-1] is not None:
            sensor_a[i] = sensor_a[i-1]

    # Backward fill
    for i in range(len(sensor_a)-2, -1, -1):
        if sensor_a[i] is None and sensor_a[i+1] is not None:
            sensor_a[i] = sensor_a[i+1]

    return sum(sensor_a)

def calculate_clipped_B_mean(data):
    sensor_b = [float(row['sensor_B']) for row in data]

    def quantile(data_list, q):
        s = sorted(data_list)
        n = len(s)
        idx = (n - 1) * q
        lower = int(idx)
        upper = lower + 1
        weight = idx - lower
        if upper >= n:
            return s[lower]
        return s[lower] * (1 - weight) + s[upper] * weight

    p5 = quantile(sensor_b, 0.05)
    p95 = quantile(sensor_b, 0.95)

    clipped_b = [min(max(x, p5), p95) for x in sensor_b]
    return sum(clipped_b) / len(clipped_b)

def test_pipeline_results_file_exists():
    """Check if the pipeline_results.json file was created."""
    file_path = "/home/user/pipeline_results.json"
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_pipeline_results_content():
    """Validate the content and accuracy of the pipeline results."""
    result_path = "/home/user/pipeline_results.json"
    data_path = "/home/user/sensor_data.csv"

    with open(result_path, 'r', encoding='utf-8') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {result_path} does not contain valid JSON.")

    expected_keys = {"imputed_A_sum", "clipped_B_mean", "mse"}
    assert set(results.keys()) == expected_keys, f"Expected keys {expected_keys}, but got {set(results.keys())}."

    for key in expected_keys:
        assert isinstance(results[key], float) or isinstance(results[key], int), f"Value for {key} must be a number."

    csv_data = get_csv_data(data_path)

    expected_imputed_A_sum = calculate_imputed_A(csv_data)
    expected_clipped_B_mean = calculate_clipped_B_mean(csv_data)

    # Assert imputed_A_sum
    assert math.isclose(results["imputed_A_sum"], expected_imputed_A_sum, abs_tol=1e-3), \
        f"Expected imputed_A_sum approx {expected_imputed_A_sum:.4f}, got {results['imputed_A_sum']}"

    # Assert clipped_B_mean
    assert math.isclose(results["clipped_B_mean"], expected_clipped_B_mean, abs_tol=1e-3), \
        f"Expected clipped_B_mean approx {expected_clipped_B_mean:.4f}, got {results['clipped_B_mean']}"

    # Assert mse (using known expected value due to complexity of stdlib linear regression)
    expected_mse = 12.0003
    assert math.isclose(results["mse"], expected_mse, abs_tol=1e-2), \
        f"Expected mse approx {expected_mse:.4f}, got {results['mse']}"