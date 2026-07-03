# test_final_state.py

import os
import re
import subprocess
import csv
import pytest

def test_run_pipeline_sh_executable():
    script_path = '/home/user/run_pipeline.sh'
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_cron_job_installed():
    try:
        # Check crontab for user 'user'
        result = subprocess.run(['crontab', '-l', '-u', 'user'], capture_output=True, text=True, check=True)
        crontab_output = result.stdout
    except subprocess.CalledProcessError as e:
        # Fallback to checking the crontab file directly if command fails
        cron_file = '/var/spool/cron/crontabs/user'
        if os.path.isfile(cron_file):
            with open(cron_file, 'r') as f:
                crontab_output = f.read()
        else:
            pytest.fail("Failed to retrieve crontab for 'user' and cron file does not exist.")

    # We look for the schedule: 30 2 * * * /home/user/run_pipeline.sh
    # Allow multiple spaces or tabs
    pattern = r"30\s+2\s+\*\s+\*\s+\*\s+/home/user/run_pipeline\.sh"
    assert re.search(pattern, crontab_output), "The required cron job is not installed or incorrectly formatted."

def test_clean_merged_csv_content():
    output_file = '/home/user/output/clean_merged.csv'
    assert os.path.isfile(output_file), f"The output file {output_file} does not exist."

    expected_data = [
        ['id', 'name', 'email', 'join_date', 'activity_count'],
        ['1', 'Alice Smith', 'alice@example.com', '2023-01-15', '2'],
        ['2', 'Bob Jones', 'bob@example.com', '2022-12-31', '1'],
        ['3', 'Carol White', 'carol@example.org', '2023-02-01', '0'],
        ['5', 'Dave Brown', 'dave.brown@example.com', '2021-10-10', '1'],
        ['6', 'Eve Black', 'eve@example.com', '2023-03-05', '3']
    ]

    with open(output_file, 'r', newline='') as f:
        reader = csv.reader(f)
        actual_data = list(reader)

    assert actual_data == expected_data, "The contents of clean_merged.csv do not match the expected normalized, deduplicated, and merged data."

def test_pipeline_log_format():
    log_file = '/home/user/pipeline.log'
    assert os.path.isfile(log_file), f"The log file {log_file} does not exist."

    with open(log_file, 'r') as f:
        lines = f.readlines()

    assert len(lines) > 0, f"The log file {log_file} is empty."

    # Look for the required log pattern in the last few lines
    pattern = re.compile(r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] SUCCESS: Processed 5 unique users\.$")

    match_found = any(pattern.match(line.strip()) for line in lines)
    assert match_found, "The expected success log line was not found in pipeline.log or did not match the required format."