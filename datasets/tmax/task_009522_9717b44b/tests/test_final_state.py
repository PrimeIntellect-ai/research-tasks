# test_final_state.py

import os
import subprocess
import pytest

def test_optimize_test_exists_and_contains_requirements():
    test_file = "/home/user/seq_analyzer/optimize_test.go"
    assert os.path.isfile(test_file), f"{test_file} is missing. You need to create the regression test."

    with open(test_file, "r") as f:
        content = f.read()

    # Check for presence of required parameters in the test file
    assert "1.0" in content and "2.0" in content, "optimize_test.go is missing the required ratios [1.0, 2.0]"
    assert "2.0" in content and "4.0" in content, "optimize_test.go is missing the required targets [2.0, 4.0]"
    assert "0.1" in content, "optimize_test.go is missing the required learning rate 0.1"
    assert "100" in content, "optimize_test.go is missing the required epochs 100"

def test_go_test_passes():
    # Run go test to ensure the tests pass, which implies the bug is fixed and the test is correct
    result = subprocess.run(
        ["go", "test"],
        cwd="/home/user/seq_analyzer",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"'go test' failed in /home/user/seq_analyzer.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_result_txt_content():
    result_file = "/home/user/result.txt"
    assert os.path.isfile(result_file), f"{result_file} is missing. Did you redirect the output or modify main.go?"

    with open(result_file, "r") as f:
        content = f.read().strip()

    # Based on the provided sequences and targets, the optimal k converges to 0.545454...
    # Formatted to 4 decimal places, this is 0.5455.
    assert content == "0.5455", f"Expected '0.5455' in {result_file}, but got '{content}'"