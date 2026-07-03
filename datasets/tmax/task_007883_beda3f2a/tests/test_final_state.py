# test_final_state.py

import os
import stat
import pytest

def test_evidence_directory_permissions():
    """Verify that the evidence directory has exactly 700 permissions."""
    evidence_dir = "/home/user/incident/evidence"
    assert os.path.isdir(evidence_dir), f"Directory {evidence_dir} does not exist."

    st = os.stat(evidence_dir)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o700, f"Permissions on {evidence_dir} are {oct(perms)}, expected exactly 0o700."

def test_csp_policy_content():
    """Verify that the CSP policy has been updated correctly."""
    csp_file = "/home/user/incident/csp_policy.txt"
    assert os.path.isfile(csp_file), f"File {csp_file} does not exist."

    with open(csp_file, "r") as f:
        content = f.read().strip()

    expected_csp = "default-src 'self'; script-src 'self' 'nonce-r4nd0m123';"
    assert content == expected_csp, f"CSP policy content is incorrect. Expected: '{expected_csp}', but got: '{content}'"

def test_report_content():
    """Verify that the final report contains the correct findings and format."""
    report_file = "/home/user/incident/report.txt"
    assert os.path.isfile(report_file), f"Report file {report_file} does not exist."

    with open(report_file, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "Evidence Secured: Yes",
        "Malicious Payloads:",
        "10.0.0.5 - <svg onload=alert(1)>",
        "172.16.0.2 - SELECT * FROM users",
        "Fixed CSP: default-src 'self'; script-src 'self' 'nonce-r4nd0m123';"
    ]

    for line in expected_lines:
        assert line in content, f"Expected line '{line}' not found in the report."

    # Ensure benign payloads are not in the report
    assert "192.168.1.10" not in content, "Report incorrectly includes benign IP 192.168.1.10"
    assert "192.168.1.11" not in content, "Report incorrectly includes benign IP 192.168.1.11"