# test_final_state.py

import os

def test_audit_report_exists():
    """Verify that the audit_report.txt file exists at the exact required location."""
    assert os.path.isfile("/home/user/audit_report.txt"), "The file /home/user/audit_report.txt does not exist."

def test_audit_report_contents():
    """Verify that the audit_report.txt contains the correct findings."""
    with open("/home/user/audit_report.txt", "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines()]

    assert len(lines) >= 4, f"Expected at least 4 lines in audit_report.txt, but found {len(lines)}."

    assert lines[0] == "31337", f"Line 1 (port number) is incorrect. Expected '31337', got '{lines[0]}'."
    assert lines[1] == "SECURE_ADMIN_TOKEN_99812", f"Line 2 (leaked token) is incorrect. Expected 'SECURE_ADMIN_TOKEN_99812', got '{lines[1]}'."
    assert lines[2] == "X-Missing-CSP-Header", f"Line 3 (missing security header) is incorrect. Expected 'X-Missing-CSP-Header', got '{lines[2]}'."
    assert lines[3] == "FLAG{pyc_str1ngs_r3v3rs3d}", f"Line 4 (hidden flag) is incorrect. Expected 'FLAG{{pyc_str1ngs_r3v3rs3d}}', got '{lines[3]}'."