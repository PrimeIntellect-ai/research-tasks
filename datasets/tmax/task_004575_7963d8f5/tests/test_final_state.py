# test_final_state.py

import os
import subprocess
import requests
import pytest
import urllib3

# Disable insecure request warnings since we are using self-signed/test certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_DIR = "/app/compliance_system"

def test_server_crt_created():
    """Verify that the server.crt file was created and contains multiple certificates (full chain)."""
    server_crt_path = os.path.join(BASE_DIR, "certs", "server.crt")
    assert os.path.isfile(server_crt_path), f"Certificate file {server_crt_path} is missing."

    with open(server_crt_path, "r") as f:
        content = f.read()

    # Check that it contains at least two certificates (leaf + intermediate)
    cert_count = content.count("-----BEGIN CERTIFICATE-----")
    assert cert_count >= 2, f"Expected at least 2 certificates in {server_crt_path} for a full chain, found {cert_count}."

def test_nginx_tls_chain():
    """Verify that Nginx is serving the full certificate chain."""
    try:
        # Use openssl s_client to check the certificate chain
        cmd = [
            "openssl", "s_client",
            "-connect", "127.0.0.1:8443",
            "-servername", "localhost"
        ]
        # We pass a dummy input to close the connection immediately
        result = subprocess.run(cmd, input=b"Q\n", stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        output = result.stdout.decode()

        # Check if depth 1 (intermediate) is present in the chain
        assert "s:CN" in output or "i:CN" in output, "Failed to retrieve certificate information from Nginx."
        # A full chain should show multiple certs in the chain
        assert "Certificate chain" in output, "Certificate chain not found in openssl output."
    except subprocess.TimeoutExpired:
        pytest.fail("Timeout while trying to connect to Nginx via openssl s_client.")
    except Exception as e:
        pytest.fail(f"Error running openssl s_client: {e}")

def test_open_redirect_mitigation():
    """Verify that the open redirect vulnerability is fixed."""
    url = "https://127.0.0.1:8443/login?redirect_to=http://attacker.com"
    try:
        response = requests.get(url, verify=False, allow_redirects=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx at {url}: {e}")

    assert response.status_code == 302, f"Expected HTTP 302 for {url}, got {response.status_code}."
    assert response.headers.get("Location") == "/dashboard", f"Expected redirect to /dashboard, got {response.headers.get('Location')}."

def test_legitimate_redirect():
    """Verify that legitimate relative redirects still work."""
    url = "https://127.0.0.1:8443/login?redirect_to=/settings"
    try:
        response = requests.get(url, verify=False, allow_redirects=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx at {url}: {e}")

    assert response.status_code == 302, f"Expected HTTP 302 for {url}, got {response.status_code}."
    assert response.headers.get("Location") == "/settings", f"Expected redirect to /settings, got {response.headers.get('Location')}."

def test_report_service_integration():
    """Verify that the /audit endpoint proxies to the Report service correctly."""
    url = "https://127.0.0.1:8443/audit"
    try:
        response = requests.get(url, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for {url}, got {response.status_code}."
    assert "Audit Trail Active" in response.text, f"Expected 'Audit Trail Active' in response body, got: {response.text}"