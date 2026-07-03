# test_final_state.py

import os
import json
import csv
import math
import pytest

def test_files_exist():
    assert os.path.exists("/home/user/pipeline.go"), "The file /home/user/pipeline.go is missing."
    assert os.path.exists("/home/user/Makefile"), "The file /home/user/Makefile is missing."
    assert os.path.exists("/home/user/output/metrics.json"), "The file /home/user/output/metrics.json is missing."

def compute_expected_metrics():
    csv_path = "/home/user/sensor_data.csv"
    valid_rows = []

    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                a = float(row["sensor_A"])
                b = float(row["sensor_B"])
                c = float(row["sensor_C"])

                if 0.0 <= a <= 1000.0 and 0.0 <= b <= 1000.0 and 0.0 <= c <= 1000.0:
                    valid_rows.append({"A": a, "B": b, "C": c})
            except ValueError:
                continue

    n = len(valid_rows)
    assert n > 1, "Not enough valid rows to compute statistics."

    mean_a = sum(r["A"] for r in valid_rows) / n
    mean_b = sum(r["B"] for r in valid_rows) / n
    mean_c = sum(r["C"] for r in valid_rows) / n

    cov_ac = sum((r["A"] - mean_a) * (r["C"] - mean_c) for r in valid_rows) / (n - 1)

    cov_ab = sum((r["A"] - mean_a) * (r["B"] - mean_b) for r in valid_rows) / (n - 1)
    var_a = sum((r["A"] - mean_a) ** 2 for r in valid_rows) / (n - 1)
    var_b = sum((r["B"] - mean_b) ** 2 for r in valid_rows) / (n - 1)

    corr_ab = cov_ab / math.sqrt(var_a * var_b)

    return {
        "correlation_A_B": round(corr_ab, 4),
        "covariance_A_C": round(cov_ac, 4),
        "validation_status": "pass" if corr_ab >= 0.8 else "fail"
    }

def test_metrics_json_content():
    json_path = "/home/user/output/metrics.json"

    with open(json_path, "r") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    expected_data = compute_expected_metrics()

    assert "correlation_A_B" in actual_data, "Missing 'correlation_A_B' in JSON output."
    assert "covariance_A_C" in actual_data, "Missing 'covariance_A_C' in JSON output."
    assert "validation_status" in actual_data, "Missing 'validation_status' in JSON output."

    assert isinstance(actual_data["correlation_A_B"], float), "correlation_A_B must be a float."
    assert isinstance(actual_data["covariance_A_C"], float), "covariance_A_C must be a float."

    assert actual_data["correlation_A_B"] == expected_data["correlation_A_B"], f"Expected correlation_A_B to be {expected_data['correlation_A_B']}, got {actual_data['correlation_A_B']}"
    assert actual_data["covariance_A_C"] == expected_data["covariance_A_C"], f"Expected covariance_A_C to be {expected_data['covariance_A_C']}, got {actual_data['covariance_A_C']}"
    assert actual_data["validation_status"] == expected_data["validation_status"], f"Expected validation_status to be '{expected_data['validation_status']}', got '{actual_data['validation_status']}'"

def test_makefile_contains_run():
    makefile_path = "/home/user/Makefile"
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "run:" in content, "Makefile does not contain a 'run' target."