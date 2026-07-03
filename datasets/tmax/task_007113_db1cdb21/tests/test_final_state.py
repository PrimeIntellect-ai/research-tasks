# test_final_state.py

import os
import json
import subprocess
import hashlib
import pytest

AUDIT_SCRIPT = "/home/user/audit.sh"
AUDIT_REPORT = "/home/user/audit_report.json"
DAEMON_PATH = "/home/user/artifacts/web_server_daemon"

def get_expected_rodata_hash():
    """Dynamically compute the expected SHA256 hash of the .rodata section."""
    result = subprocess.run(
        ["objcopy", "-O", "binary", "--only-section=.rodata", DAEMON_PATH, "/dev/stdout"],
        capture_output=True,
        check=True
    )
    return hashlib.sha256(result.stdout).hexdigest()

def test_audit_script_exists():
    assert os.path.isfile(AUDIT_SCRIPT), f"Audit script {AUDIT_SCRIPT} is missing."

def test_audit_report_exists():
    assert os.path.isfile(AUDIT_REPORT), f"Audit report {AUDIT_REPORT} is missing."

def test_audit_report_content():
    with open(AUDIT_REPORT, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {AUDIT_REPORT} does not contain valid JSON.")

    # 1. Check rodata_hash
    expected_hash = get_expected_rodata_hash()
    actual_hash = report_data.get("rodata_hash")
    assert actual_hash == expected_hash, f"rodata_hash is incorrect. Expected {expected_hash}, got {actual_hash}."

    # 2. Check hash_match
    hash_match = report_data.get("hash_match")
    assert hash_match is True, f"hash_match should be True, got {hash_match}."

    # 3. Check cert_valid
    cert_valid = report_data.get("cert_valid")
    assert cert_valid is True, f"cert_valid should be True, got {cert_valid}."

    # 4. Check xss_vuln_count
    # Based on the setup, admin.html and profile.html contain 'eval('
    expected_xss_count = 2
    actual_xss_count = report_data.get("xss_vuln_count")
    assert actual_xss_count == expected_xss_count, f"xss_vuln_count is incorrect. Expected {expected_xss_count}, got {actual_xss_count}."