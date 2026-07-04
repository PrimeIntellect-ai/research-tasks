# test_final_state.py

import os
import tarfile
import pytest

PROCESSED_DIR = "/home/user/processed"

def test_processed_files_exist():
    expected_files = [
        "archive1_safe_30.tar.gz",
        "archive2_safe_15.tar.gz",
        "archive3_safe_25.tar.gz"
    ]

    assert os.path.exists(PROCESSED_DIR), f"Processed directory {PROCESSED_DIR} does not exist."

    for f in expected_files:
        filepath = os.path.join(PROCESSED_DIR, f)
        assert os.path.exists(filepath), f"Expected output file {filepath} is missing. Check your renaming logic and size calculation."
        assert os.path.isfile(filepath), f"{filepath} is not a file."

def test_archive1_contents():
    filepath = os.path.join(PROCESSED_DIR, "archive1_safe_30.tar.gz")
    assert os.path.exists(filepath), f"File {filepath} missing."

    with tarfile.open(filepath, "r:gz") as tar:
        names = tar.getnames()
        assert len(names) == 2, f"Expected 2 files in archive1, found {len(names)}: {names}"
        assert "file1.txt" in names, "file1.txt missing from processed archive1"
        assert "dir/file2.txt" in names, "dir/file2.txt missing from processed archive1"

        # Verify sizes
        assert tar.getmember("file1.txt").size == 10
        assert tar.getmember("dir/file2.txt").size == 20

def test_archive2_contents():
    filepath = os.path.join(PROCESSED_DIR, "archive2_safe_15.tar.gz")
    assert os.path.exists(filepath), f"File {filepath} missing."

    with tarfile.open(filepath, "r:gz") as tar:
        names = tar.getnames()
        assert len(names) == 1, f"Expected 1 file in archive2, found {len(names)}: {names}"
        assert "safe.txt" in names, "safe.txt missing from processed archive2"
        assert "../malicious.txt" not in names, "Malicious file with directory traversal was not filtered out!"

        # Verify size
        assert tar.getmember("safe.txt").size == 15

def test_archive3_contents():
    filepath = os.path.join(PROCESSED_DIR, "archive3_safe_25.tar.gz")
    assert os.path.exists(filepath), f"File {filepath} missing."

    with tarfile.open(filepath, "r:gz") as tar:
        names = tar.getnames()
        assert len(names) == 1, f"Expected 1 file in archive3, found {len(names)}: {names}"
        assert "log/safe.log" in names, "log/safe.log missing from processed archive3"
        assert "/etc/passwd" not in names, "Malicious file with absolute path was not filtered out!"

        # Verify size
        assert tar.getmember("log/safe.log").size == 25