# test_final_state.py

import os
import pytest

def test_archiver_c_exists():
    path = "/home/user/archiver.c"
    assert os.path.isfile(path), f"Source file {path} does not exist."

def test_archiver_executable_exists():
    path = "/home/user/archiver"
    assert os.path.isfile(path), f"Executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_backup_archive_exists_and_content():
    path = "/home/user/backup.archive"
    assert os.path.isfile(path), f"Archive file {path} does not exist."

    with open(path, "r") as f:
        lines = f.read().splitlines()

    expected_lines = {
        "DIR|subdir",
        "FILE|file1.txt|6|5a9b",
        "FILE|subdir/file2.txt|10|4x2y6z2\n",
        "LINK|link_a|link_b",
        "LINK|subdir/link_b|link_a"
    }

    actual_lines = set(lines)

    missing = expected_lines - actual_lines
    extra = actual_lines - expected_lines

    error_msg = []
    if missing:
        error_msg.append(f"Missing expected lines in archive: {missing}")
    if extra:
        error_msg.append(f"Unexpected extra lines in archive: {extra}")

    assert not missing and not extra, "\n".join(error_msg)