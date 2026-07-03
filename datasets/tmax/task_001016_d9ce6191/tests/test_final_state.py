# test_final_state.py

import os
import stat
import re
import pytest

ALERTS_DIR = "/home/user/alerts/active"
SPOOL_FILE = "/home/user/spool/mail/network_alerts.txt"

EXPECTED_SYMLINKS = [
    "service_web.log",
    "service_worker.log",
    "service_auth.log"
]

UNEXPECTED_SYMLINKS = [
    "service_api.log"
]

def test_alerts_directory_exists():
    assert os.path.exists(ALERTS_DIR), f"Directory {ALERTS_DIR} does not exist."
    assert os.path.isdir(ALERTS_DIR), f"{ALERTS_DIR} is not a directory."

@pytest.mark.parametrize("filename", EXPECTED_SYMLINKS)
def test_expected_symlinks(filename):
    filepath = os.path.join(ALERTS_DIR, filename)
    assert os.path.exists(filepath), f"Expected symlink {filepath} does not exist."
    assert os.path.islink(filepath), f"{filepath} is not a symbolic link."
    # Check if it points to the correct file
    target = os.path.realpath(filepath)
    expected_target = os.path.join("/home/user/logs", filename)
    assert target == expected_target, f"Symlink {filepath} points to {target}, expected {expected_target}."

@pytest.mark.parametrize("filename", UNEXPECTED_SYMLINKS)
def test_unexpected_symlinks(filename):
    filepath = os.path.join(ALERTS_DIR, filename)
    assert not os.path.exists(filepath), f"Symlink {filepath} should not exist."

def test_spool_file_exists_and_permissions():
    assert os.path.exists(SPOOL_FILE), f"Spool file {SPOOL_FILE} does not exist."
    assert os.path.isfile(SPOOL_FILE), f"{SPOOL_FILE} is not a regular file."

    file_stat = os.stat(SPOOL_FILE)
    permissions = stat.S_IMODE(file_stat.st_mode)
    assert permissions == 0o600, f"Permissions of {SPOOL_FILE} are {oct(permissions)}, expected 0o600."

def test_spool_file_content():
    with open(SPOOL_FILE, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    # Check headers
    assert "To: admin@monitoring.local" in lines, "Missing 'To: admin@monitoring.local' header."
    assert "Subject: Network Alerts" in lines, "Missing 'Subject: Network Alerts' header."

    # Extract alerts
    alerts = [line for line in lines if line.startswith("ALERT:")]
    unique_alerts = set(alerts)

    expected_alerts = {
        "ALERT: service_auth cannot reach ldap_server",
        "ALERT: service_web cannot reach db_backend",
        "ALERT: service_worker cannot reach redis_cache"
    }

    assert unique_alerts == expected_alerts, f"Alerts do not match expected.\nFound: {unique_alerts}\nExpected: {expected_alerts}"