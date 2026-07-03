# test_final_state.py

import os
import subprocess
import pytest
import re

def test_run_tester_script_exists_and_executable():
    script_path = "/home/user/run_tester.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_run_tester_execution_and_results():
    script_path = "/home/user/run_tester.sh"
    log_path = "/home/user/restore_results.log"

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)

    # Check if build failed
    if result.returncode != 0:
        if os.path.isfile(log_path):
            with open(log_path, 'r') as f:
                content = f.read().strip()
                if content == "BUILD_FAILED":
                    pytest.fail("Go build failed as indicated by BUILD_FAILED in restore_results.log.")
        pytest.fail(f"{script_path} failed with exit code {result.returncode}. Output: {result.stderr}")

    assert os.path.isfile(log_path), f"{log_path} was not created."

    with open(log_path, 'r') as f:
        log_contents = f.read().strip().splitlines()

    expected_lines = [
        "backup_a.tar.gz,SUCCESS",
        "backup_b.tar.gz,FAILED",
        "backup_c.tar.gz,FAILED"
    ]

    assert log_contents == expected_lines, f"Contents of {log_path} do not match expected results. Got: {log_contents}"

def test_tmp_restore_cleaned_up():
    tmp_dir = "/home/user/tmp_restore"
    assert not os.path.exists(tmp_dir), f"Temporary directory {tmp_dir} was not cleaned up."

def test_cron_conf():
    cron_path = "/home/user/cron.conf"
    assert os.path.isfile(cron_path), f"{cron_path} does not exist."

    with open(cron_path, 'r') as f:
        content = f.read().strip()

    # Basic check for crontab format scheduling /home/user/run_tester.sh every 15 mins
    # Matches */15 or 0,15,30,45 in the first field, followed by * for the next 4 fields
    pattern = r"^(?:\*/15|0,15,30,45)\s+\*\s+\*\s+\*\s+\*\s+/home/user/run_tester\.sh$"

    match = False
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if re.match(pattern, line):
            match = True
            break

    assert match, f"{cron_path} does not contain a valid cron expression for running /home/user/run_tester.sh every 15 minutes."