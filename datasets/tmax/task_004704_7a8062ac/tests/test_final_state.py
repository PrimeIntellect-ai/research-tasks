# test_final_state.py
import pytest
import requests

def test_audit_endpoint():
    url = "http://127.0.0.1:8080/audit"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the audit server at {url}. Is the Bash server running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP status 200, got {response.status_code}"

    csp_header = response.headers.get('Content-Security-Policy')
    assert csp_header == "default-src 'none';", f"Expected CSP header 'default-src 'none';', got {csp_header}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON: {response.text}")

    assert data.get("status") == "audited", f"Expected status 'audited', got {data.get('status')}"
    assert data.get("tampered_file") == "index.html", f"Expected tampered_file 'index.html', got {data.get('tampered_file')}"
    assert data.get("attacker_ip") == "192.168.1.105", f"Expected attacker_ip '192.168.1.105', got {data.get('attacker_ip')}"

    secret = data.get("secret_token")
    # Allow some leniency in transcription formatting
    expected_secrets = ["delta-tango-seven", "delta tango seven"]
    assert secret in expected_secrets, f"Expected secret_token to be one of {expected_secrets}, got {secret}"