# test_final_state.py
import os
import subprocess
import pytest

def test_processed_sensors_csv():
    file_path = '/home/user/processed_sensors.csv'
    assert os.path.exists(file_path), f"File {file_path} is missing."

    expected_lines = [
        "2023-10-01 10:05:00,Café_Front,22.5",
        "2023-10-01 11:25:00,Café_Back,24.1",
        "2023-10-01 12:55:00,Café_Ext,-10.0"
    ]

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip().split('\n')

    # Filter out empty lines if any
    content = [line.strip() for line in content if line.strip()]

    # The file is appended to, so we check if the expected lines are at the end
    # or just check if they are present in the correct order.
    # Given the instructions "Please execute the script once manually", it might just have these 3 lines.
    assert content[-3:] == expected_lines, f"The processed data in {file_path} does not match the expected output. Got: {content[-3:]}"

def test_etl_log():
    file_path = '/home/user/etl.log'
    assert os.path.exists(file_path), f"File {file_path} is missing."

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')

    lines = [line.strip() for line in lines if line.strip()]
    assert len(lines) > 0, f"Log file {file_path} is empty."

    expected_log = "SUCCESS: Extracted 3 samples."
    assert lines[-1] == expected_log, f"The last line of {file_path} does not match the expected log. Got: {lines[-1]}"

def test_cron_job():
    try:
        result = subprocess.run(['crontab', '-l', '-u', 'user'], capture_output=True, text=True, check=True)
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        # Fallback to reading the spool file directly
        spool_path = '/var/spool/cron/crontabs/user'
        assert os.path.exists(spool_path), "Crontab for user 'user' not found."
        with open(spool_path, 'r') as f:
            crontab_content = f.read()

    # Check for the schedule and command
    expected_command = "/usr/local/go/bin/go run /home/user/etl.go"

    found = False
    for line in crontab_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('*/15 * * * *') and expected_command in line:
            found = True
            break

    assert found, f"Crontab for 'user' does not contain the expected cron job. Crontab content:\n{crontab_content}"

def test_etl_go_script_exists():
    file_path = '/home/user/etl.go'
    assert os.path.exists(file_path), f"Go script {file_path} is missing."