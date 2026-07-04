# test_final_state.py

import os
import csv
import math
import pytest

def test_bad_commit_recorded():
    bad_commit_path = "/home/user/bad_commit.txt"
    expected_bad_commit_path = "/tmp/expected_bad_commit.txt"

    assert os.path.isfile(bad_commit_path), f"File not found: {bad_commit_path}"
    assert os.path.isfile(expected_bad_commit_path), f"Truth file not found: {expected_bad_commit_path}"

    with open(bad_commit_path, "r") as f:
        actual_commit = f.read().strip()

    with open(expected_bad_commit_path, "r") as f:
        expected_commit = f.read().strip()

    assert actual_commit == expected_commit, f"Incorrect bad commit hash recorded. Expected {expected_commit}, got {actual_commit}"

def test_fixed_metrics_csv_generated_and_correct():
    input_csv = "/home/user/data.csv"
    output_csv = "/home/user/fixed_metrics.csv"

    assert os.path.isfile(input_csv), f"Input file missing: {input_csv}"
    assert os.path.isfile(output_csv), f"Output file missing: {output_csv}"

    # Read input data to compute expected values
    expected_values = {}
    with open(input_csv, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            expected_values[row['metric_id']] = math.sqrt(float(row['value']))

    # Read output data and compare
    actual_values = {}
    with open(output_csv, "r") as f:
        reader = csv.DictReader(f)
        assert 'metric_id' in reader.fieldnames and 'baseline' in reader.fieldnames, "Output CSV missing required headers"
        for row in reader:
            actual_values[row['metric_id']] = float(row['baseline'])

    assert len(actual_values) == len(expected_values), "Output CSV row count does not match input CSV"

    for metric_id, expected_val in expected_values.items():
        assert metric_id in actual_values, f"Missing metric_id in output: {metric_id}"
        actual_val = actual_values[metric_id]
        assert math.isclose(actual_val, expected_val, rel_tol=1e-5), f"Incorrect baseline for {metric_id}. Expected ~{expected_val}, got {actual_val}"