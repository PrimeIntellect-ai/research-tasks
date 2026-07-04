# test_final_state.py

import os
import csv
import json
import math
import pytest

def test_integration_report_json():
    report_path = "/home/user/integration_report.json"
    assert os.path.isfile(report_path), f"Missing required output file: {report_path}"

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    expected_keys = {"euler_mse_v", "euler_mse_p", "trapz_mse_v", "trapz_mse_p", "best_method"}
    assert expected_keys.issubset(data.keys()), f"Missing keys in {report_path}. Expected {expected_keys}, found {set(data.keys())}"

    assert data["best_method"] == "trapz", f"Expected best_method to be 'trapz', got {data['best_method']}"

    assert data["trapz_mse_v"] < data["euler_mse_v"], "Trapezoidal MSE for velocity should be less than Euler MSE."
    assert data["trapz_mse_p"] < data["euler_mse_p"], "Trapezoidal MSE for position should be less than Euler MSE."

def test_training_data_csv():
    data_path = "/home/user/training_data.csv"
    assert os.path.isfile(data_path), f"Missing required output file: {data_path}"

    with open(data_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['t', 'a', 'v', 'p'], f"Incorrect header in {data_path}. Expected ['t', 'a', 'v', 'p'], got {header}"

        rows = list(reader)
        assert len(rows) == 101, f"Expected 101 data rows in {data_path}, got {len(rows)}"

        # Check last row t=10.0
        last_row = rows[-1]
        t_val = float(last_row[0])
        a_val = float(last_row[1])
        v_val = float(last_row[2])
        p_val = float(last_row[3])

        assert math.isclose(t_val, 10.0, abs_tol=1e-3), f"Expected last row t=10.0, got {t_val}"

        # Check precision (4 decimal places)
        for val_str in last_row:
            if '.' in val_str:
                decimals = len(val_str.split('.')[1])
                assert decimals <= 4, f"Values should be rounded to 4 decimal places, found {val_str}"

        # Approximate values for Trapezoidal integration at t=10.0
        # a = sin(10) ~ -0.5440
        # v ~ 1 - cos(10) ~ 1.8391
        # p ~ 10 - sin(10) ~ 10.5440
        expected_a = math.sin(10.0)
        expected_v = 1.0 - math.cos(10.0)
        expected_p = 10.0 - math.sin(10.0)

        assert math.isclose(a_val, expected_a, abs_tol=0.1), f"Acceleration at t=10.0 incorrect: {a_val}"
        assert math.isclose(v_val, expected_v, abs_tol=0.1), f"Velocity at t=10.0 incorrect: {v_val}"
        assert math.isclose(p_val, expected_p, abs_tol=0.1), f"Position at t=10.0 incorrect: {p_val}"