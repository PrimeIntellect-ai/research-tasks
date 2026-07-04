# test_final_state.py

import os
import subprocess
import hashlib
import pytest

def test_process_script_exists_and_executable():
    script_path = "/home/user/process.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_process_script_output():
    script_path = "/home/user/process.sh"
    input_path = "/home/user/raw_sensors.csv"
    output_path = "/home/user/alerts.csv"

    # Ensure input exists
    assert os.path.isfile(input_path), f"Input file {input_path} is missing."

    # Run the script to generate the output
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}\nStderr: {result.stderr}"

    assert os.path.isfile(output_path), f"Output file {output_path} was not created."

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Expected logic:
    # A100 -> 376c12fb
    # C300 -> d83b631e
    # D400 -> fd32d94a

    expected_lines = [
        "376c12fb,US-EAST,t2,55.1,CRITICAL",
        "d83b631e,EU-WEST,t1,80.1,CRITICAL",
        "fd32d94a,US-WEST,t1,60.0,CRITICAL"
    ]

    actual_sorted = sorted(lines)
    expected_sorted = sorted(expected_lines)

    assert actual_sorted == expected_sorted, (
        f"Output in {output_path} does not match expected results.\n"
        f"Expected: {expected_sorted}\n"
        f"Got: {actual_sorted}"
    )