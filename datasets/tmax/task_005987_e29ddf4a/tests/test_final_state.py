# test_final_state.py

import os
import pytest

def test_zero_variance_cols():
    """Test that zero_variance_cols.txt contains the correct zero variance columns."""
    file_path = '/home/user/zero_variance_cols.txt'
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == "5,6", f"Expected '5,6' in {file_path}, but got '{content}'."

def test_correlation():
    """Test that correlation.txt contains the correct Pearson correlation coefficient."""
    file_path = '/home/user/correlation.txt'
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == "0.999", f"Expected '0.999' in {file_path}, but got '{content}'."

def test_ci():
    """Test that ci.txt contains the correct mean and confidence interval."""
    file_path = '/home/user/ci.txt'
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == "131.875,114.607,149.143", f"Expected '131.875,114.607,149.143' in {file_path}, but got '{content}'."

def test_script_exists():
    """Test that the analyze.sh script was created."""
    file_path = '/home/user/analyze.sh'
    assert os.path.isfile(file_path), f"Script {file_path} is missing."