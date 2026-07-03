# test_final_state.py

import os
import csv
import subprocess
import pytest

def test_profile_mc_exists():
    """Check if the Python profiling script was created."""
    file_path = "/home/user/profile_mc.py"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

def test_mc_results_csv():
    """Check the generated CSV file for correct lines and deterministic output."""
    file_path = "/home/user/mc_results.csv"
    assert os.path.exists(file_path), f"File {file_path} is missing. Did you run your Python script?"

    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 4, f"Expected exactly 4 lines in {file_path}, but found {len(rows)}."

    expected_Ns = [1000, 10000, 100000, 1000000]
    expected_errors = [
        0.013592653589793012,
        0.007607346410206803,
        0.005192653589792879,
        0.0007766535897929427
    ]

    for i, row in enumerate(rows):
        assert len(row) == 3, f"Row {i+1} does not have exactly 3 columns: {row}"

        n_val = int(row[0])
        assert n_val == expected_Ns[i], f"Row {i+1} expected N={expected_Ns[i]}, got N={n_val}"

        # We don't check execution time strictly, just that it's a float
        try:
            float(row[1])
        except ValueError:
            pytest.fail(f"Execution time in row {i+1} is not a valid float: {row[1]}")

        err_val = float(row[2])
        assert abs(err_val - expected_errors[i]) < 1e-5, \
            f"Row {i+1} expected absolute error ~{expected_errors[i]}, got {err_val}. Check if random.seed(42) was called exactly once before the loop."

def test_verify_sh_exists_and_executable():
    """Check if verify.sh exists and is executable."""
    file_path = "/home/user/verify.sh"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_verify_sh_execution():
    """Check the behavior of verify.sh."""
    file_path = "/home/user/verify.sh"

    # Run the script
    result = subprocess.run([file_path], capture_output=True, text=True)

    assert result.returncode == 0, f"{file_path} exited with status code {result.returncode}, expected 0."
    assert result.stdout.strip() == "Convergence OK", f"Expected output 'Convergence OK', got '{result.stdout.strip()}'."