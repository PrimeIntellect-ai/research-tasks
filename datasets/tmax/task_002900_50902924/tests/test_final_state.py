# test_final_state.py

import os
import pytest

def test_structural_weights_correct():
    actual_path = '/home/user/structural_weights.txt'
    expected_path = '/home/user/.expected_weights'

    assert os.path.exists(actual_path), f"File {actual_path} does not exist. The script did not create the required output file."
    assert os.path.isfile(actual_path), f"Path {actual_path} is not a file."

    with open(expected_path, 'r') as f:
        expected_content = f.read().strip()

    with open(actual_path, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, f"Contents of {actual_path} do not match the expected values. Expected: '{expected_content}', Got: '{actual_content}'"

def test_reconstruction_mse_correct():
    actual_path = '/home/user/reconstruction_mse.txt'
    expected_path = '/home/user/.expected_mse'

    assert os.path.exists(actual_path), f"File {actual_path} does not exist. The script did not create the required output file."
    assert os.path.isfile(actual_path), f"Path {actual_path} is not a file."

    with open(expected_path, 'r') as f:
        expected_content = f.read().strip()

    with open(actual_path, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, f"Contents of {actual_path} do not match the expected values. Expected: '{expected_content}', Got: '{actual_content}'"