# test_final_state.py
import os
import json
import pytest

WEB_LOG_PATH = "/home/user/incident_workspace/decrypted/web.log"
AUTH_LOG_PATH = "/home/user/incident_workspace/decrypted/auth.log"
REPORT_PATH = "/home/user/incident_report.json"

def test_decrypted_web_log_exists_and_correct():
    assert os.path.isfile(WEB_LOG_PATH), f"Decrypted web log not found at {WEB_LOG_PATH}"

    with open(WEB_LOG_PATH, "r") as f:
        content = f.read()

    assert "192.168.1.105 - GET /api/v1/diagnostic" in content, "Decrypted web log does not contain the expected attacker traffic. Decryption may have failed or output is incorrect."
    assert "10.0.0.55 - GET /index.html 200" in content, "Decrypted web log is missing expected benign traffic."

def test_decrypted_auth_log_exists_and_correct():
    assert os.path.isfile(AUTH_LOG_PATH), f"Decrypted auth log not found at {AUTH_LOG_PATH}"

    with open(AUTH_LOG_PATH, "r") as f:
        content = f.read()

    assert "COMMAND=/usr/bin/tar -cf /dev/null" in content, "Decrypted auth log does not contain the expected privilege escalation event."
    assert "Accepted publickey for user1" in content, "Decrypted auth log is missing expected benign events."

def test_incident_report_exists_and_valid_json():
    assert os.path.isfile(REPORT_PATH), f"Incident report not found at {REPORT_PATH}"

    with open(REPORT_PATH, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Incident report is not valid JSON.")

    assert isinstance(report, dict), "Incident report should be a JSON object."

    expected_keys = {"attacker_ip", "exploited_endpoint", "privesc_binary"}
    assert expected_keys.issubset(report.keys()), f"Incident report is missing required keys. Expected {expected_keys}, found {set(report.keys())}"

def test_incident_report_values():
    with open(REPORT_PATH, "r") as f:
        report = json.load(f)

    assert report.get("attacker_ip") == "192.168.1.105", f"Incorrect attacker_ip. Expected '192.168.1.105', got '{report.get('attacker_ip')}'"
    assert report.get("exploited_endpoint") == "/api/v1/diagnostic", f"Incorrect exploited_endpoint. Expected '/api/v1/diagnostic', got '{report.get('exploited_endpoint')}'"
    assert report.get("privesc_binary") == "/usr/bin/tar", f"Incorrect privesc_binary. Expected '/usr/bin/tar', got '{report.get('privesc_binary')}'"