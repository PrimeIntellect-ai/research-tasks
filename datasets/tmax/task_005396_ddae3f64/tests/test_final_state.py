# test_final_state.py

import os
import re
import subprocess
import pytest

def test_process_script_exists_and_executable():
    script_path = '/home/user/process.sh'
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_summary_report_content():
    report_path = '/home/user/reports/summary.txt'
    assert os.path.isfile(report_path), f"The report {report_path} does not exist."

    with open(report_path, 'r') as f:
        content = f.read().strip()

    expected_content = """Daily Feedback Report
Most frequent words:
1. quality (5)
2. product (4)
3. fantastic (3)"""

    assert content == expected_content, f"The content of {report_path} does not match the expected output."

def test_pipeline_log_format():
    log_path = '/home/user/logs/pipeline.log'
    assert os.path.isfile(log_path), f"The log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) > 0, f"The log file {log_path} is empty."

    # Check the last line for the expected format
    last_line = lines[-1].strip()
    pattern = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Pipeline completed successfully\.$"
    assert re.match(pattern, last_line), f"The log entry format is incorrect: {last_line}"

def test_crontab_entry():
    try:
        result = subprocess.run(['crontab', '-l', '-u', 'user'], capture_output=True, text=True, check=True)
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to retrieve crontab for 'user'.")

    # Look for the specific cron entry, allowing for multiple spaces/tabs
    pattern = r"^0\s+2\s+\*\s+\*\s+\*\s+/home/user/process\.sh"

    match_found = any(re.match(pattern, line.strip()) for line in crontab_content.splitlines())
    assert match_found, "The crontab for 'user' does not contain the correct schedule for /home/user/process.sh."