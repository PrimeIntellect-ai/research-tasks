# test_final_state.py

import os
import pytest

def test_valid_logs_moved():
    """Test that valid logs are moved to the valid_logs directory."""
    valid_dir = "/home/user/valid_logs"
    assert os.path.isdir(valid_dir), f"Directory {valid_dir} is missing."

    files = sorted(os.listdir(valid_dir))
    expected_files = ["log_01.tar.gz", "log_03.tar.gz"]
    assert files == expected_files, f"Expected valid logs {expected_files}, but found {files} in {valid_dir}."

def test_corrupt_logs_moved():
    """Test that corrupt logs are moved to the corrupt_logs directory."""
    corrupt_dir = "/home/user/corrupt_logs"
    assert os.path.isdir(corrupt_dir), f"Directory {corrupt_dir} is missing."

    files = sorted(os.listdir(corrupt_dir))
    expected_files = ["log_02.tar.gz", "log_04.tar.gz", "log_05.tar.gz"]
    assert files == expected_files, f"Expected corrupt logs {expected_files}, but found {files} in {corrupt_dir}."

def test_original_logs_removed():
    """Test that the logs were moved and no longer exist in the original directory."""
    logs_dir = "/home/user/logs"
    if os.path.isdir(logs_dir):
        files = os.listdir(logs_dir)
        # Check that none of the original files are still there
        for f in ["log_01.tar.gz", "log_02.tar.gz", "log_03.tar.gz", "log_04.tar.gz", "log_05.tar.gz"]:
            assert f not in files, f"File {f} should have been moved out of {logs_dir}."

def test_report_content():
    """Test that the report.txt contains the correct sorted list of corrupted files."""
    report_file = "/home/user/report.txt"
    assert os.path.isfile(report_file), f"Report file {report_file} is missing."

    with open(report_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["log_02.tar.gz", "log_04.tar.gz", "log_05.tar.gz"]
    assert lines == expected_lines, f"Expected report lines {expected_lines}, but got {lines}."