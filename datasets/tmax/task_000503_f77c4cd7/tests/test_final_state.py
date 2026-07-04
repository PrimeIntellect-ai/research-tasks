# test_final_state.py

import os
import re
import stat
import subprocess
import glob
import pytest

SCRIPT_PATH = "/home/user/rotate_and_summarize.py"
DATA_LOG = "/home/user/app/data.log"
ERROR_SUMMARY = "/home/user/app/error_summary.log"
ARCHIVE_DIR = "/home/user/app/archive"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_crontab_entry():
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        crontab_output = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Ensure crontab is set up for the user.")

    # Looking for: 0 0 * * * /usr/bin/python3 /home/user/rotate_and_summarize.py
    pattern = re.compile(r"^0\s+0\s+\*\s+\*\s+\*\s+/usr/bin/python3\s+/home/user/rotate_and_summarize\.py$", re.MULTILINE)
    assert pattern.search(crontab_output), "Crontab entry is missing or incorrect. Expected '0 0 * * * /usr/bin/python3 /home/user/rotate_and_summarize.py'."

def test_script_execution():
    # Setup expected initial state for the test
    original_content = (
        "INFO: Application started\n"
        "ERROR: Connection timeout on port 8080\n"
        "DEBUG: Memory usage at 45%\n"
        "ERROR: Disk space low on /dev/sda1\n"
        "INFO: Shutting down\n"
    )

    # Ensure data.log is in the state it should be before rotation
    with open(DATA_LOG, "w") as f:
        f.write(original_content)

    # Clear archive dir to ensure we can easily find the new archive
    for f in glob.glob(os.path.join(ARCHIVE_DIR, "data_*.log")):
        os.remove(f)

    # Remove error_summary.log if it exists so we can verify the append
    if os.path.exists(ERROR_SUMMARY):
        os.remove(ERROR_SUMMARY)

    # Execute the script
    result = subprocess.run(["/usr/bin/python3", SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with output: {result.stderr}"

    # 1. data.log must exist and be exactly 0 bytes
    assert os.path.isfile(DATA_LOG), f"{DATA_LOG} does not exist after script execution."
    assert os.path.getsize(DATA_LOG) == 0, f"{DATA_LOG} is not 0 bytes after script execution."

    # 2. error_summary.log must contain exactly the ERROR lines
    expected_error_content = (
        "ERROR: Connection timeout on port 8080\n"
        "ERROR: Disk space low on /dev/sda1\n"
    )
    assert os.path.isfile(ERROR_SUMMARY), f"{ERROR_SUMMARY} does not exist."
    with open(ERROR_SUMMARY, "r") as f:
        error_content = f.read()
    assert error_content == expected_error_content, f"Content of {ERROR_SUMMARY} does not match expected ERROR lines."

    # 3. Archive file must exist and contain the original 5 lines
    archive_files = glob.glob(os.path.join(ARCHIVE_DIR, "data_[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]_[0-9][0-9][0-9][0-9][0-9][0-9].log"))
    assert len(archive_files) == 1, "Expected exactly one rotated archive file matching the pattern data_YYYYMMDD_HHMMSS.log."

    with open(archive_files[0], "r") as f:
        archived_content = f.read()
    assert archived_content == original_content, "Archived file content does not match the original data.log content."

def test_script_execution_empty_file():
    # Ensure data.log is 0 bytes
    with open(DATA_LOG, "w") as f:
        pass

    # Record current archive files
    archive_files_before = glob.glob(os.path.join(ARCHIVE_DIR, "data_*.log"))

    # Execute the script again
    result = subprocess.run(["/usr/bin/python3", SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed on empty file with output: {result.stderr}"

    # Verify no new archive file was created
    archive_files_after = glob.glob(os.path.join(ARCHIVE_DIR, "data_*.log"))
    assert len(archive_files_after) == len(archive_files_before), "Script should not rotate an empty log file."