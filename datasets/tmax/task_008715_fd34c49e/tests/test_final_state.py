# test_final_state.py

import os
import re
import pytest

def test_files_exist_and_executable():
    assert os.path.isfile("/home/user/normalize.c"), "/home/user/normalize.c does not exist."

    executable_path = "/home/user/normalize"
    assert os.path.isfile(executable_path), f"{executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"{executable_path} is not executable."

    script_path = "/home/user/process.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_clean_data_csv():
    csv_path = "/home/user/clean_data.csv"
    assert os.path.isfile(csv_path), f"{csv_path} does not exist. Did you run process.sh?"

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "A1,3.0000",
        "B2,7.5000",
        "C3,0.5000",
        "D4,0.8400",
        "E5,0.0000"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {csv_path}, but found {len(lines)}."

    for i, expected in enumerate(expected_lines):
        assert lines[i] == expected, f"Line {i+1} in {csv_path} is incorrect. Expected '{expected}', got '{lines[i]}'."

def test_report_md():
    report_path = "/home/user/report.md"
    assert os.path.isfile(report_path), f"{report_path} does not exist. Did you run process.sh?"

    with open(report_path, "r") as f:
        content = f.read().strip()

    assert "Total records processed: 5" in content, f"Expected 'Total records processed: 5' in {report_path}."
    assert "{{COUNT}}" not in content, f"Placeholder {{{{COUNT}}}} was not replaced in {report_path}."

def test_cron_schedule():
    cron_path = "/home/user/cron_schedule.txt"
    assert os.path.isfile(cron_path), f"{cron_path} does not exist."

    with open(cron_path, "r") as f:
        content = f.read().strip()

    # Check for midnight cron expression: "0 0 * * *"
    # It might have multiple spaces or tabs
    parts = content.split()
    assert len(parts) >= 6, f"{cron_path} does not contain a valid cron expression."

    assert parts[0] == "0", f"Minute field in cron expression should be 0, got {parts[0]}"
    assert parts[1] == "0", f"Hour field in cron expression should be 0, got {parts[1]}"
    assert parts[2] == "*", f"Day of month field in cron expression should be *, got {parts[2]}"
    assert parts[3] == "*", f"Month field in cron expression should be *, got {parts[3]}"
    assert parts[4] == "*", f"Day of week field in cron expression should be *, got {parts[4]}"

    command = " ".join(parts[5:])
    assert "/home/user/process.sh" in command, f"Cron command should execute /home/user/process.sh, got '{command}'"