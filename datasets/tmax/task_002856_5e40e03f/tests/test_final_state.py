# test_final_state.py

import os
import json
import hashlib
import pytest

def test_audit_report_exists():
    assert os.path.isfile("/home/user/audit_report.json"), "Audit report /home/user/audit_report.json does not exist."

def test_audit_report_content():
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), "Audit report missing."

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Audit report is not valid JSON.")

    assert "vulnerable_files" in report, "Missing 'vulnerable_files' key in report."
    assert "insecure_csp" in report, "Missing 'insecure_csp' key in report."

    # Compute expected vulnerable files and hashes dynamically
    expected_vulnerable_files = {}
    base_dir = "/home/user/app_audit"
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            file_path = os.path.join(root, file)
            # Check if world-writable (others have write permission)
            if os.stat(file_path).st_mode & 0o002:
                with open(file_path, "rb") as f:
                    file_hash = hashlib.sha256(f.read()).hexdigest()
                expected_vulnerable_files[file_path] = file_hash

    # Compute expected insecure CSPs dynamically
    expected_insecure_csps = []
    policy_path = "/home/user/app_audit/network_policy.json"
    if os.path.isfile(policy_path):
        with open(policy_path, "r") as f:
            try:
                policy = json.load(f)
                for csp in policy.get("csp", []):
                    if "default-src" not in csp:
                        expected_insecure_csps.append(csp)
            except json.JSONDecodeError:
                pass

    # Validate vulnerable_files
    assert report["vulnerable_files"] == expected_vulnerable_files, \
        f"vulnerable_files does not match expected.\nExpected: {expected_vulnerable_files}\nGot: {report['vulnerable_files']}"

    # Validate insecure_csp (order-independent)
    assert isinstance(report["insecure_csp"], list), "'insecure_csp' must be a list."
    assert sorted(report["insecure_csp"]) == sorted(expected_insecure_csps), \
        f"insecure_csp does not match expected.\nExpected: {expected_insecure_csps}\nGot: {report['insecure_csp']}"