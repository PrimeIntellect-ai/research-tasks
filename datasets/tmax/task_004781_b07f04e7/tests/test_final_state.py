# test_final_state.py
import os
import csv
import pytest

def test_generate_report_executable_exists():
    path = "/home/user/generate_report"
    assert os.path.isfile(path), f"Executable missing at {path}"
    assert os.access(path, os.X_OK), f"File at {path} is not executable"

def test_revenue_report_csv_correctness():
    path = "/home/user/revenue_report.csv"
    assert os.path.isfile(path), f"CSV report missing at {path}"

    expected = {
        "Clothing": 330,
        "Electronics": 2400
    }

    try:
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            actual = {row['category']: int(row['total_revenue']) for row in reader}
    except Exception as e:
        pytest.fail(f"Failed to read or parse {path}: {e}")

    mse = 0
    for cat, exp_val in expected.items():
        act_val = actual.get(cat, 0)
        mse += (exp_val - act_val) ** 2

    mse /= len(expected)

    assert mse <= 0.0, f"MSE of total_revenue is {mse}, expected <= 0.0. Actual values: {actual}"