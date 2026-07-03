# test_final_state.py

import os
import sys
import subprocess
import pytest

def test_fast_sim_exists_and_executable():
    """Check if fast_sim is compiled and executable."""
    fast_sim_path = "/home/user/ode/fast_sim"
    assert os.path.exists(fast_sim_path), f"Executable {fast_sim_path} does not exist."
    assert os.path.isfile(fast_sim_path), f"{fast_sim_path} is not a file."
    assert os.access(fast_sim_path, os.X_OK), f"{fast_sim_path} is not executable."

def test_regression_diff_correct():
    """Check if regression_diff.txt exists and contains a value close to 0."""
    diff_file = "/home/user/ode/regression_diff.txt"
    assert os.path.exists(diff_file), f"File {diff_file} does not exist."

    with open(diff_file, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {diff_file} is not a valid float: '{content}'")

    assert val < 1e-4, f"The maximum absolute difference {val} in {diff_file} is too large or incorrect."
    assert val >= 0.0, f"The maximum absolute difference {val} cannot be negative."

def test_train_data_csv_matches_expected():
    """Check if train_data.csv matches the expected output for the given parameters."""
    train_data_path = "/home/user/ode/train_data.csv"
    assert os.path.exists(train_data_path), f"File {train_data_path} does not exist."

    # Compile the C code to a temporary executable to get the expected output
    simulator_c_path = "/home/user/ode/simulator.c"
    expected_exe_path = "/tmp/fast_sim_expected"

    compile_cmd = ["gcc", "-O3", "-lm", simulator_c_path, "-o", expected_exe_path]
    compile_res = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert compile_res.returncode == 0, f"Failed to compile {simulator_c_path} for verification."

    # Run the expected executable to generate expected CSV output
    run_cmd = [expected_exe_path, "1.0", "5.0", "0.1", "20.0", "0.01"]
    run_res = subprocess.run(run_cmd, capture_output=True, text=True)
    assert run_res.returncode == 0, "Failed to run the expected executable."

    expected_output = run_res.stdout.strip()

    # Read the actual train_data.csv
    with open(train_data_path, 'r') as f:
        actual_output = f.read().strip()

    # Compare line by line to provide better error messages
    expected_lines = expected_output.splitlines()
    actual_lines = actual_output.splitlines()

    assert len(actual_lines) == len(expected_lines), (
        f"Line count mismatch in {train_data_path}. "
        f"Expected {len(expected_lines)} lines, got {len(actual_lines)} lines."
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, (
            f"Mismatch at line {i + 1} in {train_data_path}.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )