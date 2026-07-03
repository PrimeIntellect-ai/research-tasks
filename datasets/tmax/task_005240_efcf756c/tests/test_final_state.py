# test_final_state.py

import os
import re
import subprocess
import pytest

def test_process_logs_script_exists():
    script_path = "/home/user/process_logs.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_merged_data_csv_content():
    output_path = "/home/user/output/merged_data.csv"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    expected_content = (
        "minute_timestamp,event_id,action_token,avg_cpu,avg_ram\n"
        "2023-10-15 14:32:00,1,restart,87.8,60.6\n"
        "2023-10-15 14:32:00,2,warning,87.8,60.6\n"
        "2023-10-15 14:33:00,3,deploying,75.0,65.5\n"
        "2023-10-15 14:35:00,4,crash,20.5,40.0"
    )

    with open(output_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content.strip(), (
        f"The content of {output_path} does not match the expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )

def test_etl_log_content():
    log_path = "/home/user/logs/etl.log"
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist."

    with open(log_path, "r") as f:
        log_content = f.read().strip()

    lines = log_content.split("\n")
    assert len(lines) > 0, "The log file is empty."

    last_line = lines[-1]
    # Expecting format: [YYYY-MM-DD HH:MM:SS] SUCCESS: Processed 4 events
    match = re.search(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] SUCCESS: Processed 4 events", last_line)

    assert match is not None, (
        f"The log file does not contain the correct success message in the last line.\n"
        f"Last line found: {last_line}"
    )

def test_cron_job_configured():
    try:
        result = subprocess.run(
            ["crontab", "-l", "-u", "user"],
            capture_output=True,
            text=True,
            check=True
        )
        crontab_output = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to retrieve crontab for user 'user'. Make sure the cron job is installed.")

    # Check for */15 * * * * and process_logs.py
    cron_lines = [line.strip() for line in crontab_output.split("\n") if line.strip() and not line.strip().startswith("#")]

    found_cron = False
    for line in cron_lines:
        if "*/15 * * * *" in line and "process_logs.py" in line:
            found_cron = True
            break

    assert found_cron, (
        "Could not find the expected cron job for user 'user'.\n"
        "Expected schedule: */15 * * * *\n"
        "Expected script: process_logs.py\n"
        f"Current crontab:\n{crontab_output}"
    )