# test_final_state.py
import os
import re
import pytest

def test_analyzer_c_exists():
    assert os.path.isfile("/home/user/analyzer.c"), "/home/user/analyzer.c is missing."

def test_analyzer_executable_exists():
    assert os.path.isfile("/home/user/analyzer"), "/home/user/analyzer executable is missing."
    assert os.access("/home/user/analyzer", os.X_OK), "/home/user/analyzer is not executable."

def test_anomalies_log_content():
    log_path = "/home/user/anomalies.log"
    assert os.path.isfile(log_path), f"{log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip().splitlines()

    expected_lines = [
        "TIMESTAMP: 1620000360, AVG_TEMP: 82.20, CPU: 10",
        "TIMESTAMP: 1620000420, AVG_TEMP: 87.00, CPU: 10",
        "TIMESTAMP: 1620000480, AVG_TEMP: 90.40, CPU: 5"
    ]

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in {log_path}, found {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual.strip() == expected, f"Line {i+1} in {log_path} does not match. Expected '{expected}', got '{actual.strip()}'."

def test_run_pipeline_sh():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert "/home/user/analyzer" in content, f"{script_path} does not seem to execute /home/user/analyzer."

def test_crontab_txt():
    cron_path = "/home/user/crontab.txt"
    assert os.path.isfile(cron_path), f"{cron_path} is missing."

    with open(cron_path, "r") as f:
        content = f.read().strip()

    # Valid 5-minute schedules: "*/5 * * * *" or "0,5,10... * * * *"
    # We will just check for */5 * * * * or similar
    match = re.search(r'^(\*/5|0,5,10,15,20,25,30,35,40,45,50,55)\s+\*\s+\*\s+\*\s+\*\s+(.+)$', content, re.MULTILINE)
    assert match is not None, f"{cron_path} does not contain a valid 5-minute cron schedule."

    command = match.group(2)
    assert "/home/user/run_pipeline.sh" in command, f"Cron command does not execute /home/user/run_pipeline.sh. Found: {command}"