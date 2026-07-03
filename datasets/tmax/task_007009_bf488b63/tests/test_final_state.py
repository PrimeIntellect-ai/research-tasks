# test_final_state.py
import os
import json
import csv
import pytest

def compute_expected_metrics(csv_path):
    processed_rows = 0
    temp_ratios = []
    x_vals = []
    y_vals = []

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            status = row['status'].strip()
            if status == "OK":
                processed_rows += 1
                temp = float(row['temperature'])
                hum = float(row['humidity'])

                temp_ratios.append(temp / hum)
                x_vals.append(temp)
                y_vals.append(hum)

    if processed_rows == 0:
        return 0, 0.0, 0.0, 0.0

    avg_temp_ratio = sum(temp_ratios) / processed_rows

    mean_x = sum(x_vals) / processed_rows
    mean_y = sum(y_vals) / processed_rows

    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_vals, y_vals))
    var = sum((x - mean_x) ** 2 for x in x_vals)

    slope = cov / var if var != 0 else 0.0
    intercept = mean_y - slope * mean_x

    return processed_rows, avg_temp_ratio, slope, intercept

def test_results_json_exists_and_correct():
    results_path = "/home/user/results.json"
    csv_path = "/home/user/data/sensors.csv"

    assert os.path.exists(results_path), f"Expected results file at {results_path} does not exist."
    assert os.path.exists(csv_path), f"Expected data file at {csv_path} does not exist."

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON.")

    expected_rows, expected_avg_ratio, expected_slope, expected_intercept = compute_expected_metrics(csv_path)

    assert "processed_rows" in results, "Missing 'processed_rows' in results.json"
    assert "average_temp_ratio" in results, "Missing 'average_temp_ratio' in results.json"
    assert "model_slope" in results, "Missing 'model_slope' in results.json"
    assert "model_intercept" in results, "Missing 'model_intercept' in results.json"

    assert results["processed_rows"] == expected_rows, f"processed_rows is incorrect. Expected {expected_rows}, got {results['processed_rows']}"
    assert results["average_temp_ratio"] == pytest.approx(expected_avg_ratio, rel=1e-3), f"average_temp_ratio is incorrect. Expected approx {expected_avg_ratio}, got {results['average_temp_ratio']}"
    assert results["model_slope"] == pytest.approx(expected_slope, rel=1e-3), f"model_slope is incorrect. Expected approx {expected_slope}, got {results['model_slope']}"
    assert results["model_intercept"] == pytest.approx(expected_intercept, rel=1e-3), f"model_intercept is incorrect. Expected approx {expected_intercept}, got {results['model_intercept']}"

def test_cargo_toml_dependencies():
    cargo_toml_path = "/home/user/sensor_etl/Cargo.toml"
    assert os.path.exists(cargo_toml_path), f"Expected Cargo.toml at {cargo_toml_path} does not exist."

    with open(cargo_toml_path, 'r') as f:
        content = f.read()

    assert "linreg" in content, "The 'linreg' crate is missing from Cargo.toml dependencies."