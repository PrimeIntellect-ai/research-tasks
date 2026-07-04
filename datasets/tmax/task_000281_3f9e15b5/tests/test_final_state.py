# test_final_state.py

import os

def test_exploit_go_exists():
    """Verify that the exploit.go file was created by the user."""
    assert os.path.isfile("/home/user/exploit.go"), "The file /home/user/exploit.go does not exist."

def test_incident_report_exists():
    """Verify that the incident_report.txt file was created by the exploit."""
    assert os.path.isfile("/home/user/incident_report.txt"), "The file /home/user/incident_report.txt does not exist. The exploit may have failed."

def test_incident_report_contents():
    """Verify that the incident_report.txt file contains the exact expected string."""
    with open("/home/user/incident_report.txt", "r") as f:
        content = f.read()
    assert content == "VULNERABLE", f"The contents of /home/user/incident_report.txt are incorrect. Expected 'VULNERABLE', got '{content}'"