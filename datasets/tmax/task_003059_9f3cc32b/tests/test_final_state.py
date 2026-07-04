# test_final_state.py

import os
import json
import stat
import requests
import pytest

def test_findings_json():
    findings_path = "/home/user/findings.json"
    assert os.path.isfile(findings_path), f"Findings file missing: {findings_path}"

    with open(findings_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {findings_path} is not valid JSON")

    assert data.get("attacker_ip") == "10.0.0.15", f"Incorrect attacker_ip: {data.get('attacker_ip')}"
    assert data.get("compromised_user") == "alice_admin", f"Incorrect compromised_user: {data.get('compromised_user')}"

    # Derive world-writable files dynamically from the file system
    web_root = "/home/user/web_root"
    expected_insecure = []
    if os.path.exists(web_root):
        for root, dirs, files in os.walk(web_root):
            for file in files:
                full_path = os.path.join(root, file)
                mode = os.stat(full_path).st_mode
                if mode & stat.S_IWOTH:
                    expected_insecure.append(full_path)

    expected_insecure.sort()
    actual_insecure = sorted(data.get("insecure_files", []))

    assert actual_insecure == expected_insecure, f"Incorrect insecure_files. Expected {expected_insecure}, got {actual_insecure}"

def test_reporting_service():
    url = "http://127.0.0.1:8080/report"
    headers = {
        "Authorization": "Bearer Incident-Resp-2024",
        "Content-Type": "application/json"
    }

    # Derive the payload dynamically based on the expected state
    web_root = "/home/user/web_root"
    expected_insecure = []
    if os.path.exists(web_root):
        for root, dirs, files in os.walk(web_root):
            for file in files:
                full_path = os.path.join(root, file)
                mode = os.stat(full_path).st_mode
                if mode & stat.S_IWOTH:
                    expected_insecure.append(full_path)

    payload = {
        "attacker_ip": "10.0.0.15",
        "compromised_user": "alice_admin",
        "insecure_files": sorted(expected_insecure)
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to reporting service at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"
    assert "REPORT_RECEIVED" in response.text, f"Expected 'REPORT_RECEIVED' in response body, got: {response.text}"