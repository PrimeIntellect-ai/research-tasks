# test_final_state.py

import os
import csv
import json
import re
import subprocess
import time
import urllib.request
import urllib.error
import pytest

def test_objective1_vulnerable_csv():
    csv_path = "/home/user/vulnerable.csv"
    json_path = "/home/user/scan_data.json"

    assert os.path.exists(csv_path), f"File not found: {csv_path}"
    assert os.path.exists(json_path), f"File not found: {json_path}"

    # Recompute expected logic
    with open(json_path, 'r') as f:
        scan_data = json.load(f)

    expected_rows = []
    for svc in scan_data:
        unencrypted = svc.get("encryption") == "none" and svc.get("port") != 80
        cves = svc.get("cve_count", 0) > 0

        if unencrypted and cves:
            reason = "Critical"
        elif unencrypted:
            reason = "Unencrypted"
        elif cves:
            reason = "CVEs Found"
        else:
            continue

        expected_rows.append({
            "IP": svc["ip"],
            "Port": str(svc["port"]),
            "Service": svc["service"],
            "Reason": reason
        })

    expected_rows.sort(key=lambda x: int(x["Port"]))

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        actual_rows = list(reader)

    assert reader.fieldnames == ["IP", "Port", "Service", "Reason"], "CSV headers do not match the required format exactly."
    assert len(actual_rows) == len(expected_rows), "The number of vulnerable services in the CSV is incorrect."

    for actual, expected in zip(actual_rows, expected_rows):
        assert actual == expected, f"Row mismatch. Expected {expected}, got {actual}"

def test_objective2_xss_payload():
    payload_path = "/home/user/xss_payload.txt"
    assert os.path.exists(payload_path), f"File not found: {payload_path}"

    with open(payload_path, 'r') as f:
        content = f.read().strip()

    # Check for execution of alert(document.domain)
    # This is a basic check for educational purposes
    assert "alert(document.domain)" in content.replace(" ", ""), "The payload does not contain the required alert function."

    # Check if it's a valid HTML injection (script or event handler)
    is_script = re.search(r'<script\b[^>]*>.*alert\(document\.domain\).*</script>', content, re.IGNORECASE | re.DOTALL)
    is_event = re.search(r'<[^>]+on\w+\s*=\s*["\']?.*alert\(document\.domain\)["\']?[^>]*>', content, re.IGNORECASE | re.DOTALL)

    assert is_script or is_event, "The payload is not a valid XSS vector (missing script tags or event handlers)."

def test_objective3_csp_headers():
    app_path = "/home/user/webapp/app.py"
    assert os.path.exists(app_path), f"File not found: {app_path}"

    # Start the Flask app as a background process
    proc = subprocess.Popen(["python3", app_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        # Wait for the server to start
        time.sleep(2)

        req = urllib.request.Request("http://127.0.0.1:8080/greet")
        try:
            with urllib.request.urlopen(req) as response:
                headers = response.headers
        except urllib.error.URLError as e:
            pytest.fail(f"Failed to connect to the Flask application: {e}")

        csp_header = headers.get("Content-Security-Policy")
        assert csp_header is not None, "Content-Security-Policy header is missing from the response."

        # Check the exact policy
        expected_policy = "default-src 'self'; script-src 'none';"
        assert expected_policy in csp_header, f"CSP header value is incorrect. Expected to find: {expected_policy}"

    finally:
        proc.terminate()
        proc.wait()

def test_objective4_ssh_hardening():
    hardened_path = "/home/user/ssh_configs/sshd_config_hardened"
    assert os.path.exists(hardened_path), f"File not found: {hardened_path}"

    with open(hardened_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

    config = {}
    for line in lines:
        parts = line.split()
        if len(parts) >= 2:
            key = parts[0]
            val = " ".join(parts[1:])
            config[key] = val

    assert config.get("PermitRootLogin") == "no", "PermitRootLogin is not set to 'no'."
    assert config.get("PasswordAuthentication") == "no", "PasswordAuthentication is not set to 'no'."
    assert config.get("Ciphers") == "chacha20-poly1305@openssh.com,aes256-gcm@openssh.com", "Ciphers line is incorrect or missing."

    # Check preserved configs
    assert config.get("Port") == "22", "Existing configuration 'Port 22' was not preserved."
    assert config.get("MaxAuthTries") == "6", "Existing configuration 'MaxAuthTries 6' was not preserved."
    assert config.get("X11Forwarding") == "no", "Existing configuration 'X11Forwarding no' was not preserved."