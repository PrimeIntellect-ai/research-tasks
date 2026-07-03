# test_final_state.py

import os
import subprocess
import pytest

REPO_DIR = "/home/user/perf-repo"
RUNNER_SCRIPT = os.path.join(REPO_DIR, "runner.sh")
USER_BAD_COMMIT_FILE = "/home/user/bad_commit.txt"
EXPECTED_BAD_COMMIT_FILE = "/tmp/expected_bad_commit.txt"

def test_bad_commit_identified():
    assert os.path.isfile(USER_BAD_COMMIT_FILE), f"File {USER_BAD_COMMIT_FILE} does not exist."
    assert os.path.isfile(EXPECTED_BAD_COMMIT_FILE), f"File {EXPECTED_BAD_COMMIT_FILE} does not exist."

    with open(EXPECTED_BAD_COMMIT_FILE, "r") as f:
        expected_commit = f.read().strip()

    with open(USER_BAD_COMMIT_FILE, "r") as f:
        user_commit = f.read().strip()

    assert user_commit == expected_commit, f"Expected bad commit {expected_commit}, but got {user_commit}."

def test_runner_script_fixed_and_output_correct():
    assert os.path.isfile(RUNNER_SCRIPT), f"File {RUNNER_SCRIPT} does not exist."
    assert os.access(RUNNER_SCRIPT, os.X_OK), f"File {RUNNER_SCRIPT} is not executable."

    try:
        result = subprocess.run(
            [RUNNER_SCRIPT],
            capture_output=True,
            text=True,
            timeout=1.0,
            check=False
        )
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution of {RUNNER_SCRIPT} timed out. The infinite recursion bug might still be present.")

    assert result.returncode == 0, f"Expected exit code 0, but got {result.returncode}."

    expected_output = "Processing task1\nProcessing task2\nProcessing task3\n"
    assert result.stdout == expected_output, f"Expected output:\n{expected_output}\nBut got:\n{result.stdout}"

def test_runner_script_is_recursive():
    assert os.path.isfile(RUNNER_SCRIPT), f"File {RUNNER_SCRIPT} does not exist."

    with open(RUNNER_SCRIPT, "r") as f:
        content = f.read()

    # Check that the function process_jobs is defined and calls itself
    assert "process_jobs" in content, "The runner.sh script must contain the 'process_jobs' function."

    # Simple heuristic to ensure recursive structure is kept
    lines = content.splitlines()
    call_count = sum(1 for line in lines if "process_jobs" in line and not line.strip().startswith("process_jobs()"))
    assert call_count >= 2, "The 'process_jobs' function must be called recursively and at least once initially."