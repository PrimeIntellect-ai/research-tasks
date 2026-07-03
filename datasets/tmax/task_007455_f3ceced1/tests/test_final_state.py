# test_final_state.py

import os
import pytest
import math

def test_optimal_params_file_exists():
    file_path = '/home/user/kinetics/optimal_params.txt'
    assert os.path.isfile(file_path), f"File {file_path} does not exist. The script must save the optimal parameters to this file."

def test_optimal_params_content_format():
    file_path = '/home/user/kinetics/optimal_params.txt'
    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content, f"File {file_path} is empty."

    parts = content.split(',')
    assert len(parts) == 2, f"File {file_path} must contain exactly two values separated by a comma. Found: '{content}'"

    # Check if they are rounded to two decimal places
    for part in parts:
        part = part.strip()
        assert '.' in part, f"Value '{part}' does not have a decimal point."
        decimals = part.split('.')[1]
        assert len(decimals) == 2, f"Value '{part}' is not rounded to exactly two decimal places."

def test_optimal_params_values():
    file_path = '/home/user/kinetics/optimal_params.txt'
    with open(file_path, 'r') as f:
        content = f.read().strip()

    parts = content.split(',')
    try:
        k1 = float(parts[0].strip())
        k2 = float(parts[1].strip())
    except ValueError:
        pytest.fail(f"Could not parse parameters as floats: '{content}'")

    expected_k1 = 2.00
    expected_k2 = 0.50

    # Allow a small tolerance due to numerical integration and optimization variations
    assert math.isclose(k1, expected_k1, abs_tol=0.1), f"k1 value {k1} is not close enough to expected {expected_k1}."
    assert math.isclose(k2, expected_k2, abs_tol=0.1), f"k2 value {k2} is not close enough to expected {expected_k2}."