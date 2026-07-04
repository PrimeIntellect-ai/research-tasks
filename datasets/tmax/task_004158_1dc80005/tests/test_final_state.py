# test_final_state.py

import os
import pytest

def test_executable_compiled():
    """Test that matrix_sim was compiled and is executable."""
    exe_path = "/home/user/matrix_sim"
    assert os.path.isfile(exe_path), f"The compiled executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"The file {exe_path} is not executable."

def test_profile_script_exists_and_executable():
    """Test that profile.sh exists and is executable."""
    script_path = "/home/user/profile.sh"
    assert os.path.isfile(script_path), f"The bash script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_results_csv_content():
    """Test that results.csv has the correct format and data."""
    csv_path = "/home/user/results.csv"
    assert os.path.isfile(csv_path), f"The results file {csv_path} is missing."

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 91, f"Expected 91 lines in {csv_path}, found {len(lines)}."

    # Check specific lines
    assert lines[0] == "0.010,SUCCESS", f"Expected first line to be '0.010,SUCCESS', found '{lines[0]}'."

    # Calculate the expected index for 0.076
    # 0.010 is index 0, so 0.076 is index 66
    assert lines[66] == "0.076,SUCCESS", f"Expected line for dt=0.076 to be '0.076,SUCCESS', found '{lines[66]}'."
    assert lines[67] == "0.077,DIVERGED", f"Expected line for dt=0.077 to be '0.077,DIVERGED', found '{lines[67]}'."
    assert lines[-1] == "0.100,DIVERGED", f"Expected last line to be '0.100,DIVERGED', found '{lines[-1]}'."

def test_optimal_dt_content():
    """Test that optimal_dt.txt contains the correct value."""
    txt_path = "/home/user/optimal_dt.txt"
    assert os.path.isfile(txt_path), f"The file {txt_path} is missing."

    with open(txt_path, "r") as f:
        content = f.read().strip()

    assert content == "0.076", f"Expected optimal_dt.txt to contain '0.076', found '{content}'."