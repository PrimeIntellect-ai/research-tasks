# test_final_state.py
import os
import json
import stat
import pytest

REPORT_PATH = "/home/user/audit_report.json"
WEBAPP_DIR = "/home/user/webapp"

def get_world_writable_executable():
    """Find the world-writable and executable file in the webapp directory."""
    if not os.path.exists(WEBAPP_DIR):
        return None
    for root, dirs, files in os.walk(WEBAPP_DIR):
        for file in files:
            filepath = os.path.join(root, file)
            st = os.stat(filepath)
            if bool(st.st_mode & stat.S_IWOTH) and bool(st.st_mode & stat.S_IXOTH):
                return filepath
    return None

def test_audit_report_exists():
    assert os.path.exists(REPORT_PATH), f"The audit report was not found at {REPORT_PATH}."
    assert os.path.isfile(REPORT_PATH), f"{REPORT_PATH} is not a valid file."

def test_audit_report_content():
    assert os.path.exists(REPORT_PATH), f"The audit report was not found at {REPORT_PATH}."

    with open(REPORT_PATH, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {REPORT_PATH} does not contain valid JSON.")

    expected_keys = {"world_writable_file", "cwe_id", "db_pass"}
    missing_keys = expected_keys - set(report.keys())
    assert not missing_keys, f"The audit report is missing the following keys: {missing_keys}"

    # 1. Check world writable file
    expected_file = get_world_writable_executable() or "/home/user/webapp/cleanup.sh"
    assert report["world_writable_file"] == expected_file, \
        f"Expected 'world_writable_file' to be '{expected_file}', but got '{report.get('world_writable_file')}'."

    # 2. Check CWE ID
    actual_cwe = str(report.get("cwe_id", "")).strip().upper()
    assert actual_cwe == "CWE-798", \
        f"Expected 'cwe_id' to be 'CWE-798', but got '{report.get('cwe_id')}'."

    # 3. Check DB Password
    # Since AES-128-CBC decryption requires a third-party library, we use the expected truth value directly.
    expected_db_pass = "P0w3rful_@ud1t_P@ss"
    assert report["db_pass"] == expected_db_pass, \
        f"Expected 'db_pass' to be correct, but the decrypted value does not match the expected password."