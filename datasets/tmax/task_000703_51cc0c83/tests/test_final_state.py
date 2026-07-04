# test_final_state.py

import os
import gzip
import json
import pytest

SCRIPT_PATH = "/home/user/check_quota.sh"
LOG_PATH = "/home/user/warnings.log"
DATA_PATH = "/home/user/quotas.json.gz"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_uses_flock():
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()
    assert "flock" in content, "Script does not contain 'flock' command."
    assert "warnings.lock" in content, "Script does not reference 'warnings.lock'."

def test_warnings_log_contents():
    assert os.path.isfile(LOG_PATH), f"Log file {LOG_PATH} does not exist."

    # Compute expected users dynamically
    expected_users = set()
    try:
        with gzip.open(DATA_PATH, "rt") as f:
            data = json.load(f)
            for item in data:
                if item["used"] > 0.9 * item["limit"]:
                    expected_users.add(item["user"])
    except Exception as e:
        pytest.fail(f"Could not read {DATA_PATH} to compute expected users: {e}")

    # Read actual users
    with open(LOG_PATH, "r") as f:
        actual_users = set(line.strip() for line in f if line.strip())

    assert actual_users == expected_users, f"Expected users {expected_users}, but got {actual_users} in {LOG_PATH}."