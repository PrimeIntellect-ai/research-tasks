# test_final_state.py

import os
import glob
import pytest

def test_archiver_cpp_exists():
    assert os.path.isfile("/home/user/archiver.cpp"), "The C++ source file /home/user/archiver.cpp is missing."

def test_archive_dat_exists_and_content():
    archive_path = "/home/user/archive.dat"
    assert os.path.isfile(archive_path), f"The archive file {archive_path} is missing."

    with open(archive_path, "r") as f:
        content = f.read()

    expected_content = (
        "=== app.log ===\n"
        "FATAL Out of memory exception in thread 1\n"
        "FATAL Process crashed\n"
        "=== sys.log ===\n"
        "FATAL Disk /dev/sda1 failure\n"
    )

    assert content == expected_content, f"The content of {archive_path} does not match the expected format and filtered lines."

def test_processed_log_files_exist():
    expected_files = [
        "/home/user/logs/app.log.processed",
        "/home/user/logs/auth.log.processed",
        "/home/user/logs/sys.log.processed"
    ]
    for file_path in expected_files:
        assert os.path.isfile(file_path), f"The processed log file {file_path} is missing."

def test_no_unprocessed_log_files():
    unprocessed_logs = glob.glob("/home/user/logs/*.log")
    assert len(unprocessed_logs) == 0, f"Found unprocessed log files: {unprocessed_logs}. They should have been renamed to .log.processed."