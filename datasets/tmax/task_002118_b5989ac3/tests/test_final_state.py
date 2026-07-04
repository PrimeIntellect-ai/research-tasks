# test_final_state.py

import os
import pytest

def test_kl_result_exists():
    path = "/home/user/kl_result.txt"
    assert os.path.isfile(path), f"File not found: {path}. The task requires saving the result to this file."

def test_kl_result_content():
    result_path = "/home/user/kl_result.txt"
    expected_path = "/home/user/expected_kl.txt"

    assert os.path.isfile(expected_path), "Expected result file missing (environment setup issue)."
    assert os.path.isfile(result_path), f"Result file missing: {result_path}"

    with open(result_path, 'r') as f:
        result_val = f.read().strip()

    with open(expected_path, 'r') as f:
        expected_val = f.read().strip()

    assert result_val == expected_val, f"KL divergence result mismatch. Expected {expected_val}, got {result_val}."

def test_go_code_exists():
    path = "/home/user/analysis/analyze.go"
    assert os.path.isfile(path), f"Go source file not found: {path}. The task requires writing the solution here."