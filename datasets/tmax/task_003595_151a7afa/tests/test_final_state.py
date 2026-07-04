# test_final_state.py

import os
import json
import pytest

def test_investigate_script_exists():
    assert os.path.isfile("/home/user/investigate.py"), "The script /home/user/investigate.py was not found."

def test_incident_report_exists():
    assert os.path.isfile("/home/user/incident_report.json"), "The report /home/user/incident_report.json was not found."

def test_incident_report_content():
    try:
        with open("/home/user/incident_report.json", "r") as f:
            report = json.load(f)
    except json.JSONDecodeError:
        pytest.fail("/home/user/incident_report.json is not a valid JSON file.")
    except Exception as e:
        pytest.fail(f"Failed to read /home/user/incident_report.json: {e}")

    # 1. Compromised File
    assert "compromised_file" in report, "Missing 'compromised_file' key in the JSON report."
    expected_compromised = "/home/user/webroot/login.html"
    assert report["compromised_file"] == expected_compromised, f"Incorrect compromised_file. Expected {expected_compromised}, got {report['compromised_file']}."

    # 2. XSS Target URL
    assert "xss_target_url" in report, "Missing 'xss_target_url' key in the JSON report."
    url = report["xss_target_url"]
    # Accept the base URL or the URL with query parameters
    assert url.startswith("https://evil-exfil.net/steal"), f"Incorrect xss_target_url. Expected it to start with 'https://evil-exfil.net/steal', got '{url}'."

    # 3. World Writable File
    assert "world_writable_file" in report, "Missing 'world_writable_file' key in the JSON report."
    expected_writable = "/home/user/webroot/db_config.ini"
    assert report["world_writable_file"] == expected_writable, f"Incorrect world_writable_file. Expected {expected_writable}, got {report['world_writable_file']}."

    # 4. CSP Bypassed
    assert "csp_bypassed" in report, "Missing 'csp_bypassed' key in the JSON report."
    assert report["csp_bypassed"] is True, f"Incorrect csp_bypassed. Expected True, got {report['csp_bypassed']}."