# test_final_state.py

import os
import subprocess
import pytest

REPO_DIR = "/home/user/image_processor"
BAD_COMMIT_FILE = "/home/user/bad_commit.txt"
SYSCALLS_LOG_FILE = "/home/user/syscalls.log"
CORRUPTED_FILENAME_FILE = "/home/user/corrupted_filename.txt"

def get_expected_bad_commit():
    """Retrieve the Git SHA for 'Commit 142' from the repository."""
    result = subprocess.run(
        ["git", "log", "--format=%H %s"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
        check=True
    )
    for line in result.stdout.splitlines():
        if "Commit 142" in line:
            return line.split()[0]
    return None

def test_bad_commit_txt():
    assert os.path.isfile(BAD_COMMIT_FILE), f"{BAD_COMMIT_FILE} does not exist."

    with open(BAD_COMMIT_FILE, "r") as f:
        actual_commit = f.read().strip()

    expected_commit = get_expected_bad_commit()
    assert expected_commit is not None, "Could not find 'Commit 142' in the repository history."
    assert actual_commit == expected_commit, f"Expected bad commit {expected_commit}, but found {actual_commit}."

def test_corrupted_filename_txt():
    assert os.path.isfile(CORRUPTED_FILENAME_FILE), f"{CORRUPTED_FILENAME_FILE} does not exist."

    with open(CORRUPTED_FILENAME_FILE, "r") as f:
        actual_filename = f.read().strip()

    expected_filename = "outpUT_CORRUPT_X99.dat"
    assert actual_filename == expected_filename, f"Expected filename '{expected_filename}', but found '{actual_filename}'."

def test_syscalls_log():
    assert os.path.isfile(SYSCALLS_LOG_FILE), f"{SYSCALLS_LOG_FILE} does not exist."

    with open(SYSCALLS_LOG_FILE, "r") as f:
        content = f.read()

    # Check for keywords that indicate strace output and abort
    assert "SIGABRT" in content, "The syscalls.log does not contain 'SIGABRT', which is expected from the abort() call."
    assert "openat" in content or "open" in content, "The syscalls.log does not contain file opening syscalls."