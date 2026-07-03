# test_final_state.py

import os
import csv
import math

def test_c_source_file():
    """Check that root_finder.c exists and contains OpenMP parallel for."""
    c_file = "/home/user/root_finder.c"
    assert os.path.exists(c_file), f"{c_file} does not exist."

    with open(c_file, "r") as f:
        content = f.read()

    assert "#pragma omp parallel for" in content, "The C code must contain '#pragma omp parallel for' to parallelize the loop."

def test_bash_script():
    """Check that build_and_run.sh exists."""
    sh_file = "/home/user/build_and_run.sh"
    assert os.path.exists(sh_file), f"{sh_file} does not exist."

def test_csv_output():
    """Check that roots.csv exists and contains the correct values."""
    csv_file = "/home/user/roots.csv"
    assert os.path.exists(csv_file), f"{csv_file} does not exist. Did you run the bash script?"

    expected_values = [
        (0.1, 0.100335),
        (0.2, 0.202759),
        (0.3, 0.309653),
        (0.4, 0.423719),
        (0.5, 0.548455),
        (0.6, 0.688862),
        (0.7, 0.852579),
        (0.8, 1.053155),
    ]

    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == len(expected_values), f"Expected {len(expected_values)} rows in {csv_file}, but found {len(rows)}."

    for i, row in enumerate(rows):
        assert len(row) == 2, f"Row {i+1} does not have exactly 2 columns."
        c_val = float(row[0])
        x_val = float(row[1])

        expected_c, expected_x = expected_values[i]

        assert math.isclose(c_val, expected_c, abs_tol=1e-5), f"Row {i+1}: Expected C_i ≈ {expected_c}, got {c_val}."
        assert math.isclose(x_val, expected_x, abs_tol=1e-4), f"Row {i+1}: Expected x_i ≈ {expected_x}, got {x_val}."