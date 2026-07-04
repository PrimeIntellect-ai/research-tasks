# test_final_state.py
import os
import stat
import json
import pytest

REPORT_PATH = "/home/user/audit_report.json"
LOG_DIR = "/home/user/app/logs"

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} was not created."

def test_report_content():
    with open(REPORT_PATH, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} is not valid JSON.")

    # 1. Certificate Validation
    assert "cert_valid" in report, "Key 'cert_valid' missing from report."
    assert report["cert_valid"] is True, "'cert_valid' should be true based on the provided certificates."

    # 2. Intrusion Detection & Redaction
    assert "intrusions" in report, "Key 'intrusions' missing from report."
    expected_intrusions = [
        "192.168.1.50 - GET /api/data?key=[REDACTED]&query=UNION SELECT * FROM users HTTP/1.1",
        "10.0.0.2 - GET /download?file=../../../../etc/passwd HTTP/1.1"
    ]
    actual_intrusions = report["intrusions"]
    assert isinstance(actual_intrusions, list), "'intrusions' should be a list."
    assert len(actual_intrusions) == len(expected_intrusions), f"Expected {len(expected_intrusions)} intrusions, found {len(actual_intrusions)}."

    for expected in expected_intrusions:
        assert expected in actual_intrusions, f"Missing expected intrusion line: {expected}"

    # 3. Fixed Files
    assert "fixed_files" in report, "Key 'fixed_files' missing from report."
    expected_fixed = {
        "/home/user/app/logs/access.log",
        "/home/user/app/logs/debug.log"
    }
    actual_fixed = report["fixed_files"]
    assert isinstance(actual_fixed, list), "'fixed_files' should be a list."
    assert set(actual_fixed) == expected_fixed, f"Expected fixed_files to be {expected_fixed}, but got {set(actual_fixed)}."

def test_file_permissions_fixed():
    # Check that no files in the log directory are accessible by 'others'
    # and that the specific files were modified to 640.
    assert os.path.isdir(LOG_DIR), f"Log directory {LOG_DIR} is missing."

    for filename in os.listdir(LOG_DIR):
        filepath = os.path.join(LOG_DIR, filename)
        if not os.path.isfile(filepath):
            continue

        st = os.stat(filepath)
        mode = stat.S_IMODE(st.st_mode)

        # Check that 'others' have no permissions (read=4, write=2, exec=1 for others is the last octal digit)
        assert (mode & stat.S_IRWXO) == 0, f"File {filepath} still grants permissions to 'others' (mode: {oct(mode)})."

    # Verify specific files are exactly 640
    for target_file in ["access.log", "debug.log"]:
        filepath = os.path.join(LOG_DIR, target_file)
        if os.path.isfile(filepath):
            mode = stat.S_IMODE(os.stat(filepath).st_mode)
            assert mode == 0o640, f"File {filepath} permissions were not set to exactly 640 (current: {oct(mode)})."