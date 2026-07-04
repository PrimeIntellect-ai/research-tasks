# test_final_state.py

import os
import json
import math
import subprocess
import pytest

def test_bad_commit_txt():
    expected_file = "/tmp/expected_bad_commit.txt"
    actual_file = "/home/user/bad_commit.txt"

    assert os.path.exists(expected_file), "Truth file /tmp/expected_bad_commit.txt is missing."
    assert os.path.exists(actual_file), f"Expected file {actual_file} to be created by the user."

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    with open(actual_file, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Expected bad commit hash '{expected_hash}', but got '{actual_hash}'."

def test_fixed_output_txt():
    output_file = "/home/user/fixed_output.txt"
    assert os.path.exists(output_file), f"Expected file {output_file} to be created."

    with open(output_file, "r") as f:
        try:
            output_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Content of {output_file} is not valid JSON.")

    assert isinstance(output_data, list), "Output should be a JSON array."
    assert len(output_data) == 3, "Output array should have 3 elements."

    # Compute expected softmax for [1000.0, 1001.0, 1002.0]
    x = [1000.0, 1001.0, 1002.0]
    max_x = max(x)
    exp_x = [math.exp(i - max_x) for i in x]
    sum_exp_x = sum(exp_x)
    expected_data = [i / sum_exp_x for i in exp_x]

    for actual, expected in zip(output_data, expected_data):
        assert math.isclose(actual, expected, rel_tol=1e-5), f"Expected {expected}, got {actual}. The softmax calculation is incorrect."

def test_softmax_script_fixed():
    script_path = "/home/user/ml_tools/softmax.py"
    input_path = "/home/user/eval data/large_inputs.json"

    assert os.path.exists(script_path), f"Expected file {script_path} to exist."

    result = subprocess.run(
        ["python3", script_path, input_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"softmax.py crashed. stderr: {result.stderr}"
    assert "OverflowError" not in result.stderr, "softmax.py still raises OverflowError."

    try:
        data = json.loads(result.stdout.strip())
        assert isinstance(data, list), "Output of softmax.py should be a JSON array."
    except json.JSONDecodeError:
        pytest.fail("Output of softmax.py is not valid JSON.")

def test_is_on_main_branch():
    repo_path = "/home/user/ml_tools"
    result = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to run git branch."
    branch = result.stdout.strip()
    assert branch == "main", f"Expected to be on 'main' branch, but currently on '{branch}'."