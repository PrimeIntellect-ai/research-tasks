# test_final_state.py
import os
import pytest

def test_pentest_report():
    report_path = "/home/user/pentest_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) >= 2, f"Report file {report_path} does not have at least 2 lines."
    assert lines[0] == "CERT_STATUS: VALID", f"Line 1 is incorrect. Expected 'CERT_STATUS: VALID', got '{lines[0]}'"
    assert lines[1] == "TOKEN: FLAG{sqli_auth_bypass_success_8832}", f"Line 2 is incorrect. Expected 'TOKEN: FLAG{{sqli_auth_bypass_success_8832}}', got '{lines[1]}'"
    assert len(lines) == 2, f"Report file {report_path} should have exactly 2 lines, found {len(lines)}."