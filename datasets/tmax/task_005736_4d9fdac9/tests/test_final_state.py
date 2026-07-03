# test_final_state.py

import os
import pytest

def test_optimal_c_file_exists():
    """Test that the output file optimal_c.txt exists."""
    file_path = '/home/user/optimal_c.txt'
    assert os.path.exists(file_path), f"Verification failed: {file_path} not found."
    assert os.path.isfile(file_path), f"Verification failed: {file_path} is not a file."

def test_optimal_c_value():
    """Test that the optimal drag coefficient is correct."""
    file_path = '/home/user/optimal_c.txt'
    assert os.path.exists(file_path), f"Verification failed: {file_path} not found."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == "0.45", f"Verification failed: Expected '0.45', got '{content}'"