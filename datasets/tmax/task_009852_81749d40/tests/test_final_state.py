# test_final_state.py
import os
import pytest

def test_forensic_report_exists_and_correct():
    report_path = "/home/user/forensic_report.txt"
    assert os.path.isfile(report_path), f"The file {report_path} was not created."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = (
        "Attacker IP: 192.168.1.50\n"
        "Target Path: /admin/secrets\n"
        "Bypass Header: X-Internal-IP: 127.0.0.1\n"
        "Forged Cookie: session_role=admin"
    )

    assert content == expected_content, f"The content of {report_path} does not match the expected output. Got:\n{content}"