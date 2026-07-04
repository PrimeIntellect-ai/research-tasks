# test_final_state.py

import os
import tarfile
import pytest

APP_LOGS_DIR = "/home/user/app_logs"
OLD_LOG = os.path.join(APP_LOGS_DIR, "log_old.txt")
RECENT_LOG1 = os.path.join(APP_LOGS_DIR, "log_recent1.txt")
RECENT_LOG2 = os.path.join(APP_LOGS_DIR, "log_recent2.txt")
ERROR_SUMMARY = "/home/user/error_summary.txt"
ARCHIVE_PATH = "/home/user/processed_logs.tar.gz"

def test_old_log_untouched():
    """Verify that log_old.txt was not modified and still contains [TRACE] lines."""
    assert os.path.isfile(OLD_LOG), f"Old log file {OLD_LOG} is missing."
    with open(OLD_LOG, "r") as f:
        content = f.read()
    assert "[TRACE]" in content, f"Old log file {OLD_LOG} should not have been modified and should still contain [TRACE]."

def test_recent_logs_cleaned():
    """Verify that recent log files have [TRACE] lines removed."""
    for log_path in [RECENT_LOG1, RECENT_LOG2]:
        assert os.path.isfile(log_path), f"Recent log file {log_path} is missing."
        with open(log_path, "r") as f:
            content = f.read()
        assert "[TRACE]" not in content, f"Recent log file {log_path} still contains [TRACE] lines."

def test_error_summary_contents():
    """Verify that error_summary.txt contains correct [ERROR] lines from recent logs only."""
    assert os.path.isfile(ERROR_SUMMARY), f"Error summary file {ERROR_SUMMARY} is missing."
    with open(ERROR_SUMMARY, "r") as f:
        content = f.read()

    assert "[ERROR] Memory limit exceeded" in content, "Error summary is missing '[ERROR] Memory limit exceeded'."
    assert "[ERROR] GC failed" in content, "Error summary is missing '[ERROR] GC failed'."
    assert "Module A failed" not in content, "Error summary incorrectly contains errors from the old log."

def test_archive_contents():
    """Verify that processed_logs.tar.gz contains the correct files."""
    assert os.path.isfile(ARCHIVE_PATH), f"Archive file {ARCHIVE_PATH} is missing."

    with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
        names = tar.getnames()

        # We need to check if the recent logs are in the archive, ignoring directory prefixes
        base_names = [os.path.basename(name) for name in names]

        assert "log_recent1.txt" in base_names, "log_recent1.txt is missing from the archive."
        assert "log_recent2.txt" in base_names, "log_recent2.txt is missing from the archive."
        assert "log_old.txt" not in base_names, "log_old.txt should not be in the archive."

        # Ensure no absolute paths are used
        for name in names:
            assert not name.startswith("/"), f"Archive contains absolute path: {name}"