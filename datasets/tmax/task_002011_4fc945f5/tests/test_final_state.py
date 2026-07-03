# test_final_state.py

import os
import json
import csv
import math

def test_clean_data_csv():
    clean_csv_path = "/home/user/clean_data.csv"
    assert os.path.isfile(clean_csv_path), f"Missing clean data file at {clean_csv_path}"

    with open(clean_csv_path, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) > 0, "Clean data file is empty"

    for i, row in enumerate(rows):
        assert "clicks" in row, "Missing 'clicks' column in clean data"
        clicks_val = row["clicks"]

        # Check that it's an integer string (no decimals)
        assert "." not in clicks_val, f"Row {i+1}: 'clicks' value '{clicks_val}' contains a decimal point. It must be strictly integer."

        try:
            clicks_int = int(clicks_val)
        except ValueError:
            assert False, f"Row {i+1}: 'clicks' value '{clicks_val}' is not a valid integer."

def test_experiment_json():
    json_path = "/home/user/experiment.json"
    assert os.path.isfile(json_path), f"Missing experiment log at {json_path}"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} is not valid JSON."

    expected_keys = {"cleaned_rows", "mean_response_time", "ci_lower", "ci_upper"}
    for key in expected_keys:
        assert key in data, f"Missing key '{key}' in experiment.json"

    clean_csv_path = "/home/user/clean_data.csv"
    assert os.path.isfile(clean_csv_path), "Cannot validate json values without clean_data.csv"

    with open(clean_csv_path, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    n = len(rows)
    assert data["cleaned_rows"] == n, f"Expected cleaned_rows to be {n}, got {data['cleaned_rows']}"

    response_times = []
    for row in rows:
        assert "response_time" in row, "Missing 'response_time' column in clean data"
        response_times.append(float(row["response_time"]))

    mean = sum(response_times) / n
    variance = sum((x - mean) ** 2 for x in response_times) / (n - 1) if n > 1 else 0
    std_dev = math.sqrt(variance)
    margin_of_error = 1.96 * (std_dev / math.sqrt(n))

    ci_lower = mean - margin_of_error
    ci_upper = mean + margin_of_error

    assert math.isclose(data["mean_response_time"], mean, rel_tol=1e-2), f"Expected mean_response_time ~ {mean:.3f}, got {data['mean_response_time']}"
    assert math.isclose(data["ci_lower"], ci_lower, rel_tol=1e-2), f"Expected ci_lower ~ {ci_lower:.3f}, got {data['ci_lower']}"
    assert math.isclose(data["ci_upper"], ci_upper, rel_tol=1e-2), f"Expected ci_upper ~ {ci_upper:.3f}, got {data['ci_upper']}"