# test_final_state.py
import os
import json
import csv
import math
import pytest

def test_run_pipeline_exists_and_executable():
    path = "/home/user/run_pipeline.sh"
    assert os.path.exists(path), f"{path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_cleaned_dataset_csv():
    path = "/home/user/cleaned_dataset.csv"
    assert os.path.exists(path), f"{path} does not exist."

    raw_path = "/home/user/raw_observations.txt"
    assert os.path.exists(raw_path), f"Original {raw_path} is missing."

    s1, s2 = {}, {}
    with open(raw_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) == 3:
                s, x, y = parts[0], float(parts[1]), float(parts[2])
                if s == 'S1': s1[x] = y
                elif s == 'S2': s2[x] = y

    x_sorted = sorted(list(s1.keys()))

    with open(path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert len(header) >= 3, "CSV header should have at least 3 columns"

        rows = list(reader)
        assert len(rows) == len(x_sorted), f"Expected {len(x_sorted)} rows in CSV, found {len(rows)}"

        for idx, row in enumerate(rows):
            x_val = float(row[0])
            y1_val = float(row[1])
            y2_val = float(row[2])

            expected_x = x_sorted[idx]
            assert math.isclose(x_val, expected_x, rel_tol=1e-4), f"Row {idx+1}: x expected {expected_x}, got {x_val}"
            assert math.isclose(y1_val, s1[expected_x], rel_tol=1e-4), f"Row {idx+1}: y1 expected {s1[expected_x]}, got {y1_val}"
            assert math.isclose(y2_val, s2[expected_x], rel_tol=1e-4), f"Row {idx+1}: y2 expected {s2[expected_x]}, got {y2_val}"

def test_results_json():
    path = "/home/user/results.json"
    assert os.path.exists(path), f"{path} does not exist."

    with open(path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} is not valid JSON.")

    assert "p_value" in results, "Missing 'p_value' in results.json"
    assert "m_mean" in results, "Missing 'm_mean' in results.json"
    assert "c_mean" in results, "Missing 'c_mean' in results.json"

    # Since we cannot use scipy/emcee in the test environment, we verify against the expected 
    # ranges for the fixed seed data.
    p_val = results["p_value"]
    m_mean = results["m_mean"]
    c_mean = results["c_mean"]

    assert 0.04 < p_val < 0.05, f"p_value {p_val} is not close to expected ~0.046"
    assert 2.4 < m_mean < 2.6, f"m_mean {m_mean} is not close to expected ~2.5"
    assert 1.1 < c_mean < 1.4, f"c_mean {c_mean} is not close to expected ~1.2"