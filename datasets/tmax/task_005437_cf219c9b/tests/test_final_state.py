# test_final_state.py

import os
import pytest

def test_n_components_file():
    path = '/home/user/n_components.txt'
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read().strip()

    assert content.isdigit(), f"Expected an integer in {path}, got '{content}'."
    assert content == '46', f"Expected k to be 46 for this dataset, but got {content}."

def test_pca_max_error_file():
    path = '/home/user/pca_max_error.txt'
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read().strip()

    try:
        error_val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the content of {path} as a float. Got: '{content}'")

    assert 'e' in content.lower(), f"Expected scientific notation in {path}, got '{content}'."
    assert error_val < 1e-12, f"Expected max reconstruction error to be less than 1e-12, got {error_val}."

def test_mse_file():
    path = '/home/user/mse.txt'
    assert os.path.exists(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read().strip()

    try:
        mse_val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the content of {path} as a float. Got: '{content}'")

    # Check if it's rounded to exactly 4 decimal places
    if '.' in content:
        decimals = content.split('.')[1]
        assert len(decimals) == 4, f"Expected MSE to be rounded to exactly 4 decimal places, got '{content}'."
    else:
        pytest.fail(f"Expected MSE to have 4 decimal places, got '{content}'.")

    # The expected MSE for this dataset is approximately 0.0097
    expected_mse = 0.0097
    tolerance = 0.01
    assert abs(mse_val - expected_mse) < tolerance, f"Expected MSE to be near {expected_mse}, but got {mse_val}."