# test_final_state.py

import os
import stat
import pytest

AUDIT_SCRIPT = "/home/user/audit.sh"
AUDIT_REPORT = "/home/user/audit_report.csv"

EXPECTED_REPORT_LINES = [
    "/home/user/webapp/config.php,Injection_Risk",
    "/home/user/webapp/config.php,World_Writable",
    "/home/user/webapp/data.txt,World_Writable",
    "/home/user/webapp/index.html,CSP_XSS_Risk"
]

def test_audit_script_exists():
    assert os.path.isfile(AUDIT_SCRIPT), f"Audit script {AUDIT_SCRIPT} does not exist."

def test_audit_report_exists():
    assert os.path.isfile(AUDIT_REPORT), f"Audit report {AUDIT_REPORT} does not exist."

def test_audit_report_contents():
    assert os.path.isfile(AUDIT_REPORT), f"Audit report {AUDIT_REPORT} does not exist."
    with open(AUDIT_REPORT, "r") as f:
        # Read lines, strip whitespace, and ignore empty lines
        lines = [line.strip() for line in f if line.strip()]

    # Check that the lines match exactly the expected lines
    assert lines == EXPECTED_REPORT_LINES, (
        f"Audit report contents are incorrect.\n"
        f"Expected:\n{EXPECTED_REPORT_LINES}\n"
        f"Actual:\n{lines}"
    )