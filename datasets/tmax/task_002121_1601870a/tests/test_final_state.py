# test_final_state.py

import os
import subprocess
import pytest

def test_compiled_binary():
    binary_path = "/home/user/secure_archiver"
    assert os.path.isfile(binary_path), f"Compiled binary missing at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable"

def test_vault_contents():
    expected_vault_files = [
        "/home/user/vault/reports/file1.txt",
        "/home/user/vault/images/file2.txt",
        "/home/user/vault/deep/nested/path/file3.txt"
    ]
    for path in expected_vault_files:
        assert os.path.isfile(path), f"Expected moved file is missing in vault: {path}"

def test_staging_contents():
    # Evil files should remain in staging
    expected_staging_files = [
        "/home/user/staging/evil1.txt",
        "/home/user/staging/evil2.txt"
    ]
    for path in expected_staging_files:
        assert os.path.isfile(path), f"Blocked file should still be in staging: {path}"

    # Moved files should NOT be in staging
    unexpected_staging_files = [
        "/home/user/staging/file1.txt",
        "/home/user/staging/file2.txt",
        "/home/user/staging/file3.txt"
    ]
    for path in unexpected_staging_files:
        assert not os.path.exists(path), f"File should have been moved out of staging: {path}"

def test_security_log():
    log_path = "/home/user/security.log"
    assert os.path.isfile(log_path), f"Security log missing at {log_path}"

    with open(log_path, "r") as f:
        log_contents = f.read().splitlines()

    expected_lines = [
        "[MOVED] file1.txt -> /home/user/vault/reports/file1.txt",
        "[MOVED] file2.txt -> /home/user/vault/images/file2.txt",
        "[BLOCKED] evil1.txt -> ../../user/evil1.txt",
        "[MOVED] file3.txt -> /home/user/vault/deep/nested/path/file3.txt",
        "[BLOCKED] evil2.txt -> /etc/passwd_copy"
    ]

    for expected_line in expected_lines:
        assert expected_line in log_contents, f"Expected log entry missing: {expected_line}"

def test_map_file_cleaned_up():
    assert not os.path.exists("/home/user/spool/test_batch.map"), "Processed map file was not deleted from spool directory."
    assert not os.path.exists("/home/user/test_batch.map"), "Map file was not moved into spool directory."

def test_daemon_exited():
    try:
        # Check if any secure_archiver process is still running
        output = subprocess.check_output(["pgrep", "-f", "secure_archiver"]).decode("utf-8")
        # If pgrep finds something, it will return the PID(s)
        if output.strip():
            pytest.fail("secure_archiver daemon is still running, did not exit on SHUTDOWN.")
    except subprocess.CalledProcessError:
        # pgrep returns non-zero exit code if no processes are matched, which is the expected behavior here
        pass