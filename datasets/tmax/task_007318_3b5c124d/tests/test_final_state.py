# test_final_state.py

import os
import pytest

def test_summary_file():
    summary_path = "/home/user/summary.txt"
    assert os.path.isfile(summary_path), f"The file {summary_path} does not exist."

    with open(summary_path, "r") as f:
        content = f.read().strip()

    assert content == "3", f"Expected summary.txt to contain '3', but found '{content}'."

def test_renamed_archived_files():
    # system_01 and system_03 should be renamed to .archived
    expected_archived = [
        "/home/user/logs/system_01.log.gz.archived",
        "/home/user/logs/system_03.log.gz.archived"
    ]
    for path in expected_archived:
        assert os.path.isfile(path), f"Expected archived file {path} is missing. It was not renamed correctly."

    # Original files should no longer exist
    unexpected_originals = [
        "/home/user/logs/system_01.log.gz",
        "/home/user/logs/system_03.log.gz"
    ]
    for path in unexpected_originals:
        assert not os.path.exists(path), f"Original file {path} still exists. It should have been renamed."

def test_unmodified_files():
    # system_02 should NOT be renamed
    expected_original = "/home/user/logs/system_02.log.gz"
    assert os.path.isfile(expected_original), f"Expected unmodified file {expected_original} is missing."

    unexpected_archived = "/home/user/logs/system_02.log.gz.archived"
    assert not os.path.exists(unexpected_archived), f"File {unexpected_archived} should not exist. It was incorrectly renamed."

def test_no_decompressed_files():
    # Ensure no .log files were left on disk (requirement: do not extract to disk)
    logs_dir = "/home/user/logs"
    if os.path.isdir(logs_dir):
        for filename in os.listdir(logs_dir):
            assert not filename.endswith(".log"), f"Found uncompressed log file {filename} in {logs_dir}. Files should not be permanently decompressed to disk."