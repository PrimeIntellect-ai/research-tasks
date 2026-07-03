# test_final_state.py

import os
import json
import subprocess
import pytest

def test_bad_commit_correct():
    user_file = "/home/user/bad_commit.txt"
    truth_file = "/tmp/true_bad_commit.txt"

    assert os.path.exists(user_file), f"{user_file} is missing."
    assert os.path.exists(truth_file), f"{truth_file} is missing."

    with open(user_file, "r") as f:
        user_commit = f.read().strip()

    with open(truth_file, "r") as f:
        true_commit = f.read().strip()

    assert user_commit == true_commit, f"Expected bad commit {true_commit}, but got {user_commit}."

def test_payload_causes_crash_on_bad_commit():
    payload_file = "/home/user/crash_payload.txt"
    truth_file = "/tmp/true_bad_commit.txt"
    repo_dir = "/home/user/math_evaluator"

    assert os.path.exists(payload_file), f"{payload_file} is missing."

    with open(payload_file, "r") as f:
        payload = f.read().strip()

    with open(truth_file, "r") as f:
        true_commit = f.read().strip()

    # Checkout the bad commit
    subprocess.run(["git", "checkout", "-f", true_commit], cwd=repo_dir, check=True, capture_output=True)

    # Run the script with the payload
    arg = json.dumps({"expr_b64": payload})
    result = subprocess.run(
        ["python3", "evaluate.py", arg],
        cwd=repo_dir,
        capture_output=True
    )

    # It should crash (non-zero exit code)
    assert result.returncode != 0, "Payload did not cause a crash (exit code 0) on the bad commit."

def test_payload_works_on_initial_commit():
    payload_file = "/home/user/crash_payload.txt"
    repo_dir = "/home/user/math_evaluator"

    assert os.path.exists(payload_file), f"{payload_file} is missing."

    with open(payload_file, "r") as f:
        payload = f.read().strip()

    # Get the initial commit
    res = subprocess.run(
        ["git", "rev-list", "--max-parents=0", "HEAD"],
        cwd=repo_dir,
        check=True,
        capture_output=True,
        text=True
    )
    initial_commit = res.stdout.strip().split('\n')[0]

    # Checkout the initial commit
    subprocess.run(["git", "checkout", "-f", initial_commit], cwd=repo_dir, check=True, capture_output=True)

    # Run the script with the payload
    arg = json.dumps({"expr_b64": payload})
    result = subprocess.run(
        ["python3", "evaluate.py", arg],
        cwd=repo_dir,
        capture_output=True
    )

    # It should exit cleanly (exit code 0)
    assert result.returncode == 0, f"Payload caused a crash on the initial commit. Stderr: {result.stderr.decode()}"