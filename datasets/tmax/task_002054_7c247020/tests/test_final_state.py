# test_final_state.py

import os
import stat
import pytest

def test_restore_area_extracted():
    """Test that the backup archive was extracted to the restore area."""
    config_path = "/home/user/restore_area/etc/app_config.conf"
    assert os.path.isfile(config_path), f"Configuration file not found at {config_path}. Did you extract the archive?"

def test_script_exists_and_executable():
    """Test that the bash script was created and is executable."""
    script_path = "/home/user/bin/rotate_and_test.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script at {script_path} is not executable"

def test_log_rotated():
    """Test that the log file was rotated and truncated."""
    log_gz_path = "/home/user/restore_area/var/log/app/access.log.1.gz"
    log_path = "/home/user/restore_area/var/log/app/access.log"

    assert os.path.isfile(log_gz_path), f"Rotated log file not found at {log_gz_path}"
    assert os.path.isfile(log_path), f"Original log file not found at {log_path}"
    assert os.path.getsize(log_path) == 0, f"Original log file at {log_path} was not truncated (size is not 0)"

def test_summary_report():
    """Test that the summary report matches the expected output."""
    summary_path = "/home/user/restore_summary.txt"
    assert os.path.isfile(summary_path), f"Summary report not found at {summary_path}"

    with open(summary_path, 'r') as f:
        content = f.read().strip()

    expected_lines = [
        "RESTORED_PORT=8443",
        "TLS_CERT_FOUND=true",
        "LOG_ROTATED=true"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    for expected in expected_lines:
        assert expected in actual_lines, f"Expected line '{expected}' not found in {summary_path}"