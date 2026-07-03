# test_final_state.py

import os
import json
import csv
import math
import pytest

def test_audit_results_exist():
    """Test that the audit_results.json file exists."""
    assert os.path.isfile("/home/user/audit_results.json"), "The file /home/user/audit_results.json does not exist."

def test_audit_results_correctness():
    """Test that the values in audit_results.json are correct based on the data."""
    json_path = "/home/user/audit_results.json"
    csv_path = "/home/user/etl_dump.csv"

    assert os.path.isfile(json_path), "Missing audit_results.json"
    assert os.path.isfile(csv_path), "Missing etl_dump.csv"

    with open(json_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("audit_results.json is not a valid JSON file.")

    # Calculate expected values
    total_rows = 0
    corrupt_rows = 0
    x = []
    y = []

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rec_id = float(row[0])
            val = row[1]
            is_corrupt = 1.0 if ('.' in val or val == 'NaN') else 0.0

            x.append(rec_id)
            y.append(is_corrupt)
            total_rows += 1
            if is_corrupt == 1.0:
                corrupt_rows += 1

    mean_x = sum(x) / total_rows
    mean_y = sum(y) / total_rows

    cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / (total_rows - 1)
    expected_posterior_mean = (1.0 + corrupt_rows) / (2.0 + total_rows)

    assert "total_rows" in results, "Missing 'total_rows' in JSON output."
    assert "corrupt_rows" in results, "Missing 'corrupt_rows' in JSON output."
    assert "posterior_mean" in results, "Missing 'posterior_mean' in JSON output."
    assert "covariance" in results, "Missing 'covariance' in JSON output."

    assert results["total_rows"] == total_rows, f"Expected total_rows to be {total_rows}, got {results['total_rows']}"
    assert results["corrupt_rows"] == corrupt_rows, f"Expected corrupt_rows to be {corrupt_rows}, got {results['corrupt_rows']}"
    assert math.isclose(results["posterior_mean"], expected_posterior_mean, rel_tol=1e-5), f"Expected posterior_mean to be close to {expected_posterior_mean}, got {results['posterior_mean']}"
    assert math.isclose(results["covariance"], cov, rel_tol=1e-5), f"Expected covariance to be close to {cov}, got {results['covariance']}"

def test_audit_go_exists():
    """Test that the Go source code file exists."""
    assert os.path.isfile("/home/user/audit.go"), "The file /home/user/audit.go does not exist."