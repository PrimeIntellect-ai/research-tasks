# test_final_state.py

import os
import json
import subprocess
import glob
import pytest

def test_cron_job_scheduled():
    """Verify that the cron job is scheduled correctly."""
    try:
        # Check crontab for 'user' (or current user if running as user)
        # We'll just run crontab -l and check the output.
        # Since tests might run as root or user, we check user's crontab.
        result = subprocess.run(["crontab", "-l", "-u", "user"], capture_output=True, text=True)
        if result.returncode != 0:
            # Fallback to current user if -u user fails
            result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    except Exception as e:
        pytest.fail(f"Failed to check crontab: {e}")

    lines = result.stdout.strip().split("\n")
    cron_found = False
    for line in lines:
        if line.startswith("#"):
            continue
        if "15 3 * * *" in line and "/home/user/pipeline/run_daily.sh" in line:
            cron_found = True
            break

    assert cron_found, "Cron job for run_daily.sh at 03:15 AM is missing or incorrectly configured."

def test_validator_clean_corpus():
    """Verify validator accepts clean corpus files."""
    validator_path = "/home/user/pipeline/validator.py"
    assert os.path.isfile(validator_path), f"Missing validator script at {validator_path}"

    clean_files = glob.glob("/app/corpus/clean/*")
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []
    for f in clean_files:
        result = subprocess.run(["python3", validator_path, f], capture_output=True, text=True)
        if result.returncode != 0 or "ACCEPTED" not in result.stdout.upper():
            failed_files.append(os.path.basename(f))

    assert len(failed_files) == 0, f"{len(failed_files)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_files)}"

def test_validator_evil_corpus():
    """Verify validator rejects evil corpus files."""
    validator_path = "/home/user/pipeline/validator.py"
    assert os.path.isfile(validator_path), f"Missing validator script at {validator_path}"

    evil_files = glob.glob("/app/corpus/evil/*")
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []
    for f in evil_files:
        result = subprocess.run(["python3", validator_path, f], capture_output=True, text=True)
        if result.returncode != 1 or "REJECTED" not in result.stdout.upper():
            failed_files.append(os.path.basename(f))

    assert len(failed_files) == 0, f"{len(failed_files)} of {len(evil_files)} evil bypassed: {', '.join(failed_files)}"

def test_run_daily_and_process():
    """Verify run_daily.sh runs process.py and gap-fills correctly."""
    run_daily_path = "/home/user/pipeline/run_daily.sh"
    assert os.path.isfile(run_daily_path), f"Missing run_daily.sh at {run_daily_path}"
    assert os.access(run_daily_path, os.X_OK), f"run_daily.sh is not executable."

    # Ensure incoming data is in place before running
    incoming_data = "/home/user/incoming/data.jsonl"
    assert os.path.isfile(incoming_data), f"Missing incoming data at {incoming_data}"

    # Execute run_daily.sh
    result = subprocess.run(["bash", run_daily_path], capture_output=True, text=True)
    assert result.returncode == 0, f"run_daily.sh failed with exit code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

    processed_file = "/home/user/processed/cleaned.jsonl"
    assert os.path.isfile(processed_file), f"Processed file not found at {processed_file}"

    with open(processed_file, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, "Processed file is empty."

    try:
        data = json.loads(lines[0].strip())
    except json.JSONDecodeError:
        pytest.fail("Processed file does not contain valid JSON.")

    assert "duration_sec" in data, "Missing 'duration_sec' in processed JSON."
    assert data["duration_sec"] == 3.45, f"Expected duration_sec to be 3.45, got {data['duration_sec']}"