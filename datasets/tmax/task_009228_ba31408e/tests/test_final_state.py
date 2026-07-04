# test_final_state.py

import os
import json
import csv
import math

def test_results_json_exists():
    assert os.path.exists('/home/user/output/results.json'), "results.json does not exist in /home/user/output/"
    assert os.path.isfile('/home/user/output/results.json'), "/home/user/output/results.json is not a file"

def test_results_json_content():
    results_path = '/home/user/output/results.json'
    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, "results.json is not valid JSON"

    # Required keys
    expected_keys = {
        "cleaned_row_count",
        "slope",
        "mean_x",
        "bootstrap_ci_lower",
        "bootstrap_ci_upper",
        "compute_time_ms"
    }
    missing_keys = expected_keys - set(results.keys())
    assert not missing_keys, f"results.json is missing keys: {missing_keys}"

    # Read and clean data to compute expected values
    csv_path = '/home/user/data/sensor_log.csv'
    assert os.path.exists(csv_path), "Original CSV file is missing"

    cleaned_x = []
    cleaned_y = []

    with open(csv_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sx = row['sensor_x']
            sy = row['sensor_y']
            if not sx or not sy or sx.lower() == 'nan' or sy.lower() == 'nan':
                continue
            try:
                x_val = float(sx)
                y_val = float(sy)
            except ValueError:
                continue

            if x_val > 1000.0:
                continue

            cleaned_x.append(x_val)
            cleaned_y.append(y_val)

    n = len(cleaned_x)
    assert results["cleaned_row_count"] == n, f"Expected cleaned_row_count to be {n}, got {results['cleaned_row_count']}"

    mean_x = sum(cleaned_x) / n
    mean_y = sum(cleaned_y) / n

    assert math.isclose(results["mean_x"], mean_x, rel_tol=1e-2), f"Expected mean_x ~ {mean_x:.4f}, got {results['mean_x']}"

    # Calculate slope
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(cleaned_x, cleaned_y))
    denominator = sum((x - mean_x) ** 2 for x in cleaned_x)
    expected_slope = numerator / denominator

    assert math.isclose(results["slope"], expected_slope, rel_tol=1e-2), f"Expected slope ~ {expected_slope:.4f}, got {results['slope']}"

    # Calculate analytical CI bounds
    variance_x = sum((x - mean_x) ** 2 for x in cleaned_x) / (n - 1)
    std_x = math.sqrt(variance_x)
    margin_of_error = 1.96 * (std_x / math.sqrt(n))

    expected_ci_lower = mean_x - margin_of_error
    expected_ci_upper = mean_x + margin_of_error

    assert abs(results["bootstrap_ci_lower"] - expected_ci_lower) <= 1.0, f"bootstrap_ci_lower {results['bootstrap_ci_lower']} is not within 1.0 of analytical bound {expected_ci_lower:.4f}"
    assert abs(results["bootstrap_ci_upper"] - expected_ci_upper) <= 1.0, f"bootstrap_ci_upper {results['bootstrap_ci_upper']} is not within 1.0 of analytical bound {expected_ci_upper:.4f}"

    assert isinstance(results["compute_time_ms"], (int, float)) and results["compute_time_ms"] > 0, "compute_time_ms must be a positive number"