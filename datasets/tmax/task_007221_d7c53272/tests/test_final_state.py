# test_final_state.py

import os
import tarfile
import json
import pytest

ARCHIVE_PATH = "/home/user/incremental_backup.tar.gz"
STATE_FILE = "/home/user/backup_state.json"
SOURCE_DIR = "/home/user/images"

def test_archive_contents():
    assert os.path.exists(ARCHIVE_PATH), f"Archive {ARCHIVE_PATH} was not created."

    with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
        members = tar.getmembers()
        names = [os.path.basename(m.name) for m in members if m.isfile()]

    expected_names = {"updated.png", "new.png"}
    assert set(names) == expected_names, f"Archive should contain exactly {expected_names}, but found {set(names)}"

def test_state_file_contents():
    assert os.path.exists(STATE_FILE), f"State file {STATE_FILE} does not exist."

    with open(STATE_FILE, "r") as f:
        try:
            state = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"State file {STATE_FILE} is not valid JSON.")

    assert "fake.png" not in state, "fake.png should not be in the state file because it is not a valid PNG."

    expected_files = ["old.png", "updated.png", "new.png"]
    for filename in expected_files:
        assert filename in state, f"{filename} is missing from the state file."

        filepath = os.path.join(SOURCE_DIR, filename)
        actual_mtime = os.path.getmtime(filepath)

        assert state[filename] == actual_mtime, f"mtime for {filename} in state file does not match actual file mtime."