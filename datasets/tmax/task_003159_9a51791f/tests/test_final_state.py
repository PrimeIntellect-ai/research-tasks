# test_final_state.py

import os
import subprocess
import pytest
import re

def test_run_job_script_exists_and_executable():
    script_path = "/home/user/pipeline/run_job.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_c_program_exists():
    c_path = "/home/user/pipeline/process_sensor.c"
    assert os.path.isfile(c_path), f"C source file {c_path} does not exist."

def test_pipeline_execution_and_results():
    script_path = "/home/user/pipeline/run_job.sh"
    log_path = "/home/user/pipeline/results.log"

    # Execute the script
    result = subprocess.run([script_path], cwd="/home/user/pipeline", capture_output=True, text=True)
    assert result.returncode == 0, f"run_job.sh failed with return code {result.returncode}\nstderr: {result.stderr}"

    # Check if results.log was created/appended
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    with open(log_path, "r") as f:
        content = f.read()

    expected_line = "Records: 5, AvgTemp: 31.74, Anomalies: 2"
    assert expected_line in content, f"Expected output '{expected_line}' not found in {log_path}. Content:\n{content}"

def test_cron_job_scheduled():
    # Check crontab for user 'user'
    result = subprocess.run(["crontab", "-l", "-u", "user"], capture_output=True, text=True)

    # If the user has no crontab, it might return non-zero, but we expect a crontab to exist
    assert result.returncode == 0, "No crontab found for user 'user'."

    cron_output = result.stdout.strip()

    # Look for 15 3 * * * and run_job.sh
    # Standard cron format: 15 3 * * * /home/user/pipeline/run_job.sh
    match = re.search(r'^15\s+3\s+\*\s+\*\s+\*\s+.*run_job\.sh', cron_output, re.MULTILINE)
    assert match is not None, f"Cron job for 3:15 AM running run_job.sh not found in crontab. Crontab content:\n{cron_output}"