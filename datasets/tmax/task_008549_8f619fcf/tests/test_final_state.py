# test_final_state.py

import os
import pytest

def test_analyze_script_exists():
    """Check if the user created the analyze.py script."""
    file_path = "/home/user/analyze.py"
    assert os.path.isfile(file_path), f"Missing script: {file_path}"

def test_best_model_idx_exists():
    """Check if the output file best_model_idx.txt exists."""
    file_path = "/home/user/best_model_idx.txt"
    assert os.path.isfile(file_path), f"Missing output file: {file_path}"

def test_best_model_idx_content():
    """Check if the output file contains the correct model index."""
    file_path = "/home/user/best_model_idx.txt"
    assert os.path.isfile(file_path), f"Missing output file: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == "1337", f"Expected best model index to be '1337', but got '{content}'"