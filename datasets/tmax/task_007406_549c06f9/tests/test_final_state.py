# test_final_state.py
import os
import json
import stat
import hashlib
import urllib.parse
import pytest

def test_incident_report_exists():
    report_path = '/home/user/incident_report.json'
    assert os.path.exists(report_path), f"Expected report file not found at {report_path}"
    assert os.path.isfile(report_path), f"Expected {report_path} to be a file"

def test_incident_report_structure_and_content():
    report_path = '/home/user/incident_report.json'
    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    expected_keys = {"malicious_requests", "decrypted_payloads", "tampered_files", "suid_files"}
    actual_keys = set(report.keys())
    assert expected_keys.issubset(actual_keys), f"Report is missing keys: {expected_keys - actual_keys}"

    # Recompute malicious_requests
    logs_path = '/home/user/traffic_logs.json'
    assert os.path.exists(logs_path), "Traffic logs file missing, cannot verify."
    with open(logs_path, 'r') as f:
        logs = json.load(f)

    expected_malicious_requests = []
    for log in logs:
        url = log.get('url', '')
        status = log.get('status')
        decoded_url = urllib.parse.unquote(url).lower()
        if '../' in decoded_url and status == 201:
            expected_malicious_requests.append(log.get('request_id'))

    expected_malicious_requests.sort()
    actual_malicious_requests = sorted(report.get("malicious_requests", []))
    assert actual_malicious_requests == expected_malicious_requests, (
        f"Expected malicious_requests {expected_malicious_requests}, got {actual_malicious_requests}"
    )

    # Note: Decrypted payloads are tricky to recompute without cryptography library,
    # but based on the setup, we expect exactly these two strings.
    expected_payloads = sorted(["Overwrite logger", "Set SUID on backup"])
    actual_payloads = sorted(report.get("decrypted_payloads", []))
    assert actual_payloads == expected_payloads, (
        f"Expected decrypted_payloads {expected_payloads}, got {actual_payloads}"
    )

    # Recompute tampered files
    hashes_path = '/home/user/system_hashes.txt'
    expected_tampered = []
    if os.path.exists(hashes_path):
        with open(hashes_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    expected_hash, filename = parts
                    file_path = os.path.join('/home/user/system', filename)
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as pf:
                            actual_hash = hashlib.sha256(pf.read()).hexdigest()
                        if actual_hash != expected_hash:
                            expected_tampered.append(file_path)

    expected_tampered.sort()
    actual_tampered = sorted(report.get("tampered_files", []))
    assert actual_tampered == expected_tampered, (
        f"Expected tampered_files {expected_tampered}, got {actual_tampered}"
    )

    # Recompute SUID files
    system_dir = '/home/user/system'
    expected_suid = []
    if os.path.exists(system_dir):
        for filename in os.listdir(system_dir):
            file_path = os.path.join(system_dir, filename)
            if os.path.isfile(file_path):
                st = os.stat(file_path)
                if st.st_mode & stat.S_ISUID:
                    expected_suid.append(file_path)

    expected_suid.sort()
    actual_suid = sorted(report.get("suid_files", []))
    assert actual_suid == expected_suid, (
        f"Expected suid_files {expected_suid}, got {actual_suid}"
    )