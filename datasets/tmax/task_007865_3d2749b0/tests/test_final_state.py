# test_final_state.py

import os
import math
import csv
import stat
import pytest

def test_files_exist():
    """Check that the required files exist."""
    assert os.path.isfile("/home/user/generate_data.cpp"), "generate_data.cpp is missing."
    assert os.path.isfile("/home/user/run_pipeline.sh"), "run_pipeline.sh is missing."
    assert os.path.isfile("/home/user/training_data.csv"), "training_data.csv is missing."

def test_script_executable():
    """Check that run_pipeline.sh is executable."""
    st = os.stat("/home/user/run_pipeline.sh")
    assert bool(st.st_mode & stat.S_IXUSR), "run_pipeline.sh is not executable."

def test_csv_contents():
    """Validate the contents of training_data.csv."""
    csv_path = "/home/user/training_data.csv"

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV is empty."
    assert rows[0] == ['x', 'u'], f"CSV header is incorrect, got {rows[0]}"

    data_rows = rows[1:]
    assert len(data_rows) == 101, f"CSV must have exactly 101 data rows, got {len(data_rows)}"

    x_vals = []
    u_vals = []

    for i, row in enumerate(data_rows):
        assert len(row) == 2, f"Row {i+1} does not have exactly 2 columns."
        try:
            x_val = float(row[0])
            u_val = float(row[1])
        except ValueError:
            pytest.fail(f"Could not parse row {i+1} as floats: {row}")

        x_vals.append(x_val)
        u_vals.append(u_val)

        # Check formatting (6 decimal places)
        # We can check if there's a decimal point and up to 6 digits after it, 
        # but standard float formatting might drop trailing zeros. 
        # The prompt says "formatted to 6 decimal places", so let's check if the string has at most 6 decimal places 
        # or exactly 6 if they used fixed formatting.
        if '.' in row[0]:
            assert len(row[0].split('.')[1]) <= 6, f"x value {row[0]} has more than 6 decimal places."
        if '.' in row[1]:
            assert len(row[1].split('.')[1]) <= 6, f"u value {row[1]} has more than 6 decimal places."

    # Check boundaries
    assert math.isclose(x_vals[0], 0.0, abs_tol=1e-5), f"x[0] != 0.0, got {x_vals[0]}"
    assert math.isclose(u_vals[0], 0.0, abs_tol=1e-5), f"u[0] != 0.0, got {u_vals[0]}"
    assert math.isclose(x_vals[-1], 1.0, abs_tol=1e-5), f"x[-1] != 1.0, got {x_vals[-1]}"
    assert math.isclose(u_vals[-1], 0.0, abs_tol=1e-5), f"u[-1] != 0.0, got {u_vals[-1]}"

    # Check midpoint
    u_mid = u_vals[50]
    assert 1.08 < u_mid < 1.09, f"Midpoint value u(0.5)={u_mid} is out of expected range [1.08, 1.09]"

    # Check discrete equation residual
    h = 0.01
    for i in range(1, 100):
        # - (u_{i+1} - 2u_i + u_{i-1}) / h^2 + exp(u_i) = 10
        second_deriv = (u_vals[i+1] - 2*u_vals[i] + u_vals[i-1]) / (h**2)
        residual = -second_deriv + math.exp(u_vals[i]) - 10
        assert abs(residual) < 1e-3, f"Discrete residual at index {i} (x={x_vals[i]}) is too large: {residual}"