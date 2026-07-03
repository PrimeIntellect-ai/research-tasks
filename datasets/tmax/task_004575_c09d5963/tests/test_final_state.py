# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/extract_errors.py"
LOG_PATH = "/home/user/service.log"
STATE_PATH = "/home/user/backup.state"
ARCHIVE_PATH = "/home/user/error_archive.log"

EXPECTED_FIRST_ERROR = (
    "[2023-10-25 10:05:00] ERROR Connection timeout\n"
    "Traceback (most recent call last):\n"
    "  File \"main.py\", line 10, in <module>\n"
    "TimeoutError: db unreachable\n"
)

NEW_LOG_DATA = (
    "[2023-10-25 10:10:00] INFO User logged in\n"
    "[2023-10-25 10:15:00] ERROR NullPointerException\n"
    "  at com.example.App.main(App.java:15)\n"
    "  at java.base/java.lang.Thread.run\n"
    "[2023-10-25 10:16:00] INFO Shutdown\n"
)

EXPECTED_SECOND_ERROR = (
    "[2023-10-25 10:15:00] ERROR NullPointerException\n"
    "  at com.example.App.main(App.java:15)\n"
    "  at java.base/java.lang.Thread.run\n"
)

def test_script_exists_and_uses_required_modules():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()

    assert "fcntl" in content, "Script does not import or use fcntl."
    assert "flock" in content, "Script does not use fcntl.flock."
    assert "mmap" in content, "Script does not import or use mmap."

def test_initial_run_results():
    assert os.path.isfile(STATE_PATH), f"State file {STATE_PATH} does not exist."
    assert os.path.isfile(ARCHIVE_PATH), f"Archive file {ARCHIVE_PATH} does not exist."

    with open(LOG_PATH, "rb") as f:
        log_size = len(f.read())

    with open(STATE_PATH, "r") as f:
        state_val = f.read().strip()

    assert state_val == str(log_size), f"Expected state to be {log_size}, got {state_val}"

    with open(ARCHIVE_PATH, "r") as f:
        archive_content = f.read()

    assert archive_content == EXPECTED_FIRST_ERROR, "Initial error archive content does not match expected."

def test_incremental_run_results():
    # Append new data
    with open(LOG_PATH, "a") as f:
        f.write(NEW_LOG_DATA)

    with open(LOG_PATH, "rb") as f:
        new_log_size = len(f.read())

    # Run the script
    result = subprocess.run(["python3", SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed on incremental run:\n{result.stderr}"

    # Verify state
    with open(STATE_PATH, "r") as f:
        state_val = f.read().strip()

    assert state_val == str(new_log_size), f"Expected state to be {new_log_size} after incremental run, got {state_val}"

    # Verify archive
    with open(ARCHIVE_PATH, "r") as f:
        archive_content = f.read()

    expected_full_archive = EXPECTED_FIRST_ERROR + EXPECTED_SECOND_ERROR
    assert archive_content == expected_full_archive, "Error archive content does not match expected after incremental run."