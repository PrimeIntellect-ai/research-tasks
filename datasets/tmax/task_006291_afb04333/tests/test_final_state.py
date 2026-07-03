# test_final_state.py

import os
import re
import pytest

def test_capacity_log_contents():
    """Check that /home/user/capacity.log contains the expected sequence of events."""
    log_path = "/home/user/capacity.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    assert "SERVICE_STARTED" in content, "SERVICE_STARTED not found in capacity.log."

    # Check for CAPACITY_WARNING with a size > 10000000
    warning_match = re.search(r"CAPACITY_WARNING:\s*(\d+)", content)
    assert warning_match is not None, "CAPACITY_WARNING line not found in capacity.log."
    size = int(warning_match.group(1))
    assert size > 10000000, f"CAPACITY_WARNING size {size} is not greater than 10,000,000."

    assert "BACKUP_SUCCESS" in content, "BACKUP_SUCCESS not found in capacity.log."
    assert "RECOVERY_COMPLETE" in content, "RECOVERY_COMPLETE not found in capacity.log."
    assert "SERVICE_STOPPED" in content, "SERVICE_STOPPED not found in capacity.log."

def test_backup_archive_exists():
    """Check that the backup archive was created."""
    backup_path = "/home/user/backups/app_backup.tar.gz"
    assert os.path.isfile(backup_path), f"Backup archive {backup_path} does not exist."

def test_app_data_cleanup():
    """Check that /home/user/app_data was cleaned up and its total size is < 5MB."""
    app_data_path = "/home/user/app_data"
    assert os.path.isdir(app_data_path), f"Directory {app_data_path} does not exist."

    total_size = 0
    for dirpath, _, filenames in os.walk(app_data_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    assert total_size < 5000000, f"Total size of {app_data_path} is {total_size} bytes, which is not less than 5MB. Cleanup may have failed."