# test_final_state.py

import os
import json
import pytest

def test_script_exists():
    script_path = "/home/user/verify_restores.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

def test_summary_json_exists_and_correct():
    summary_path = "/home/user/summary.json"
    assert os.path.isfile(summary_path), f"Summary file {summary_path} does not exist."

    with open(summary_path, 'r') as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {summary_path} is not valid JSON.")

    expected_summary = {
        "/": 3,
        "/var/www": 3,
        "/opt/app/backup": 3
    }

    assert summary == expected_summary, f"Summary JSON content is incorrect. Expected {expected_summary}, got {summary}."

def test_log_files_exist():
    logs_dir = "/home/user/logs"

    # Check for /
    assert os.path.isfile(os.path.join(logs_dir, "_.log")), "Log file for '/' missing."
    assert os.path.isfile(os.path.join(logs_dir, "_.log.1")), "Rotated log file 1 for '/' missing."
    assert os.path.isfile(os.path.join(logs_dir, "_.log.2")), "Rotated log file 2 for '/' missing."

    # Check for /var/www
    assert os.path.isfile(os.path.join(logs_dir, "_var_www.log")), "Log file for '/var/www' missing."
    assert os.path.isfile(os.path.join(logs_dir, "_var_www.log.1")), "Rotated log file 1 for '/var/www' missing."
    assert os.path.isfile(os.path.join(logs_dir, "_var_www.log.2")), "Rotated log file 2 for '/var/www' missing."

    # Check for /opt/app/backup
    assert os.path.isfile(os.path.join(logs_dir, "_opt_app_backup.log")), "Log file for '/opt/app/backup' missing."
    assert os.path.isfile(os.path.join(logs_dir, "_opt_app_backup.log.1")), "Rotated log file 1 for '/opt/app/backup' missing."
    assert os.path.isfile(os.path.join(logs_dir, "_opt_app_backup.log.2")), "Rotated log file 2 for '/opt/app/backup' missing."

def test_log_file_contents():
    logs_dir = "/home/user/logs"

    # Check content of one of the log files to ensure correct format
    root_log = os.path.join(logs_dir, "_.log")
    if os.path.isfile(root_log):
        with open(root_log, 'r') as f:
            content = f.read()
            assert "VERIFIED: /" in content, f"Log file {root_log} does not contain expected message format."
            assert "INFO" not in content, f"Log file {root_log} should not contain log levels."