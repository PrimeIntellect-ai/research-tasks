# test_final_state.py

import os
import subprocess
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/run_and_profile.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_run_script_and_check_outputs():
    script_path = "/home/user/run_and_profile.sh"

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute properly. Output: {result.stderr}"

    # Check input.txt
    input_txt_path = "/home/user/input.txt"
    assert os.path.isfile(input_txt_path), f"File {input_txt_path} does not exist."
    with open(input_txt_path, "r") as f:
        input_content = f.read().strip()
    expected_input = "1.0 4.0 7.0 2.0 5.0 8.0 3.0 6.0 9.0"
    # Allow for multiple spaces
    normalized_input = " ".join(input_content.split())
    assert normalized_input == expected_input, f"Expected input.txt to be '{expected_input}', got '{normalized_input}'."

    # Check profile.txt
    profile_txt_path = "/home/user/profile.txt"
    assert os.path.isfile(profile_txt_path), f"File {profile_txt_path} does not exist."
    with open(profile_txt_path, "r") as f:
        profile_content = f.read()
    assert "tottime" in profile_content, "profile.txt does not appear to contain cProfile output sorted by tottime."
    assert "solve_pde" in profile_content, "profile.txt does not contain expected function names."

    # Check bottleneck.txt
    bottleneck_txt_path = "/home/user/bottleneck.txt"
    assert os.path.isfile(bottleneck_txt_path), f"File {bottleneck_txt_path} does not exist."
    with open(bottleneck_txt_path, "r") as f:
        bottleneck_content = f.read().strip()
    assert bottleneck_content == "app.py:4(solve_pde)", f"Expected bottleneck.txt to contain 'app.py:4(solve_pde)', got '{bottleneck_content}'."