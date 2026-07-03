# test_final_state.py

import os
import pytest

def test_prob_file():
    """Test that prob.txt contains the correct probability."""
    file_path = "/home/user/prob.txt"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "0.8710", f"Expected prob.txt to contain '0.8710', but got '{content}'."

def test_decision_file():
    """Test that decision.txt contains the correct decision."""
    file_path = "/home/user/decision.txt"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content == "RETAIN", f"Expected decision.txt to contain 'RETAIN', but got '{content}'."