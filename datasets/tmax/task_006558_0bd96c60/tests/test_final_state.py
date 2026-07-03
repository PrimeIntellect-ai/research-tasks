# test_final_state.py

import os
import stat
import subprocess
import pytest

SCRIPT_PATH = "/home/user/process_drift.sh"
OUTPUT_PATH = "/home/user/top_drifts.txt"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_script_execution_and_output():
    # Remove output file if it exists to ensure we are testing the script's execution
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)

    # Run the script
    result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

    # Check if output file was created
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} was not created by the script."

    with open(OUTPUT_PATH, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "PaymentSvc:16.5",
        "InventorySvc:13.5",
        "CacheSvc:12.5"
    ]

    assert len(lines) == 3, f"Expected exactly 3 lines in {OUTPUT_PATH}, got {len(lines)}"

    for i, expected in enumerate(expected_lines):
        assert lines[i] == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{lines[i]}'"

def test_cron_job_scheduled():
    # Check the crontab for 'user'
    result = subprocess.run(['crontab', '-l', '-u', 'user'], capture_output=True, text=True)

    # If the user has no crontab, returncode might be non-zero (e.g., 1)
    # We just check if the expected cron expression is in the stdout
    stdout = result.stdout.strip()

    # Normalize whitespace for comparison
    cron_lines = [line.strip() for line in stdout.split('\n') if line.strip() and not line.strip().startswith('#')]

    expected_cron_command = "/home/user/process_drift.sh"

    found = False
    for line in cron_lines:
        parts = line.split()
        if len(parts) >= 6:
            schedule = " ".join(parts[:5])
            command = " ".join(parts[5:])
            if schedule == "0 2 * * *" and expected_cron_command in command:
                found = True
                break

    assert found, "Cron job '0 2 * * * /home/user/process_drift.sh' not found for user 'user'."