# test_final_state.py

import os
import pytest

def test_best_fc_exists_and_correct():
    """Check if /home/user/best_fc.txt exists and contains the correct value."""
    file_path = "/home/user/best_fc.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did the bash script run successfully?"

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "6", f"Expected the best cutoff frequency to be '6', but got '{content}'."

def test_scripts_exist():
    """Check if the required scripts were created."""
    compute_path = "/home/user/compute.py"
    optimize_path = "/home/user/optimize.sh"

    assert os.path.isfile(compute_path), f"Python script {compute_path} is missing."
    assert os.path.isfile(optimize_path), f"Bash script {optimize_path} is missing."