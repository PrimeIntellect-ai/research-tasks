# test_final_state.py

import os
import subprocess
import pytest
import requests
import time
import socket

def test_certificates_exist_and_valid():
    crt_path = "/home/user/certs/server.crt"
    key_path = "/home/user/certs/server.key"

    assert os.path.exists(crt_path), f"Certificate file {crt_path} does not exist."
    assert os.path.exists(key_path), f"Key file {key_path} does not exist."

    # Check if it's a valid x509 cert for *.internal.corp
    try:
        result = subprocess.run(
            ["openssl", "x509", "-in", crt_path, "-noout", "-subject"],
            capture_output=True, text=True, check=True
        )
        assert "*.internal.corp" in result.stdout, "Certificate is not for *.internal.corp"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to parse certificate: {e.stderr}")

def test_proxy_listening():
    def is_port_open(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0

    assert is_port_open(8080), "Proxy is not listening on 127.0.0.1:8080"
    assert is_port_open(8443), "Proxy is not listening on 127.0.0.1:8443"

def test_benign_http_request():
    try:
        response = requests.get(
            "http://127.0.0.1:8080/login",
            headers={"Host": "test.internal.corp"},
            timeout=5
        )
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
        assert "CLEAN" in response.text, "Response did not contain the expected output from the binary."
    except requests.RequestException as e:
        pytest.fail(f"Benign HTTP request failed: {e}")

def test_benign_https_request():
    try:
        response = requests.get(
            "https://127.0.0.1:8443/login",
            headers={"Host": "test.internal.corp"},
            verify=False,
            timeout=5
        )
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
        assert "CLEAN" in response.text, "Response did not contain the expected output from the binary."
    except requests.RequestException as e:
        pytest.fail(f"Benign HTTPS request failed: {e}")

def test_malicious_http_request_dropped():
    malicious_headers = {
        "Host": "test.internal.corp",
        "Referer": "http://test.internal.corp//evil.com/%2e%2e"
    }
    try:
        response = requests.get(
            "http://127.0.0.1:8080/login",
            headers=malicious_headers,
            timeout=5
        )
        pytest.fail(f"Expected connection to be dropped, but received response: {response.status_code}")
    except requests.exceptions.ConnectionError:
        pass # Expected behavior
    except requests.RequestException as e:
        pytest.fail(f"Unexpected exception during malicious HTTP request: {e}")

def test_malicious_https_request_dropped():
    malicious_headers = {
        "Host": "test.internal.corp",
        "Referer": "http://test.internal.corp//evil.com/%2e%2e"
    }
    try:
        response = requests.get(
            "https://127.0.0.1:8443/login",
            headers=malicious_headers,
            verify=False,
            timeout=5
        )
        pytest.fail(f"Expected connection to be dropped, but received response: {response.status_code}")
    except requests.exceptions.ConnectionError:
        pass # Expected behavior
    except requests.RequestException as e:
        pytest.fail(f"Unexpected exception during malicious HTTPS request: {e}")

def test_security_drops_log():
    log_path = "/home/user/security_drops.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    expected_log_entry = "[DROP] IP=127.0.0.1 Payload=aHR0cDovL3Rlc3QuaW50ZXJuYWwuY29ycC8vZXZpbC5jb20vJTJlJTJl"

    with open(log_path, "r") as f:
        logs = f.read()

    assert expected_log_entry in logs, f"Expected log entry '{expected_log_entry}' not found in {log_path}."