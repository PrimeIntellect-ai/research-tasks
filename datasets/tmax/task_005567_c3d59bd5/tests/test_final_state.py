# test_final_state.py

import os
import json
import csv
import math
import pytest

PARAMS_FILE = "/home/user/fitted_params.json"
CSV_FILE = "/home/user/pinn_training.csv"

def test_fitted_params():
    """Verify that fitted_params.json exists, is valid, and contains correct parameters."""
    assert os.path.isfile(PARAMS_FILE), f"File {PARAMS_FILE} is missing."

    with open(PARAMS_FILE, "r") as f:
        try:
            params = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {PARAMS_FILE} is not valid JSON.")

    assert "A" in params, "Key 'A' is missing from fitted_params.json."
    assert "k" in params, "Key 'k' is missing from fitted_params.json."

    A_fit = params["A"]
    k_fit = params["k"]

    assert isinstance(A_fit, (int, float)), f"'A' must be a number, got {type(A_fit)}."
    assert isinstance(k_fit, (int, float)), f"'k' must be a number, got {type(k_fit)}."

    assert abs(A_fit - 5.0) < 0.2, f"Fitted parameter A ({A_fit}) is too far from expected 5.0."
    assert abs(k_fit - 0.5) < 0.05, f"Fitted parameter k ({k_fit}) is too far from expected 0.5."

def test_csv_structure_and_grid():
    """Verify the CSV file exists, has the correct columns, row count, and grid sorting."""
    assert os.path.isfile(CSV_FILE), f"File {CSV_FILE} is missing."

    with open(CSV_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            pytest.fail(f"{CSV_FILE} is empty.")

        expected_headers = ["t", "x", "T", "T_t", "T_xx"]
        assert headers == expected_headers, f"CSV headers are incorrect. Expected {expected_headers}, got {headers}."

        rows = list(reader)

    assert len(rows) == 2500, f"Expected exactly 2500 rows of data, got {len(rows)}."

    # Check grid values and sorting
    t_values = []
    x_values = []

    for i, row in enumerate(rows):
        assert len(row) == 5, f"Row {i+1} does not have exactly 5 columns."
        try:
            t = float(row[0])
            x = float(row[1])
        except ValueError:
            pytest.fail(f"Non-numeric grid value in row {i+1}: {row}")

        t_values.append(t)
        x_values.append(x)

    # Verify sorting: primarily by t, secondarily by x
    for i in range(1, len(rows)):
        if t_values[i] < t_values[i-1]:
            pytest.fail(f"Data is not sorted primarily by 't' in ascending order at row {i+1}.")
        if t_values[i] == t_values[i-1] and x_values[i] < x_values[i-1]:
            pytest.fail(f"Data is not sorted secondarily by 'x' in ascending order at row {i+1}.")

    # Verify grid bounds
    assert min(t_values) == 0.0, f"Minimum 't' should be 0.0, got {min(t_values)}"
    assert max(t_values) == 2.0, f"Maximum 't' should be 2.0, got {max(t_values)}"
    assert min(x_values) == 0.0, f"Minimum 'x' should be 0.0, got {min(x_values)}"
    assert max(x_values) == 1.0, f"Maximum 'x' should be 1.0, got {max(x_values)}"

def test_csv_values_and_derivatives():
    """Verify that the values in the CSV are computed correctly using the fitted parameters and rounded to 4 decimals."""
    assert os.path.isfile(PARAMS_FILE), f"File {PARAMS_FILE} is missing."
    with open(PARAMS_FILE, "r") as f:
        params = json.load(f)
    A_fit = params["A"]
    k_fit = params["k"]

    with open(CSV_FILE, "r", newline="") as f:
        reader = csv.reader(f)
        next(reader) # skip headers
        rows = list(reader)

    for i, row in enumerate(rows):
        t_str, x_str, T_str, Tt_str, Txx_str = row

        # Check decimal places (at most 4 decimal places)
        for col_name, val_str in zip(["T", "T_t", "T_xx"], [T_str, Tt_str, Txx_str]):
            if "." in val_str:
                decimals = len(val_str.split(".")[1])
                assert decimals <= 4, f"Value {val_str} for {col_name} in row {i+1} is not rounded to 4 decimal places."

        t = float(t_str)
        x = float(x_str)
        T_val = float(T_str)
        Tt_val = float(Tt_str)
        Txx_val = float(Txx_str)

        # Compute expected values using the student's fitted parameters
        exp_T = A_fit * math.exp(-k_fit * t) * math.sin(math.pi * x)
        exp_Tt = -k_fit * A_fit * math.exp(-k_fit * t) * math.sin(math.pi * x)
        exp_Txx = -(math.pi**2) * A_fit * math.exp(-k_fit * t) * math.sin(math.pi * x)

        # Round expected to 4 decimal places
        exp_T_rounded = round(exp_T, 4)
        exp_Tt_rounded = round(exp_Tt, 4)
        exp_Txx_rounded = round(exp_Txx, 4)

        assert math.isclose(T_val, exp_T_rounded, abs_tol=1e-4), \
            f"Row {i+1}: T mismatch. Got {T_val}, expected {exp_T_rounded}"
        assert math.isclose(Tt_val, exp_Tt_rounded, abs_tol=1e-4), \
            f"Row {i+1}: T_t mismatch. Got {Tt_val}, expected {exp_Tt_rounded}"
        assert math.isclose(Txx_val, exp_Txx_rounded, abs_tol=1e-4), \
            f"Row {i+1}: T_xx mismatch. Got {Txx_val}, expected {exp_Txx_rounded}"