# test_final_state.py

import os
import json
import re
import subprocess
import pytest

def test_investigation_json():
    json_path = "/home/user/investigation.json"
    assert os.path.exists(json_path), f"File {json_path} does not exist. You must create this file with your findings."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "first_bad_commit" in data, "Key 'first_bad_commit' is missing in the JSON file."
    assert "secret_token" in data, "Key 'secret_token' is missing in the JSON file."

    # Derive expected secret token from the memory dump
    dump_path = "/home/user/core.dmp"
    assert os.path.exists(dump_path), f"File {dump_path} does not exist."

    with open(dump_path, 'rb') as f:
        content = f.read()

    # Find the token using regex matching the format SECRET_TOKEN-<16 alphanumeric characters>
    match = re.search(rb"SECRET_TOKEN-[a-zA-Z0-9]{16}", content)
    assert match is not None, "Could not find the SECRET_TOKEN in core.dmp."
    expected_token = match.group(0).decode('utf-8')

    # Derive expected bad commit from the git history
    repo_path = "/home/user/sync_service"
    try:
        output = subprocess.check_output(
            ["git", "log", "--format=%H", "--grep=Optimize lock acquisition order"],
            cwd=repo_path,
            text=True
        ).strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run git log in {repo_path}: {e}")

    expected_commits = output.splitlines()
    assert expected_commits, "Could not find the bad commit in git history."
    expected_commit = expected_commits[-1]  # The first one introduced chronologically if there are multiple

    # Assert the final state matches the derived expected values
    assert data["first_bad_commit"] == expected_commit, f"Incorrect first_bad_commit. Expected {expected_commit}, got {data['first_bad_commit']}."
    assert data["secret_token"] == expected_token, f"Incorrect secret_token. Expected {expected_token}, got {data['secret_token']}."