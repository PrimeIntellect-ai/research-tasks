# test_final_state.py
import os
import re
import pytest

def test_bootstrap_rs_optimized():
    bootstrap_path = '/home/user/sequence_aligner/src/bootstrap.rs'
    assert os.path.isfile(bootstrap_path), "bootstrap.rs is missing."

    with open(bootstrap_path, 'r') as f:
        content = f.read()

    # The bottleneck was `let temp_data = data.to_vec();`
    # Ensure to_vec() is not called on `data` inside the loop.
    # A simple check is that `to_vec()` or `clone()` is not present in the file, 
    # or at least not used for `data` inside the loop.
    assert "data.to_vec()" not in content, "The performance bug (data.to_vec()) is still present in bootstrap.rs."

def test_run_tests_sh_exists_and_executable():
    script_path = '/home/user/run_tests.sh'
    assert os.path.isfile(script_path), "/home/user/run_tests.sh does not exist."
    assert os.access(script_path, os.X_OK), "/home/user/run_tests.sh is not executable."

def test_ci_result_content():
    result_path = '/home/user/ci_result.txt'
    assert os.path.isfile(result_path), "/home/user/ci_result.txt does not exist."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    expected_result = "44.60,50.35"
    assert content == expected_result, f"Expected /home/user/ci_result.txt to contain '{expected_result}', but found '{content}'."