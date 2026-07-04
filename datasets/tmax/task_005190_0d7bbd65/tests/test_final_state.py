# test_final_state.py

import os
import subprocess

def test_deliverable_files_exist():
    """Check that the required source and build files exist."""
    assert os.path.isfile('/home/user/process_sensors.c'), "process_sensors.c is missing."
    assert os.path.isfile('/home/user/Makefile'), "Makefile is missing."
    assert os.path.isfile('/home/user/run.sh'), "run.sh is missing."

def test_compilation_and_execution():
    """Run the bash script to compile and execute the C program, then verify the output."""
    # Execute the run.sh script
    result = subprocess.run(
        ['bash', '/home/user/run.sh'],
        cwd='/home/user',
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"run.sh failed to execute properly. Stderr: {result.stderr}"

    summary_path = '/home/user/summary.csv'
    expected_path = '/home/user/expected_summary.csv'

    assert os.path.isfile(summary_path), f"Output file {summary_path} was not created."
    assert os.path.isfile(expected_path), f"Expected summary file {expected_path} is missing."

    with open(summary_path, 'r') as f:
        actual_lines = [line.strip() for line in f.read().strip().splitlines() if line.strip()]

    with open(expected_path, 'r') as f:
        expected_lines = [line.strip() for line in f.read().strip().splitlines() if line.strip()]

    assert len(actual_lines) == 2, f"summary.csv must contain exactly 2 lines, but found {len(actual_lines)}."

    # Check header
    assert actual_lines[0] == expected_lines[0], f"Header mismatch. Expected '{expected_lines[0]}', got '{actual_lines[0]}'."

    # Check values
    actual_vals = actual_lines[1].split(',')
    expected_vals = expected_lines[1].split(',')

    assert len(actual_vals) == 5, f"Data row must contain exactly 5 columns, but found {len(actual_vals)}."

    # Compare valid_rows exactly
    assert actual_vals[0] == expected_vals[0], f"valid_rows mismatch. Expected {expected_vals[0]}, got {actual_vals[0]}."

    # Compare float values with a small tolerance for floating point differences
    columns = ["sensor1_mean", "sensor1_sd", "sensor2_mean", "sensor3_mean"]
    for i, col_name in enumerate(columns, start=1):
        try:
            actual_float = float(actual_vals[i])
            expected_float = float(expected_vals[i])
        except ValueError:
            pytest.fail(f"Could not parse float value for {col_name}. Got: '{actual_vals[i]}'")

        diff = abs(actual_float - expected_float)
        assert diff <= 0.001, f"{col_name} mismatch. Expected {expected_float:.4f}, got {actual_float:.4f}."