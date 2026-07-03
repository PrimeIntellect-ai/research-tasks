# test_final_state.py

import os
import stat
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/process_changes.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_invalid_lines_log():
    log_path = "/home/user/invalid_lines.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. Did the script run?"

    expected_lines = [
        "INVALID LINE 1",
        "2024-05-01 02:XX:00,bad,BAD,SUCCESS"
    ]

    with open(log_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Content of {log_path} does not match expected invalid lines."

def test_hourly_summary_csv():
    csv_path = "/home/user/hourly_summary.csv"
    assert os.path.isfile(csv_path), f"File {csv_path} does not exist. Did the script run?"

    expected_lines = [
        "2024-05-01 00:00,1",
        "2024-05-01 01:00,2",
        "2024-05-01 02:00,0",
        "2024-05-01 03:00,1",
        "2024-05-01 04:00,0",
        "2024-05-01 05:00,1"
    ]

    with open(csv_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Content of {csv_path} does not match the expected time-based bucketing and gap-filling."