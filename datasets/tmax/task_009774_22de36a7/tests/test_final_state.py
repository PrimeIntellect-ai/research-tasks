# test_final_state.py

import os
import pytest

def test_analyzer_files_exist():
    assert os.path.isfile('/home/user/analyzer.c'), "C source file /home/user/analyzer.c is missing."
    assert os.path.isfile('/home/user/analyzer'), "Executable /home/user/analyzer is missing."
    assert os.access('/home/user/analyzer', os.X_OK), "/home/user/analyzer is not executable."

def test_stats_csv_content():
    stats_path = '/home/user/stats.csv'
    assert os.path.isfile(stats_path), f"Output file {stats_path} is missing."

    expected_lines = [
        "ErrorCode,Count",
        "403,1",
        "404,2",
        "500,2"
    ]

    with open(stats_path, 'r') as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, f"Content of {stats_path} is incorrect. Expected {expected_lines}, got {actual_lines}"

def test_monitor_log_content():
    monitor_path = '/home/user/monitor.log'
    assert os.path.isfile(monitor_path), f"Monitor log file {monitor_path} is missing."

    expected_content = "Processed 7 lines. Found 5 critical errors."

    with open(monitor_path, 'r') as f:
        content = f.read()

    assert expected_content in content, f"Expected '{expected_content}' in {monitor_path}, but got '{content}'"