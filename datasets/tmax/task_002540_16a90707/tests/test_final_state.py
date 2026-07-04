# test_final_state.py

import os
import re
import pytest

def test_evaluator_c_exists():
    """Verify that the evaluator.c source file exists."""
    file_path = "/home/user/mlops/evaluator.c"
    assert os.path.isfile(file_path), f"Expected source file {file_path} does not exist."

def test_report_csv_exists():
    """Verify that the report.csv file was generated."""
    file_path = "/home/user/mlops/report.csv"
    assert os.path.isfile(file_path), f"Expected output file {file_path} does not exist."

def test_report_csv_content_and_format():
    """Verify the content and formatting of report.csv."""
    file_path = "/home/user/mlops/report.csv"
    if not os.path.exists(file_path):
        pytest.fail(f"{file_path} is missing.")

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in report.csv, but got {len(lines)}."

    expected_ns = ["100", "200", "300"]

    # Regex patterns for exact formatting requirements
    # MAE to 6 decimal places (e.g., 0.000000)
    mae_pattern = re.compile(r"^\d+\.\d{6}$")
    # Time to 1 decimal place (e.g., 1450.5)
    time_pattern = re.compile(r"^\d+\.\d{1}$")

    for i, line in enumerate(lines):
        parts = line.split(",")
        assert len(parts) == 3, f"Line {i+1} does not have exactly 3 columns: '{line}'"

        n_val, mae_str, time_str = parts

        assert n_val == expected_ns[i], f"Expected N={expected_ns[i]} on line {i+1}, got {n_val}."

        # Check formatting
        assert mae_pattern.match(mae_str), \
            f"MAE on line {i+1} is not formatted to 6 decimal places: '{mae_str}'"
        assert time_pattern.match(time_str), \
            f"Time on line {i+1} is not formatted to 1 decimal place: '{time_str}'"

        # Check numerical constraints
        try:
            mae_val = float(mae_str)
            time_val = float(time_str)
        except ValueError:
            pytest.fail(f"Non-numeric values found in line {i+1}: '{line}'")

        assert mae_val <= 1e-4, f"MAE on line {i+1} is too high: {mae_val}"
        assert time_val > 0, f"Time on line {i+1} must be positive, got: {time_val}"