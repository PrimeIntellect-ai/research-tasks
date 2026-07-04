# test_final_state.py
import os
import pytest

def test_compromised_actions_file_exists():
    path = "/home/user/audit/compromised_actions.txt"
    assert os.path.isfile(path), f"The file {path} does not exist. Did you generate the report?"

def test_compromised_actions_contents():
    path = "/home/user/audit/compromised_actions.txt"
    assert os.path.isfile(path), f"The file {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    expected_actions = [
        "EXFILTRATE_USERS",
        "DELETE_ALL_AUDIT"
    ]

    actual_actions = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_actions == expected_actions, (
        f"The contents of {path} do not match the expected decrypted actions.\n"
        f"Expected: {expected_actions}\n"
        f"Got: {actual_actions}"
    )