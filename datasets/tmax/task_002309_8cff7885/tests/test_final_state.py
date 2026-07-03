# test_final_state.py

import os
import subprocess
import requests
import pytest
import time

def test_system_timezone():
    """Verify the system timezone is set to Europe/Helsinki."""
    result = subprocess.run(['timedatectl', 'show'], capture_output=True, text=True)
    assert 'Timezone=Europe/Helsinki' in result.stdout, "System timezone is not set to Europe/Helsinki."

def test_system_locale():
    """Verify the system locale is set to fi_FI.UTF-8."""
    result = subprocess.run(['localectl', 'show'], capture_output=True, text=True)
    assert 'fi_FI.UTF-8' in result.stdout, "System locale is not set to fi_FI.UTF-8."

def test_vault_file_exists_and_content():
    """Verify the vault file exists and contains the correct data."""
    vault_path = "/home/user/secure_fs/vault.txt"
    assert os.path.exists(vault_path), f"Vault file {vault_path} is missing."
    with open(vault_path, 'r') as f:
        content = f.read().strip()
    assert content == "CONFIDENTIAL_SYSTEM_DATA", "Vault file does not contain the expected data."

def test_https_endpoint_success():
    """Verify the full chain (Nginx -> SSH Tunnel -> C++ Server) works with correct authorization."""
    url = "https://127.0.0.1:8443/vault"
    headers = {"Authorization": "Bearer A9b3FkL2"}

    try:
        response = requests.get(url, headers=headers, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTPS endpoint: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"
    assert "CONFIDENTIAL_SYSTEM_DATA" in response.text, "Response body does not contain the expected vault data."

def test_https_endpoint_forbidden():
    """Verify the endpoint returns 403 Forbidden with an incorrect token."""
    url = "https://127.0.0.1:8443/vault"
    headers = {"Authorization": "Bearer BADTOKEN"}

    try:
        response = requests.get(url, headers=headers, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTPS endpoint: {e}")

    assert response.status_code == 403, f"Expected status code 403, got {response.status_code}."

def test_https_endpoint_missing_token():
    """Verify the endpoint returns 403 Forbidden when the token is missing."""
    url = "https://127.0.0.1:8443/vault"

    try:
        response = requests.get(url, verify=False, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTPS endpoint: {e}")

    assert response.status_code == 403, f"Expected status code 403, got {response.status_code}."