# test_final_state.py
import os
import json
import socket
import time
import hashlib
import requests
import pytest

def test_nginx_proxy_analyze_payload():
    """Test the HTTP REST API /analyze_payload endpoint via Nginx port 8000."""
    url = "http://127.0.0.1:8000/analyze_payload"

    # Test vulnerable payload (CWE-22)
    payload_vuln = {"filename": "../../../etc/passwd", "content": "test"}
    try:
        r_vuln = requests.post(url, json=payload_vuln, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on port 8000: {e}")

    assert r_vuln.status_code == 200, f"Expected 200 OK for /analyze_payload, got {r_vuln.status_code}. Response: {r_vuln.text}"
    try:
        data_vuln = r_vuln.json()
    except ValueError:
        pytest.fail(f"Response from /analyze_payload is not valid JSON: {r_vuln.text}")

    assert data_vuln.get("cwe") == "CWE-22" and data_vuln.get("status") == "vulnerable", \
        f"Expected CWE-22 and vulnerable status, got {data_vuln}"

    # Test safe payload
    payload_safe = {"filename": "image.png", "content": "test"}
    r_safe = requests.post(url, json=payload_safe, timeout=2)
    assert r_safe.status_code == 200, f"Expected 200 OK for safe payload, got {r_safe.status_code}"
    data_safe = r_safe.json()
    assert data_safe.get("status") == "safe", f"Expected safe status, got {data_safe}"

def test_nginx_proxy_verify_integrity():
    """Test the HTTP REST API /verify_integrity endpoint via Nginx port 8000."""
    url = "http://127.0.0.1:8000/verify_integrity"
    test_file = "/app/test_file.txt"

    assert os.path.exists(test_file), f"Test file {test_file} is missing"
    with open(test_file, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    # Test valid hash
    payload_valid = {"filepath": test_file, "expected_sha256": file_hash}
    r_valid = requests.post(url, json=payload_valid, timeout=2)
    assert r_valid.status_code == 200, f"Expected 200 OK for /verify_integrity, got {r_valid.status_code}"
    assert r_valid.json().get("verified") is True, f"Expected verified: true, got {r_valid.json()}"

    # Test invalid hash
    payload_invalid = {"filepath": test_file, "expected_sha256": "0000000000000000000000000000000000000000000000000000000000000000"}
    r_invalid = requests.post(url, json=payload_invalid, timeout=2)
    assert r_invalid.status_code == 200, f"Expected 200 OK for invalid hash, got {r_invalid.status_code}"
    assert r_invalid.json().get("verified") is False, f"Expected verified: false, got {r_invalid.json()}"

    # Test file not found
    payload_404 = {"filepath": "/app/does_not_exist_file.txt", "expected_sha256": file_hash}
    r_404 = requests.post(url, json=payload_404, timeout=2)
    assert r_404.status_code == 404, f"Expected 404 for missing file, got {r_404.status_code}"

def test_tcp_log_parsing():
    """Test the Raw TCP Log Receiver on port 9001."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect(("127.0.0.1", 9001))
    except Exception as e:
        pytest.fail(f"Could not connect to TCP port 9001: {e}")

    log_line = "[2024-01-01T00:00:00Z] 10.0.0.5 EXFILTRATE /etc/shadow\n"
    s.sendall(log_line.encode("utf-8"))
    s.close()

    # Wait a moment for the server to process the log and write to file
    time.sleep(1.0)

    log_file = "/app/parsed_logs.json"
    assert os.path.isfile(log_file), f"{log_file} does not exist. TCP server may not be writing logs correctly."

    found = False
    with open(log_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if (obj.get("timestamp") == "2024-01-01T00:00:00Z" and 
                    obj.get("ip") == "10.0.0.5" and 
                    obj.get("action") == "EXFILTRATE" and 
                    obj.get("target") == "/etc/shadow"):
                    found = True
                    break
            except json.JSONDecodeError:
                pass

    assert found, f"Did not find the expected parsed JSON log object in {log_file}"