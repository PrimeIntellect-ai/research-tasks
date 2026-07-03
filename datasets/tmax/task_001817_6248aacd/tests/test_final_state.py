# test_final_state.py

import os
import stat
import pytest

def test_heat_sim_c_exists():
    """Test that the C source file exists."""
    path = "/home/user/heat_sim.c"
    assert os.path.exists(path), f"Missing file: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"

def test_heat_sim_executable_exists():
    """Test that the compiled executable exists and is executable."""
    path = "/home/user/heat_sim"
    assert os.path.exists(path), f"Missing compiled executable: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_evaluate_sh_exists():
    """Test that the evaluate.sh script exists and is executable."""
    path = "/home/user/evaluate.sh"
    assert os.path.exists(path), f"Missing script: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"
    assert os.access(path, os.X_OK), f"Script is not executable: {path}"

def test_temp_dist_txt_contents():
    """Test that the temp_dist.txt matches the expected distribution."""
    path = "/home/user/temp_dist.txt"
    assert os.path.exists(path), f"Missing file: {path}"

    expected_content = (
        "Bin 0: 2164\n"
        "Bin 1: 104\n"
        "Bin 2: 60\n"
        "Bin 3: 40\n"
        "Bin 4: 36\n"
        "Bin 5: 32\n"
        "Bin 6: 28\n"
        "Bin 7: 24\n"
        "Bin 8: 12\n"
        "Bin 9: 0"
    )

    with open(path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, f"Contents of {path} do not match the expected distribution."

def test_error_metric_txt_contents():
    """Test that error_metric.txt contains exactly 0."""
    path = "/home/user/error_metric.txt"
    assert os.path.exists(path), f"Missing file: {path}"

    with open(path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == "0", f"Expected error_metric.txt to contain '0', but got '{actual_content}'"