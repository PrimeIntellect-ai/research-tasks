# test_final_state.py

import os
import tarfile
import gzip
import pytest

def test_incremental_backup_exists():
    path = "/home/user/incremental.tar.gz"
    assert os.path.isfile(path), f"File {path} does not exist"

def test_incremental_backup_contents():
    path = "/home/user/incremental.tar.gz"
    assert tarfile.is_tarfile(path), f"File {path} is not a valid tar archive"

    with tarfile.open(path, "r:gz") as tar:
        # Get all file members (ignoring directories)
        members = [m.name for m in tar.getmembers() if m.isfile()]

    expected_members = {
        "logs/file3.log",
        "logs/file7.log",
        "logs/file11.log",
        "logs/file12.log"
    }

    # Check if the members match exactly
    assert set(members) == expected_members, f"Archive {path} does not contain exactly the expected files. Found: {members}"

def test_fatal_errors_exists():
    path = "/home/user/fatal_errors.gz"
    assert os.path.isfile(path), f"File {path} does not exist"

def test_fatal_errors_contents():
    path = "/home/user/fatal_errors.gz"

    try:
        with gzip.open(path, "rt") as f:
            lines = f.readlines()
    except OSError:
        pytest.fail(f"File {path} is not a valid gzip file")

    # Strip whitespace/newlines and filter empty lines
    actual_lines = [line.strip() for line in lines if line.strip()]

    expected_lines = [
        "FATAL: cpu fire",
        "FATAL: disk crash",
        "FATAL: memory leak"
    ]

    assert actual_lines == expected_lines, f"Contents of {path} do not match the expected sorted FATAL lines. Found: {actual_lines}"