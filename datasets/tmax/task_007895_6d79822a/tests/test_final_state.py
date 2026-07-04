# test_final_state.py

import os
import stat
import re
from datetime import datetime
import pytest

def test_secure_backup_permissions():
    """Verify /home/user/secure_backup/ has exactly 750 permissions."""
    path = "/home/user/secure_backup"
    assert os.path.isdir(path), f"Directory {path} does not exist."
    mode = stat.S_IMODE(os.stat(path).st_mode)
    assert oct(mode) == '0o750', f"Permissions for {path} are {oct(mode)}, expected 0o750."

def test_archive_contents():
    """Verify archive.txt contains the correct data appended 10 times."""
    path = "/home/user/secure_backup/archive.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read()

    expected_line = "critical system data\n"
    expected_content = expected_line * 10

    # Allow for potentially missing trailing newline or extra newlines
    assert content.strip() == expected_content.strip(), f"Content of {path} does not match expected 10 appends."
    lines = [line for line in content.split('\n') if line]
    assert len(lines) == 10, f"Expected 10 lines in {path}, found {len(lines)}."

def test_log_rotation_files():
    """Verify that backup.log and its rotated versions exist."""
    base_log = "/home/user/app_logs/backup.log"
    assert os.path.isfile(base_log), f"Log file {base_log} does not exist."

    for i in range(1, 4):
        rotated_log = f"{base_log}.{i}"
        assert os.path.isfile(rotated_log), f"Rotated log file {rotated_log} does not exist."

        # Check size limit constraint (maxBytes=60 means it should be around that or less)
        size = os.path.getsize(rotated_log)
        assert size > 0, f"Rotated log {rotated_log} is empty."
        # A single log line is around 40-50 bytes. 
        # "2023-10-10 10:10:10,123 - Backup successful\n" is ~45 bytes.
        # Two lines would be ~90 bytes, which exceeds 60, triggering rotation.
        # So rotated logs should typically be around 40-55 bytes.
        assert size < 100, f"Rotated log {rotated_log} size {size} is too large for maxBytes=60."

def test_log_content_and_format():
    """Verify log format and content in the oldest log."""
    oldest_log = "/home/user/app_logs/backup.log.3"
    assert os.path.isfile(oldest_log), f"Oldest log {oldest_log} missing."

    with open(oldest_log, 'r') as f:
        content = f.read().strip()

    lines = content.split('\n')
    assert len(lines) > 0, "Log file is empty."

    # Format: %(asctime)s - %(message)s
    # Example: 2023-10-25 12:34:56,789 - Backup successful
    pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - Backup successful$"
    for line in lines:
        assert re.match(pattern, line), f"Log line '{line}' does not match expected format."

def test_final_listing_artifact():
    """Verify the final_listing.txt artifact exists and contains app_logs listing."""
    path = "/home/user/final_listing.txt"
    assert os.path.isfile(path), f"Artifact {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    assert "backup.log" in content, "final_listing.txt does not contain backup.log"
    assert "backup.log.1" in content, "final_listing.txt does not contain backup.log.1"