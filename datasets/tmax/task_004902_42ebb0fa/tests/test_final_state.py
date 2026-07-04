# test_final_state.py

import os
import pytest

def test_incident_report_exists():
    assert os.path.isfile("/home/user/incident_report.txt"), "incident_report.txt was not created at /home/user/incident_report.txt"

def test_incident_report_content():
    expected_content = (
        "Vulnerable_File: log_02.txt\n"
        "Leaked_Session: xyz890leaked\n"
        "Keys_Intact: true"
    )

    with open("/home/user/incident_report.txt", "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"The incident report content is incorrect. Expected:\n{expected_content}\nGot:\n{content}"