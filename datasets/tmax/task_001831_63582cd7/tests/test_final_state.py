# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/analyze_artifacts.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist. The task requires creating this script."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable. Make sure to run 'chmod +x'."

def test_output_file_exists():
    output_path = "/home/user/closest.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist. The script must generate this file."

def test_output_content():
    output_path = "/home/user/closest.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."
    with open(output_path, "r") as f:
        content = f.read()

    actual_id = content.strip()
    expected_id = "exp_alpha"
    assert actual_id == expected_id, f"Expected output to be '{expected_id}', but got '{actual_id}'. Check your filtering and distance calculation logic."