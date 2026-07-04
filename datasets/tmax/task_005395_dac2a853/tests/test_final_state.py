# test_final_state.py

import os
import pytest

def test_fit_mixture_script_exists():
    filepath = "/home/user/fit_mixture.py"
    assert os.path.isfile(filepath), f"Missing script file: {filepath}"

def test_optimal_weight_file_exists():
    filepath = "/home/user/optimal_weight.txt"
    assert os.path.isfile(filepath), f"Missing output file: {filepath}"

def test_optimal_weight_content():
    filepath = "/home/user/optimal_weight.txt"
    assert os.path.isfile(filepath), f"Missing output file: {filepath}"

    with open(filepath, 'r') as f:
        content = f.read().strip()

    assert content == "0.800", f"Expected '0.800' in {filepath}, but got '{content}'"