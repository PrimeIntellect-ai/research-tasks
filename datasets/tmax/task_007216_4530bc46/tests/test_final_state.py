# test_final_state.py

import os
import pytest

def test_renamed_logs():
    """Verify that logs meeting the criteria were renamed properly, and others were ignored."""
    archive_old = "/home/user/logs/archive_old_app.log"
    original_old = "/home/user/logs/old app.log"
    archive_large = "/home/user/logs/subdir/archive_large_file.log"
    original_large = "/home/user/logs/subdir/large file.log"
    normal_log = "/home/user/logs/normal.log"
    archive_normal = "/home/user/logs/archive_normal.log"

    assert os.path.isfile(archive_old), f"Expected renamed file missing: {archive_old}"
    assert not os.path.exists(original_old), f"Original file should have been renamed: {original_old}"

    assert os.path.isfile(archive_large), f"Expected renamed file missing: {archive_large}"
    assert not os.path.exists(original_large), f"Original file should have been renamed: {original_large}"

    assert os.path.isfile(normal_log), f"Normal log should not have been modified: {normal_log}"
    assert not os.path.exists(archive_normal), f"Normal log was incorrectly renamed to: {archive_normal}"

def test_corrupted_archives():
    """Verify that the corrupted_archives.txt file exists and contains the correct sorted paths."""
    corrupted_file_path = "/home/user/corrupted_archives.txt"
    assert os.path.isfile(corrupted_file_path), f"File missing: {corrupted_file_path}"

    with open(corrupted_file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_corrupt = [
        "/home/user/archives/backup_corrupted.tar.gz",
        "/home/user/archives/bad_archive.tar.gz"
    ]
    expected_corrupt.sort()

    assert lines == expected_corrupt, f"Contents of {corrupted_file_path} do not match expected sorted paths. Expected {expected_corrupt}, got {lines}"

def test_processed_incoming_files():
    """Verify that the 3 incoming files were detected, renamed, and moved to the logs directory."""
    for i in range(1, 4):
        processed_file = f"/home/user/logs/processed_file{i}.log"
        incoming_file = f"/home/user/incoming/file{i}.log"

        assert os.path.isfile(processed_file), f"Processed incoming file is missing: {processed_file}"
        assert not os.path.exists(incoming_file), f"Incoming file was not removed from incoming directory: {incoming_file}"