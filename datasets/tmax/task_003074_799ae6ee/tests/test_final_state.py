# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/process_logs.sh"

    # Check if script exists
    assert os.path.isfile(script_path), f"Script file {script_path} does not exist."

    # Check if script is executable
    assert os.access(script_path, os.X_OK), f"Script file {script_path} is not executable."

def test_normalized_csv_exists_and_correct():
    csv_path = "/home/user/normalized.csv"

    # Check if output file exists
    assert os.path.isfile(csv_path), f"Output file {csv_path} does not exist."

    # Expected output content
    expected_content = """timestamp,level,message
1698832800,ERROR,Disk full
1698833100,WARN,CPU high
1698833400,INFO,Service up
1698913800,ERROR,Network timeout"""

    with open(csv_path, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"The contents of {csv_path} do not match the expected output."