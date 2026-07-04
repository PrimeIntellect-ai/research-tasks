# test_final_state.py
import os
import csv
import math
import pytest

def test_venv_exists():
    """Verify that the virtual environment was created and contains a Python executable."""
    venv_python = "/home/user/env/bin/python"
    assert os.path.isfile(venv_python), f"Virtual environment Python executable missing at {venv_python}"

def test_script_exists():
    """Verify that the student's script exists."""
    script_path = "/home/user/augment.py"
    assert os.path.isfile(script_path), f"Script missing at {script_path}"

def test_output_plot_exists():
    """Verify that the trajectories plot was generated."""
    plot_path = "/home/user/output/trajectories.png"
    assert os.path.isfile(plot_path), f"Plot missing at {plot_path}"

def test_augmented_csv_exists():
    """Verify that the augmented CSV file exists."""
    csv_path = "/home/user/output/augmented_I.csv"
    assert os.path.isfile(csv_path), f"Augmented CSV missing at {csv_path}"

def test_augmented_csv_content():
    """Verify the structure and basic correctness of the augmented CSV."""
    csv_path = "/home/user/output/augmented_I.csv"

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The augmented CSV file is empty."

    header = rows[0]
    expected_header = ["t", "I_0", "I_1", "I_2", "I_3", "I_4"]
    assert header == expected_header, f"CSV header is incorrect. Expected {expected_header}, got {header}"

    data_rows = rows[1:]
    assert len(data_rows) == 51, f"Expected exactly 51 data rows for t in [0, 50], got {len(data_rows)}"

    for i, row in enumerate(data_rows):
        assert len(row) == 6, f"Row {i+1} has {len(row)} columns, expected 6."

        try:
            t_val = float(row[0])
            i_vals = [float(v) for v in row[1:]]
        except ValueError as e:
            pytest.fail(f"Could not parse numeric values in row {i+1}: {e}")

        # Time points should be exactly 0, 1, 2, ..., 50
        assert math.isclose(t_val, i, abs_tol=1e-5), f"Time point at row {i+1} is {t_val}, expected {i}."

        # At t=0, I should be exactly the initial condition (10)
        if i == 0:
            for j, i_val in enumerate(i_vals):
                assert math.isclose(i_val, 10.0, abs_tol=0.1), f"Initial condition I_{j} at t=0 should be 10.0, got {i_val}"