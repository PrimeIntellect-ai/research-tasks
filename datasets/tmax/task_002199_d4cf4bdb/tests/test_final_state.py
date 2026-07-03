# test_final_state.py

import os
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/workspace"
REPORT_PATH = os.path.join(WORKSPACE_DIR, "report.txt")
FIXED_CGI_PATH = os.path.join(WORKSPACE_DIR, "fixed_login.cgi")
AUDIT_LOG_PATH = os.path.join(WORKSPACE_DIR, "audit.log")

def test_report_contents():
    """Verify that report.txt contains the correct malicious URL and CWE ID."""
    assert os.path.isfile(REPORT_PATH), f"Report file missing: {REPORT_PATH}"

    with open(REPORT_PATH, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.read().splitlines()]

    assert len(lines) >= 2, f"Report file {REPORT_PATH} must contain at least 2 lines."

    expected_url = "http://malicious-tracker.com/steal"
    expected_cwe = "CWE-601"

    assert lines[0] == expected_url, f"Line 1 of report.txt is incorrect. Expected '{expected_url}', got '{lines[0]}'"
    assert lines[1] == expected_cwe, f"Line 2 of report.txt is incorrect. Expected '{expected_cwe}', got '{lines[1]}'"

def test_fixed_cgi_exists_and_executable():
    """Verify that fixed_login.cgi was compiled and is executable."""
    assert os.path.isfile(FIXED_CGI_PATH), f"Compiled fixed binary missing: {FIXED_CGI_PATH}"
    assert os.access(FIXED_CGI_PATH, os.X_OK), f"Compiled fixed binary is not executable: {FIXED_CGI_PATH}"

def test_fixed_cgi_open_redirect_prevention():
    """Verify that fixed_login.cgi prevents open redirects and allows safe ones."""
    test_cases = [
        ("next=http://evil.com", "Location: /index.html"),
        ("next=//evil.com", "Location: /index.html"),
        ("next=/dashboard/main", "Location: /dashboard/main"),
        ("next=somethingelse", "Location: /index.html")
    ]

    for query_string, expected_location in test_cases:
        env = os.environ.copy()
        env["QUERY_STRING"] = query_string

        result = subprocess.run(
            [FIXED_CGI_PATH],
            env=env,
            cwd=WORKSPACE_DIR,
            capture_output=True,
            text=True
        )

        output = result.stdout
        assert expected_location in output, (
            f"Failed open redirect test for QUERY_STRING='{query_string}'. "
            f"Expected to find '{expected_location}' in output, but got:\n{output}"
        )

def test_fixed_cgi_cookie_redaction():
    """Verify that fixed_login.cgi redacts SessionID in audit.log but leaves other cookies intact."""
    if os.path.exists(AUDIT_LOG_PATH):
        os.remove(AUDIT_LOG_PATH)

    env = os.environ.copy()
    env["QUERY_STRING"] = "next=/home"
    env["HTTP_COOKIE"] = "Tracking=999; SessionID=SuperSecret123; Prefs=dark"

    subprocess.run(
        [FIXED_CGI_PATH],
        env=env,
        cwd=WORKSPACE_DIR,
        capture_output=True,
        text=True
    )

    assert os.path.isfile(AUDIT_LOG_PATH), f"Audit log was not created at {AUDIT_LOG_PATH}"

    with open(AUDIT_LOG_PATH, "r", encoding="utf-8") as f:
        log_content = f.read()

    assert "SuperSecret123" not in log_content, "Sensitive SessionID value 'SuperSecret123' was leaked in audit.log!"
    assert "SessionID=REDACTED" in log_content, "SessionID was not properly replaced with 'REDACTED' in audit.log."
    assert "Tracking=999" in log_content, "Other cookie 'Tracking=999' was incorrectly modified or removed."
    assert "Prefs=dark" in log_content, "Other cookie 'Prefs=dark' was incorrectly modified or removed."