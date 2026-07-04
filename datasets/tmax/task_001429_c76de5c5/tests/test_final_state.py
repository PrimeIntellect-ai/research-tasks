# test_final_state.py
import os

def test_resolution_log_exists():
    assert os.path.isfile("/home/user/resolution.log"), "File /home/user/resolution.log does not exist."

def test_resolution_log_content():
    with open("/home/user/resolution.log", "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, "/home/user/resolution.log must contain at least two lines (key and commit hash)."

    with open("/root/expected_key.txt", "r") as f:
        expected_key = f.read().strip()

    with open("/root/expected_commit.txt", "r") as f:
        expected_commit = f.read().strip()

    actual_key = lines[0]
    actual_commit = lines[1]

    assert actual_key == expected_key, f"Line 1 is incorrect. Expected the secret key, but got: '{actual_key}'"
    assert actual_commit == expected_commit, f"Line 2 is incorrect. Expected the bad commit hash, but got: '{actual_commit}'"