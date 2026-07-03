# test_final_state.py

import os
import subprocess
import pytest

def compute_expected_sum():
    """Compute the expected sum of squares directly from the data files."""
    total = 0
    for i in range(1, 5):
        path = f'/home/user/app/data/region{i}.txt'
        if os.path.exists(path):
            with open(path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        val = int(line)
                        total += val * val
    return total

def test_aggregator_fixed_exists_and_executable():
    """Verify that the fixed C program is compiled and executable."""
    path = '/home/user/app/aggregator_fixed'
    assert os.path.isfile(path), f"Compiled executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_resolution_txt_correct():
    """Verify that resolution.txt contains the correct aggregate value."""
    path = '/home/user/app/resolution.txt'
    assert os.path.isfile(path), f"Resolution file {path} does not exist."

    expected_sum = compute_expected_sum()
    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == str(expected_sum), f"Expected {expected_sum} in {path}, but found '{content}'."

def test_aggregator_fixed_no_race_condition():
    """Verify that running aggregator_fixed consistently produces the correct result."""
    path = '/home/user/app/aggregator_fixed'
    assert os.path.isfile(path), f"Compiled executable {path} does not exist."

    expected_sum = compute_expected_sum()

    for i in range(50):
        result = subprocess.run([path], capture_output=True, text=True)
        assert result.returncode == 0, f"Execution failed on run {i+1} with error: {result.stderr}"
        output = result.stdout.strip()
        assert output == str(expected_sum), f"Race condition detected on run {i+1}: expected {expected_sum}, got {output}."