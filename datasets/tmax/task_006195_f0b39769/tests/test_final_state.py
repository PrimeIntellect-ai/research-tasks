# test_final_state.py
import os
import subprocess
import time
import pytest

START_SERVICES_SCRIPT = "/home/user/start_services.py"
MIGRATION_LOG = "/home/user/migration.log"
EXPECTED_LOG_CONTENT = "STATUS: [SUCCESS] VM state exported"

def test_start_services_script_exists():
    """Test that the start_services.py script exists."""
    assert os.path.isfile(START_SERVICES_SCRIPT), f"Missing file: {START_SERVICES_SCRIPT}"

def test_migration_log_exists_and_correct():
    """Test that the migration.log exists and contains the correct status."""
    assert os.path.isfile(MIGRATION_LOG), f"Missing file: {MIGRATION_LOG}. The script may not have been run or failed to create the log."
    with open(MIGRATION_LOG, "r") as f:
        content = f.read().strip()
    assert EXPECTED_LOG_CONTENT in content, f"Log content incorrect. Expected to find '{EXPECTED_LOG_CONTENT}' in {MIGRATION_LOG}"

def test_idempotency():
    """Test that the script is idempotent and exits quickly if the log already indicates success."""
    # Ensure the log is in the success state
    with open(MIGRATION_LOG, "w") as f:
        f.write(EXPECTED_LOG_CONTENT + "\n")

    start_time = time.time()
    result = subprocess.run(
        ["python3", START_SERVICES_SCRIPT],
        capture_output=True,
        text=True
    )
    duration = time.time() - start_time

    assert result.returncode == 0, f"Script failed during idempotency check. Stderr: {result.stderr}"
    assert duration < 1.0, "Script took too long during idempotency check. It should exit immediately."

def test_full_execution():
    """Test that the script properly supervises the process when the log is missing."""
    if os.path.exists(MIGRATION_LOG):
        os.remove(MIGRATION_LOG)

    start_time = time.time()
    result = subprocess.run(
        ["python3", START_SERVICES_SCRIPT],
        capture_output=True,
        text=True
    )
    duration = time.time() - start_time

    assert result.returncode == 0, f"Script failed during full execution. Stderr: {result.stderr}"
    assert duration >= 2.0, "Script finished too quickly. It must wait for the VNC server to initialize before sending the command."

    assert os.path.isfile(MIGRATION_LOG), "Script failed to create migration.log after full execution."
    with open(MIGRATION_LOG, "r") as f:
        content = f.read().strip()
    assert EXPECTED_LOG_CONTENT in content, f"Log content incorrect after full execution. Expected to find '{EXPECTED_LOG_CONTENT}'"