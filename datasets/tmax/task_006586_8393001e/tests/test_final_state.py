# test_final_state.py

import os
import pytest

def test_optimal_k_file():
    path = "/home/user/optimal_k.txt"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

    with open(path, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {path} is not a valid number: '{content}'")

    assert val == 2.0, f"Expected optimal k to be 2.00, but got {val}"

def test_best_model_file():
    best_model_path = "/home/user/best_model.txt"
    golden_path = "/home/user/golden.txt"

    assert os.path.exists(best_model_path), f"File {best_model_path} does not exist."
    assert os.path.isfile(best_model_path), f"Path {best_model_path} is not a file."

    with open(best_model_path, 'r') as f:
        best_content = f.read().strip()

    with open(golden_path, 'r') as f:
        golden_content = f.read().strip()

    assert best_content == golden_content, f"Content of {best_model_path} does not match {golden_path}."

def test_regression_patch_file():
    patch_path = "/home/user/regression.patch"

    assert os.path.exists(patch_path), f"File {patch_path} does not exist."
    assert os.path.isfile(patch_path), f"Path {patch_path} is not a file."

    with open(patch_path, 'r') as f:
        content = f.read()

    assert content == "", f"Expected {patch_path} to be empty, but it contains data. This indicates differences were found or the command was incorrect."