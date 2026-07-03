# test_final_state.py

import os
import pytest

def test_best_model_file_exists():
    """Verify that the best_model.txt file was created."""
    file_path = '/home/user/best_model.txt'
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

def test_best_model_content():
    """Verify that the best_model.txt contains the correct model filename."""
    file_path = '/home/user/best_model.txt'
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    expected = "model_gamma.pkl"
    assert content == expected, f"Expected '{expected}' in {file_path}, but found '{content}'."