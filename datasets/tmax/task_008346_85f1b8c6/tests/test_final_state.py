# test_final_state.py
import os
import json
import re
import pytest

def test_report_exists_and_valid():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"The final report file {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The report file is not valid JSON.")

    assert "admin_password" in report_data, "Missing 'admin_password' in report."
    assert report_data["admin_password"] == "purplemonkey", "Incorrect admin_password. Did you crack the hash correctly?"

    assert "cert_valid" in report_data, "Missing 'cert_valid' in report."
    assert report_data["cert_valid"] is False, "Incorrect cert_valid value. The certificate chain should be invalid."

    assert "cwe_vulnerability" in report_data, "Missing 'cwe_vulnerability' in report."
    assert report_data["cwe_vulnerability"].upper() == "CWE-78", "Incorrect cwe_vulnerability. Look closely at the OS command execution."

    assert "redacted_log_lines_count" in report_data, "Missing 'redacted_log_lines_count' in report."
    assert report_data["redacted_log_lines_count"] == 3, "Incorrect redacted_log_lines_count. Check how many lines contained credit card numbers."

def test_redacted_log_file():
    redacted_log_path = "/home/user/app_backup/app_redacted.log"
    assert os.path.isfile(redacted_log_path), f"The redacted log file {redacted_log_path} does not exist."

    with open(redacted_log_path, "r") as f:
        content = f.read()

    # Ensure no credit card numbers remain
    cc_pattern = re.compile(r'\b\d{4}-\d{4}-\d{4}-\d{4}\b')
    assert not cc_pattern.search(content), "Found unredacted credit card numbers in the redacted log file."

    # Ensure [REDACTED] was used
    assert "[REDACTED]" in content, "The exact string '[REDACTED]' was not found in the redacted log file."

    # Check that exactly 4 instances of [REDACTED] are present (line 7 has two CCs)
    # Wait, the task says "every credit card number is replaced", line 7 has two.
    # The count of modified lines is 3, but the count of redactions is 4.
    redaction_count = content.count("[REDACTED]")
    assert redaction_count == 4, f"Expected 4 replacements of '[REDACTED]', but found {redaction_count}."