# test_final_state.py
import os
import pytest

def test_audit_report_exists():
    report_path = "/home/user/audit_report.html"
    assert os.path.isfile(report_path), f"The audit report was not found at {report_path}."

def test_audit_report_content():
    report_path = "/home/user/audit_report.html"
    assert os.path.isfile(report_path), f"The audit report was not found at {report_path}."

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    # We expect these exact strings or very close matches based on the Jinja template and drift calculations
    expected_alpha = "server_alpha: Anomalies=1, AvgDrift=483.0"
    expected_beta = "server_beta: Anomalies=0, AvgDrift=2.5"
    expected_gamma = "server_gamma: Anomalies=2, AvgDrift=100.0"

    assert expected_alpha in content, f"Expected '{expected_alpha}' to be in the audit report. Report content:\n{content}"
    assert expected_beta in content, f"Expected '{expected_beta}' to be in the audit report. Report content:\n{content}"
    assert expected_gamma in content, f"Expected '{expected_gamma}' to be in the audit report. Report content:\n{content}"

def test_audit_script_exists():
    script_path = "/home/user/audit_configs.py"
    assert os.path.isfile(script_path), f"The script was not found at {script_path}."