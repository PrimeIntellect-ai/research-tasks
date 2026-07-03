# test_final_state.py

import os
import json

def test_state_json_updated_correctly():
    state_file = "/home/user/state.json"
    assert os.path.exists(state_file), f"State file {state_file} does not exist"

    with open(state_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{state_file} does not contain valid JSON"

    assert "valid_backups" in data, "Key 'valid_backups' is missing in state.json"

    expected_backups = [
        "/home/user/backups/cfg_01.tar.gz",
        "/home/user/backups/cfg_04.tar.gz"
    ]

    actual_backups = data["valid_backups"]
    assert actual_backups == expected_backups, (
        f"Expected valid_backups to be {expected_backups}, but got {actual_backups}. "
        "Ensure only Pending and valid tar.gz archives are included, in the correct order."
    )

def test_tracker_go_requirements():
    tracker_file = "/home/user/tracker.go"
    assert os.path.exists(tracker_file), f"Source file {tracker_file} does not exist"

    with open(tracker_file, "r") as f:
        content = f.read()

    assert "syscall.Flock" in content, (
        "tracker.go is missing 'syscall.Flock'. You must use syscall.Flock for exclusive file locking."
    )

    assert "os.Rename" in content or "syscall.Rename" in content, (
        "tracker.go is missing 'os.Rename'. You must use an atomic rename to update the state file safely."
    )