# test_final_state.py
import json
import os
import requests
from urllib.parse import urlparse

def test_forensics_report():
    report_path = '/home/user/forensics_report.json'
    assert os.path.isfile(report_path), f"Forensics report missing at {report_path}"

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, "Forensics report is not valid JSON"

    assert report.get('attacker_ip') == '198.51.100.42', f"Incorrect attacker_ip in forensics report. Got: {report.get('attacker_ip')}"
    assert report.get('extracted_key') == 'KEY-8f4a3b2c1d9e8f7a6b5c4d3e2f1a0b9c', f"Incorrect extracted_key in forensics report. Got: {report.get('extracted_key')}"

def test_frontend_remediation_evil_url():
    try:
        r = requests.get('http://127.0.0.1:8080/login?next=http://evil.com', allow_redirects=False, timeout=2)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to frontend service: {e}. Is the service running on port 8080?"
    assert r.status_code == 400, f"Expected HTTP 400 for absolute URL, got {r.status_code}"

def test_frontend_remediation_double_slash():
    try:
        r = requests.get('http://127.0.0.1:8080/login?next=//evil.com', allow_redirects=False, timeout=2)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to frontend service: {e}. Is the service running on port 8080?"
    assert r.status_code == 400, f"Expected HTTP 400 for double-slash URL, got {r.status_code}"

def test_frontend_remediation_valid_relative():
    try:
        r = requests.get('http://127.0.0.1:8080/login?next=/dashboard', allow_redirects=False, timeout=2)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to frontend service: {e}. Is the service running on port 8080?"
    assert r.status_code == 302, f"Expected HTTP 302 for valid relative URL, got {r.status_code}"
    loc = r.headers.get('Location', '')
    parsed = urlparse(loc)
    assert parsed.path == '/dashboard', f"Expected redirect to /dashboard, got {loc}"

def test_frontend_remediation_no_next():
    try:
        r = requests.get('http://127.0.0.1:8080/login', allow_redirects=False, timeout=2)
    except requests.exceptions.RequestException as e:
        assert False, f"Failed to connect to frontend service: {e}. Is the service running on port 8080?"
    assert r.status_code == 302, f"Expected HTTP 302 for missing next parameter, got {r.status_code}"
    loc = r.headers.get('Location', '')
    parsed = urlparse(loc)
    assert parsed.path == '/home', f"Expected redirect to /home, got {loc}"