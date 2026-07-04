# test_final_state.py

import os
import json
import re
import pytest

def test_authorized_keys_remediated():
    auth_keys_path = "/home/user/.ssh/authorized_keys"
    assert os.path.isfile(auth_keys_path), f"File missing: {auth_keys_path}"

    with open(auth_keys_path, "r") as f:
        content = f.read()

    assert "admin@local" in content, "Valid key 'admin@local' was incorrectly removed from authorized_keys"
    assert "evil@empire.c2" not in content, "Rogue key 'evil@empire.c2' is still present in authorized_keys"

def test_webapp_remediated():
    app_py_path = "/home/user/webapp/app.py"
    assert os.path.isfile(app_py_path), f"Web application missing: {app_py_path}"

    with open(app_py_path, "r") as f:
        content = f.read()

    # Check for path traversal fix
    assert "secure_filename" in content, "Path traversal vulnerability not remediated: 'secure_filename' not found in app.py"

    # Check for CSP fix
    assert "default-src 'self';" in content, "CSP header not properly secured: expected \"default-src 'self';\" in app.py"
    assert "unsafe-inline" not in content, "Insecure CSP directive 'unsafe-inline' is still present in app.py"

def test_forensics_report():
    report_path = "/home/user/forensics_report.json"
    assert os.path.isfile(report_path), f"Forensics report missing: {report_path}"

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Forensics report is not valid JSON: {report_path}")

    # Check C2 address
    assert "c2_address" in report, "Missing 'c2_address' in forensics report"
    assert report["c2_address"] == "198.51.100.77:4444", f"Incorrect C2 address: {report['c2_address']}"

    # Check vulnerable route
    assert "vulnerable_route" in report, "Missing 'vulnerable_route' in forensics report"
    assert report["vulnerable_route"] == "/upload_file", f"Incorrect vulnerable route: {report['vulnerable_route']}"

    # Check rogue key fingerprint format
    assert "rogue_key_fingerprint" in report, "Missing 'rogue_key_fingerprint' in forensics report"
    fingerprint = report["rogue_key_fingerprint"]
    assert fingerprint.startswith("SHA256:"), f"Fingerprint does not start with 'SHA256:': {fingerprint}"
    assert len(fingerprint) > 10, f"Fingerprint appears too short to be valid: {fingerprint}"