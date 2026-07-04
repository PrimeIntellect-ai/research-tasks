# test_final_state.py

import os
import tarfile
import pytest

def test_c_source_exists():
    """Verify that the C source code file exists."""
    source_path = "/home/user/mail_monitor.c"
    assert os.path.isfile(source_path), f"C source file {source_path} does not exist."

def test_executable_exists():
    """Verify that the compiled executable exists and is executable."""
    exe_path = "/home/user/mail_monitor"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_backup_exists_and_valid():
    """Verify that the backup tarball was created and contains the correct files."""
    backup_path = "/home/user/mail_backup.tar.gz"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} does not exist."

    # Check that it's a valid tar.gz and contains mail_spool directory contents
    try:
        with tarfile.open(backup_path, "r:gz") as tar:
            names = tar.getnames()
            # Check for at least one expected file to ensure structure is correct
            expected_file = "mail_spool/msg_1.eml"
            assert expected_file in names, f"Expected file {expected_file} not found in the backup tarball."
    except tarfile.ReadError:
        pytest.fail(f"File {backup_path} is not a valid gzip-compressed tarball.")

def test_health_status_log():
    """Verify that the health status log exists and has the correct exact output."""
    log_path = "/home/user/health_status.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_content = "STATUS: BACKUP_TRIGGERED, EMAIL_COUNT: 12"
    assert content == expected_content, f"Log file content is incorrect. Expected '{expected_content}', got '{content}'."