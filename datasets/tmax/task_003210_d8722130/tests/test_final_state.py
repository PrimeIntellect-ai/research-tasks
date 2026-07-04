# test_final_state.py

import json
import os
import pytest

REPORT_PATH = '/home/user/audit_report.json'

def test_audit_report_exists():
    assert os.path.isfile(REPORT_PATH), f"The audit report file {REPORT_PATH} is missing."

def test_audit_report_contents():
    try:
        with open(REPORT_PATH, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {REPORT_PATH} does not contain valid JSON.")

    assert 'service_port' in data, "Key 'service_port' is missing in the audit report."
    assert data['service_port'] == 8443, f"Expected 'service_port' to be 8443, got {data['service_port']}."

    assert 'csp_unsafe_inline' in data, "Key 'csp_unsafe_inline' is missing in the audit report."
    assert data['csp_unsafe_inline'] is True, f"Expected 'csp_unsafe_inline' to be True, got {data['csp_unsafe_inline']}."

    assert 'exploit_successful' in data, "Key 'exploit_successful' is missing in the audit report."
    assert data['exploit_successful'] is True, f"Expected 'exploit_successful' to be True, got {data['exploit_successful']}."

    assert 'cert_subject' in data, "Key 'cert_subject' is missing in the audit report."
    cert_subject = data['cert_subject']
    assert isinstance(cert_subject, str), f"Expected 'cert_subject' to be a string, got {type(cert_subject)}."
    assert "ComplianceCorp" in cert_subject, "The 'cert_subject' does not contain 'ComplianceCorp'."
    assert "internal-audit-mock" in cert_subject, "The 'cert_subject' does not contain 'internal-audit-mock'."