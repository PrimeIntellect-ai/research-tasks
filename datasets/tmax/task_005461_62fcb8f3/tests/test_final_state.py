# test_final_state.py

import os
import subprocess
import re

def test_script_exists_and_executable():
    script_path = "/home/user/restore_test.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_restored_data():
    data_path = "/home/user/restored_data/data.txt"
    assert os.path.isfile(data_path), f"Restored data file {data_path} does not exist."
    with open(data_path, "r") as f:
        content = f.read().strip()
    assert content == "Database dump successful", f"Unexpected content in {data_path}: {content}"

def test_restore_report():
    report_path = "/home/user/restore_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist."

    with open(report_path, "r") as f:
        content = f.read().strip().split('\n')

    expected_lines = [
        "[2023-07-01 09:00:00] Primary db synced",
        "[2023-07-02 09:00:00] Secondary db synced"
    ]

    for expected in expected_lines:
        assert expected in content, f"Expected line '{expected}' not found in {report_path}."

def test_crontab_scheduled():
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        crontab_output = result.stdout
    except subprocess.CalledProcessError:
        assert False, "Failed to read crontab or no crontab exists."

    # Look for a line that schedules the script at 3:00 AM daily
    # Cron syntax: 0 3 * * * /home/user/restore_test.sh
    match = re.search(r'^0\s+3\s+\*\s+\*\s+\*\s+.*?/home/user/restore_test\.sh', crontab_output, re.MULTILINE)
    assert match is not None, "Crontab does not contain the correct schedule for /home/user/restore_test.sh at 3:00 AM."

def test_script_idempotency():
    script_path = "/home/user/restore_test.sh"
    report_path = "/home/user/restore_report.txt"

    # Read report before second run
    with open(report_path, "r") as f:
        before_content = f.read()

    # Run the script again
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed on subsequent run (not idempotent). Error: {result.stderr}"

    # Read report after second run
    with open(report_path, "r") as f:
        after_content = f.read()

    assert before_content == after_content, "Report file content changed on subsequent run, script is not idempotent."