# test_final_state.py

import os
import gzip
import hashlib
import pytest

def test_manifest_file():
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file missing: {manifest_path}"

    with open(manifest_path, "r") as f:
        lines = f.read().strip().split('\n')

    expected_lines = [
        "dirA/file2.txt e182e0e02eb7fa01bc6c071bb9cc233d45512b9826f59232eb1e4eb41d5b369c",
        "dirB/dirC/file4.txt 8d6ff06a8e52eec87cd7a7b8e1a1792f3900985ca581b957cf94819779df20bd",
        "dirB/file3.txt 8d6ff06a8e52eec87cd7a7b8e1a1792f3900985ca581b957cf94819779df20bd",
        "file1.txt e182e0e02eb7fa01bc6c071bb9cc233d45512b9826f59232eb1e4eb41d5b369c"
    ]

    assert lines == expected_lines, "Manifest content does not match expected output or is not sorted."

def test_error_log():
    error_log_path = "/home/user/symlink_errors.log"
    assert os.path.isfile(error_log_path), f"Error log missing: {error_log_path}"

    with open(error_log_path, "r") as f:
        lines = sorted(f.read().strip().split('\n'))

    expected_lines = [
        "/home/user/data_source/dirA/loop1",
        "/home/user/data_source/dirB/dirC/loop2"
    ]

    assert lines == expected_lines, "Error log content does not match expected output."

def test_archive_files_and_hardlinks():
    dest_dir = "/home/user/archive_dest"
    assert os.path.isdir(dest_dir), f"Destination directory missing: {dest_dir}"

    file1 = os.path.join(dest_dir, "file1.txt.gz")
    file2 = os.path.join(dest_dir, "dirA/file2.txt.gz")
    file3 = os.path.join(dest_dir, "dirB/file3.txt.gz")
    file4 = os.path.join(dest_dir, "dirB/dirC/file4.txt.gz")

    for f in [file1, file2, file3, file4]:
        assert os.path.isfile(f), f"Archive file missing: {f}"

    stat1 = os.stat(file1)
    stat2 = os.stat(file2)
    stat3 = os.stat(file3)
    stat4 = os.stat(file4)

    assert stat1.st_ino == stat2.st_ino, "file1.txt.gz and file2.txt.gz are not hard linked."
    assert stat3.st_ino == stat4.st_ino, "file3.txt.gz and file4.txt.gz are not hard linked."

    assert stat1.st_nlink == 2, f"Expected 2 hard links for file1.txt.gz, got {stat1.st_nlink}"
    assert stat3.st_nlink == 2, f"Expected 2 hard links for file3.txt.gz, got {stat3.st_nlink}"

def test_gzip_content():
    dest_dir = "/home/user/archive_dest"

    expected_content_1 = b"Hello World! This is a test file for deduplication.\n"
    expected_content_3 = b"Different content for file 3.\n"

    file1 = os.path.join(dest_dir, "file1.txt.gz")
    file3 = os.path.join(dest_dir, "dirB/file3.txt.gz")

    with gzip.open(file1, "rb") as f:
        content1 = f.read()
    assert content1 == expected_content_1, "Uncompressed content of file1.txt.gz does not match original."

    with gzip.open(file3, "rb") as f:
        content3 = f.read()
    assert content3 == expected_content_3, "Uncompressed content of file3.txt.gz does not match original."