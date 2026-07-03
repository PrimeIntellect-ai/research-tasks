# test_final_state.py

import os
import json
import subprocess
import pytest

def test_bad_commit():
    repo_dir = "/home/user/decoder_project"
    bad_commit_file = "/home/user/bad_commit.txt"

    assert os.path.exists(bad_commit_file), f"{bad_commit_file} does not exist."

    with open(bad_commit_file, "r") as f:
        actual_commit = f.read().strip()

    # Derive the expected commit hash from the git repository based on the commit message
    res = subprocess.run(
        ["git", "log", "--grep=Optimize by adding multithreading", "--format=%H"],
        cwd=repo_dir, capture_output=True, text=True, check=True
    )
    expected_commit = res.stdout.strip()

    assert expected_commit, "Could not find the target commit in the repository."
    assert actual_commit == expected_commit, f"Incorrect commit hash in {bad_commit_file}. Expected {expected_commit}, got {actual_commit}"

def test_secret_key():
    key_file = "/home/user/secret_key.txt"
    assert os.path.exists(key_file), f"{key_file} does not exist."

    with open(key_file, "r") as f:
        actual_key = f.read().strip()

    assert actual_key == "N0vA_s3cR3t_99xY", f"Secret key in {key_file} is incorrect."

def test_secure_runner_script():
    runner_file = "/home/user/secure_runner.py"
    assert os.path.exists(runner_file), f"{runner_file} does not exist."

    with open(runner_file, "r") as f:
        content = f.read()

    assert "ThreadPoolExecutor" in content, "secure_runner.py must use ThreadPoolExecutor."
    assert "Lock" in content or "lock" in content.lower(), "secure_runner.py must use a locking mechanism."

def test_output_json():
    json_file = "/home/user/output.json"
    assert os.path.exists(json_file), f"{json_file} does not exist."

    with open(json_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_file} is not valid JSON.")

    assert isinstance(data, list), f"{json_file} must contain a JSON array."
    assert len(data) == 98, f"Expected exactly 98 successful decodes, but found {len(data)}."

    expected = [f"Decoded: VALID_DATA_PAYLOAD_{i}" for i in range(1, 101) if i not in (42, 73)]
    assert sorted(data) == sorted(expected), f"The contents of {json_file} do not match the expected successfully decoded payloads."