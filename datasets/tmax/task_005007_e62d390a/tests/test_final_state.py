# test_final_state.py

import os
import pytest

REPORT_FILE = "/home/user/report.txt"

@pytest.fixture
def report_data():
    assert os.path.isfile(REPORT_FILE), f"The report file {REPORT_FILE} was not created."

    data = {}
    with open(REPORT_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or "=" not in line:
                continue
            key, val = line.split("=", 1)
            data[key.strip()] = val.strip()

    return data

def test_backdoor_pid(report_data):
    assert "BACKDOOR_PID" in report_data, "BACKDOOR_PID is missing from the report."
    assert report_data["BACKDOOR_PID"] == "9042", f"Expected BACKDOOR_PID to be 9042, but got {report_data['BACKDOOR_PID']}."

def test_c2_url(report_data):
    assert "C2_URL" in report_data, "C2_URL is missing from the report."
    assert report_data["C2_URL"] == "https://c2.evil.com/payload", f"Expected C2_URL to be https://c2.evil.com/payload, but got {report_data['C2_URL']}."

def test_attacker_ips(report_data):
    assert "ATTACKER_IPS" in report_data, "ATTACKER_IPS is missing from the report."
    # The requirement says sorted alphabetically, comma-separated
    expected_ips = "203.0.113.45,203.0.113.88"
    assert report_data["ATTACKER_IPS"] == expected_ips, f"Expected ATTACKER_IPS to be {expected_ips}, but got {report_data['ATTACKER_IPS']}."

def test_allowed_scripts(report_data):
    assert "ALLOWED_SCRIPTS" in report_data, "ALLOWED_SCRIPTS is missing from the report."
    # The requirement says sorted alphabetically, comma-separated
    expected_scripts = "https://analytics.site.com,https://trusted.cdn.com"
    assert report_data["ALLOWED_SCRIPTS"] == expected_scripts, f"Expected ALLOWED_SCRIPTS to be {expected_scripts}, but got {report_data['ALLOWED_SCRIPTS']}."