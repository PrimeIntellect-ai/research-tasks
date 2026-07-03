# test_final_state.py

import json
import os
from pathlib import Path
import pytest

AUDIT_REPORT_PATH = "/home/user/compliance_audit.json"
REDACTED_LOGS_PATH = "/home/user/redacted_logs.log"

def get_audit_report():
    path = Path(AUDIT_REPORT_PATH)
    assert path.exists(), f"Audit report is missing at {AUDIT_REPORT_PATH}"
    assert path.is_file(), f"Path {AUDIT_REPORT_PATH} exists but is not a file"

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"Audit report at {AUDIT_REPORT_PATH} is not valid JSON: {e}")

def test_audit_report_malicious_ips():
    """Verify the malicious IPs are correctly identified."""
    report = get_audit_report()
    assert "malicious_ips" in report, "Key 'malicious_ips' is missing from the audit report."

    expected_ips = {"172.16.0.4", "10.10.10.10"}
    actual_ips = set(report["malicious_ips"])

    assert actual_ips == expected_ips, (
        f"Malicious IPs do not match expected values.\n"
        f"Expected: {expected_ips}\n"
        f"Found: {actual_ips}"
    )

def test_audit_report_decoded_payloads():
    """Verify the decoded XSS payloads are correctly identified."""
    report = get_audit_report()
    assert "decoded_xss_payloads" in report, "Key 'decoded_xss_payloads' is missing from the audit report."

    expected_payloads = {"javascript:alert(1)", "<script>steal()</script>"}
    actual_payloads = set(report["decoded_xss_payloads"])

    assert actual_payloads == expected_payloads, (
        f"Decoded XSS payloads do not match expected values.\n"
        f"Expected: {expected_payloads}\n"
        f"Found: {actual_payloads}"
    )

def test_audit_report_privesc_vuln():
    """Verify the privilege escalation vulnerability file is correctly identified."""
    report = get_audit_report()
    assert "privesc_vuln_file" in report, "Key 'privesc_vuln_file' is missing from the audit report."

    expected_file = "/home/user/system_configs/sudoers.d/02-backup-vuln"
    actual_file = report["privesc_vuln_file"]

    assert actual_file == expected_file, (
        f"Privilege escalation vulnerability file is incorrect.\n"
        f"Expected: '{expected_file}'\n"
        f"Found: '{actual_file}'"
    )

def test_audit_report_redacted_count():
    """Verify the redacted log lines count is correct."""
    report = get_audit_report()
    assert "redacted_log_lines_count" in report, "Key 'redacted_log_lines_count' is missing from the audit report."

    expected_count = 3
    actual_count = report["redacted_log_lines_count"]

    assert actual_count == expected_count, (
        f"Redacted log lines count is incorrect.\n"
        f"Expected: {expected_count}\n"
        f"Found: {actual_count}"
    )

def test_redacted_logs_exist_and_correctly_redacted():
    """Verify the redacted logs file exists and sensitive data is properly masked."""
    path = Path(REDACTED_LOGS_PATH)
    assert path.exists(), f"Redacted logs file is missing at {REDACTED_LOGS_PATH}"
    assert path.is_file(), f"Path {REDACTED_LOGS_PATH} exists but is not a file"

    content = path.read_text(encoding="utf-8")

    # 1. Verify specific SSNs are gone
    assert "123-45-6789" not in content, "Found unredacted SSN (123-45-6789) in the redacted logs."
    assert "987-65-4321" not in content, "Found unredacted SSN (987-65-4321) in the redacted logs."

    # 2. Verify specific Bearer tokens are gone
    assert "abcdef1234567890ABCD==" not in content, "Found unredacted Bearer token in the redacted logs."
    assert "XYZxyz9876543210abcd==" not in content, "Found unredacted Bearer token in the redacted logs."

    # 3. Verify the replacement strings exist in the correct quantities
    ssn_redaction_count = content.count("[REDACTED_SSN]")
    assert ssn_redaction_count == 2, (
        f"Expected exactly 2 occurrences of '[REDACTED_SSN]', found {ssn_redaction_count}."
    )

    token_redaction_count = content.count("Bearer [REDACTED_TOKEN]")
    assert token_redaction_count == 2, (
        f"Expected exactly 2 occurrences of 'Bearer [REDACTED_TOKEN]', found {token_redaction_count}."
    )