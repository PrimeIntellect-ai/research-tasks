# test_final_state.py

import os
import pytest
import math

def test_go_project_setup():
    """Test that the Go project files exist."""
    go_file = '/home/user/ml_pipeline/process.go'
    mod_file = '/home/user/ml_pipeline/go.mod'

    assert os.path.exists(go_file), f"Go source file {go_file} is missing."
    assert os.path.isfile(go_file), f"Path {go_file} is not a file."

    assert os.path.exists(mod_file), f"Go module file {mod_file} is missing."
    assert os.path.isfile(mod_file), f"Path {mod_file} is not a file."

    with open(mod_file, 'r') as f:
        mod_content = f.read()
    assert 'module ml_pipeline' in mod_content, "The go.mod file does not define the module 'ml_pipeline'."
    assert 'gonum.org/v1/gonum' in mod_content, "The go.mod file does not require 'gonum.org/v1/gonum'."

def test_svd_result():
    """Test that the SVD result file exists and contains the correct value."""
    result_file = '/home/user/svd_result.txt'

    assert os.path.exists(result_file), f"Result file {result_file} is missing."
    assert os.path.isfile(result_file), f"Path {result_file} is not a file."

    with open(result_file, 'r') as f:
        content = f.read().strip()

    assert content != "", f"Result file {result_file} is empty."

    try:
        actual_val = float(content)
    except ValueError:
        pytest.fail(f"Content of {result_file} is not a valid float: '{content}'")

    # The expected value calculated via Python is 183.0232
    expected_val = 183.0232
    assert math.isclose(actual_val, expected_val, rel_tol=1e-4, abs_tol=1e-3), \
        f"Expected SVD result to be close to {expected_val}, but got {actual_val}."

    # Check formatting (exactly 4 decimal places)
    if '.' in content:
        decimals = len(content.split('.')[1])
        assert decimals == 4, f"Expected exactly 4 decimal places, but found {decimals} in '{content}'."
    else:
        pytest.fail(f"Expected float with 4 decimal places, but got '{content}'.")