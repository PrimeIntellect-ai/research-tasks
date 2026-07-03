# test_final_state.py

import os
import pytest

def test_rank_file_exists_and_correct():
    """Test that rank.txt exists and contains the correct rank (15)."""
    rank_path = "/home/user/rank.txt"
    assert os.path.exists(rank_path), f"File not found: {rank_path}"
    assert os.path.isfile(rank_path), f"Path is not a file: {rank_path}"

    with open(rank_path, 'r') as f:
        content = f.read().strip()

    assert content == "15", f"Incorrect rank. Expected '15', got '{content}'"

def test_mse_file_exists_and_small():
    """Test that mse.txt exists and contains a very small floating point number."""
    mse_path = "/home/user/mse.txt"
    assert os.path.exists(mse_path), f"File not found: {mse_path}"
    assert os.path.isfile(mse_path), f"Path is not a file: {mse_path}"

    with open(mse_path, 'r') as f:
        content = f.read().strip()

    try:
        mse_value = float(content)
    except ValueError:
        pytest.fail(f"Content of mse.txt is not a valid float: '{content}'")

    assert mse_value < 1e-20, f"MSE is too large: {mse_value}. Expected a value < 1e-20."
    assert mse_value >= 0.0, f"MSE cannot be negative: {mse_value}."