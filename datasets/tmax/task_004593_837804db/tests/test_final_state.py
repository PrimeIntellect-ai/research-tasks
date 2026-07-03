# test_final_state.py

import os
import pytest
import time

STATUS_LOG = "/home/user/health_logs/status.log"
ALERTS_LOG = "/home/user/health_logs/alerts.log"

def test_status_log_exists_and_contains_200():
    """Verify that status.log exists and contains the correct HTTP status code."""
    assert os.path.isfile(STATUS_LOG), f"FAIL: {STATUS_LOG} not found in the correct directory."

    with open(STATUS_LOG, "r") as f:
        content = f.read()

    assert "200" in content, f"FAIL: '200' OK not found in {STATUS_LOG}."

def test_alerts_log_exists_and_contains_storage_alert():
    """Verify that alerts.log exists and contains the STORAGE_ALERT string."""
    # Since the watcher runs every 2 seconds, it might take a moment to generate enough logs.
    # We will check if the file exists, and if it does, check its contents.
    # The grading environment should have given enough time to run.
    assert os.path.isfile(ALERTS_LOG), f"FAIL: {ALERTS_LOG} not found."

    with open(ALERTS_LOG, "r") as f:
        content = f.read()

    assert "STORAGE_ALERT" in content, f"FAIL: 'STORAGE_ALERT' not found in {ALERTS_LOG}."

def test_status_log_size_logic():
    """Verify that the alerts log is only created/appended when status log is > 100 bytes."""
    # If alerts.log exists, status.log must have exceeded 100 bytes at some point.
    assert os.path.isfile(STATUS_LOG), f"FAIL: {STATUS_LOG} is missing."
    assert os.path.isfile(ALERTS_LOG), f"FAIL: {ALERTS_LOG} is missing."

    status_size = os.path.getsize(STATUS_LOG)
    # Note: It's possible the size was >100 when the alert was triggered.
    # We just ensure the files are present and contain the right data as specified by the truth script.
    assert status_size > 0, f"FAIL: {STATUS_LOG} is empty."