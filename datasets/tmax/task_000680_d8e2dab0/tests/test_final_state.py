# test_final_state.py

import os
import re
import pytest

def test_grouped_csv_content():
    processed_file = "/home/user/data/processed/grouped.csv"
    assert os.path.isfile(processed_file), f"Processed file {processed_file} does not exist."

    expected_content = (
        "sensor,event_count,avg_value\n"
        "SensorA,2,11.5\n"
        "SensorB,2,150.0\n"
        "SensorC,1,5.0"
    )

    with open(processed_file, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {processed_file} does not match expected grouped output."

def test_run_log_content():
    log_file = "/home/user/logs/run.log"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."

    with open(log_file, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) > 0, f"Log file {log_file} is empty."

    pattern = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Processed 5 unique records, dropped 4 duplicates\.$")

    match_found = any(pattern.match(line) for line in lines)
    assert match_found, f"No line in {log_file} matches the expected log format and counts."

def test_schedule_cron_content():
    cron_file = "/home/user/schedule.cron"
    assert os.path.isfile(cron_file), f"Cron schedule file {cron_file} does not exist."

    with open(cron_file, "r") as f:
        content = f.read().strip().lower()

    # Valid day of week representations for Sunday are 0, 7, sun
    # The command should be /usr/bin/python3 /home/user/process.py
    # Expected format: 0 0 * * 0 /usr/bin/python3 /home/user/process.py

    # We will use regex to capture the parts, allowing multiple spaces
    pattern = re.compile(r"^0\s+0\s+\*\s+\*\s+(0|7|sun)\s+/usr/bin/python3\s+/home/user/process\.py$")
    assert pattern.match(content), f"Cron entry in {cron_file} is incorrect. Found: {content}"