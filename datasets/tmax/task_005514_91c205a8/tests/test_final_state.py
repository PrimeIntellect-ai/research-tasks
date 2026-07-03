# test_final_state.py

import os
import subprocess
import pytest

TARGET_FILE = "/home/user/recovered_token.txt"
EXPECTED_TOKEN = "SYS_TOK_83749201"

def test_recovered_token_file_exists():
    assert os.path.exists(TARGET_FILE), f"Verification failed: {TARGET_FILE} does not exist."
    assert os.path.isfile(TARGET_FILE), f"Verification failed: {TARGET_FILE} is not a regular file."

def test_recovered_token_content():
    assert os.path.exists(TARGET_FILE), f"Cannot check content, {TARGET_FILE} is missing."
    with open(TARGET_FILE, "r") as f:
        content = f.read().strip()

    assert content == EXPECTED_TOKEN, f"Verification failed: Incorrect token '{content}'. Expected '{EXPECTED_TOKEN}'."

def test_legacy_worker_still_running():
    try:
        output = subprocess.check_output(["pgrep", "-f", "legacy_worker.sh"], text=True)
        pids = output.strip().split('\n')
        assert len(pids) >= 1, "legacy_worker.sh process is no longer running. It should not have been killed."
    except subprocess.CalledProcessError:
        pytest.fail("legacy_worker.sh process is no longer running (pgrep returned no matches). It should not have been killed.")