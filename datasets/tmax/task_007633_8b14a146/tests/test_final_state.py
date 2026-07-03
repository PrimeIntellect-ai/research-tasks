# test_final_state.py

import os
import pytest

def test_output_files_exist():
    """Check that the expected output files are created."""
    assert os.path.exists("/home/user/corrupt_backups.txt"), "The file /home/user/corrupt_backups.txt is missing."
    assert os.path.exists("/home/user/valid_backups.txt"), "The file /home/user/valid_backups.txt is missing."

def test_corrupt_backups_content():
    """Check the content of corrupt_backups.txt."""
    expected = [
        "/home/user/data_mount/projects/corrupt_old.tar.gz",
        "/home/user/data_mount/users/bob/corrupt_old.zip"
    ]

    with open("/home/user/corrupt_backups.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected, f"Expected corrupt_backups.txt to contain {expected}, but got {lines}."

def test_valid_backups_content():
    """Check the content of valid_backups.txt."""
    expected = [
        "/home/user/data_mount/projects/valid_old.zip",
        "/home/user/data_mount/users/alice/valid_old.tar.gz"
    ]

    with open("/home/user/valid_backups.txt", "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected, f"Expected valid_backups.txt to contain {expected}, but got {lines}."

def test_script_exists():
    """Check that the student script exists."""
    assert os.path.isfile("/home/user/verify_storage.py"), "The script /home/user/verify_storage.py is missing."