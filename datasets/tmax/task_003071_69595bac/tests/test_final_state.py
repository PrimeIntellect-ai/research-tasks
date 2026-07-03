# test_final_state.py

import os
import ast
import pytest

def test_bad_commit_file_exists_and_matches_truth():
    bad_commit_path = "/home/user/bad_commit.txt"
    truth_commit_path = "/home/user/.truth_commit"

    assert os.path.isfile(bad_commit_path), f"The file {bad_commit_path} does not exist."
    assert os.path.isfile(truth_commit_path), f"The truth file {truth_commit_path} is missing."

    with open(bad_commit_path, "r") as f:
        bad_commit = f.read().strip()

    with open(truth_commit_path, "r") as f:
        truth_commit = f.read().strip()

    assert bad_commit == truth_commit, f"The commit hash in {bad_commit_path} ({bad_commit}) does not match the correct bad commit."

def test_test_bisect_script_exists_and_valid():
    script_path = "/home/user/test_bisect.py"

    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

    with open(script_path, "r") as f:
        script_content = f.read()

    try:
        ast.parse(script_content)
    except SyntaxError as e:
        pytest.fail(f"The script {script_path} contains a syntax error: {e}")

    # Check for required logic components via simple string matching
    assert "CONFIG_PATH" in script_content, "The script does not seem to set the 'CONFIG_PATH' environment variable."
    assert "counter.txt" in script_content, "The script does not seem to interact with 'counter.txt'."
    assert "5000" in script_content, "The script does not seem to check for the expected success value of 5000."
    assert "worker.py" in script_content, "The script does not seem to execute 'worker.py'."