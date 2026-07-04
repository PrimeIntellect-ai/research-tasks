# test_final_state.py

import os
import re
import pytest
import requests

def test_frontend_cwe_txt():
    path = "/home/user/frontend_cwe.txt"
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content in ["CWE-22", "CWE-78"], f"Expected CWE-22 or CWE-78 in {path}, got: {content}"

def test_backup_script_fixed():
    path = "/app/system_audit/backup.sh"
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, "r") as f:
        content = f.read()

    # The script must use tar but should not use a wildcard *
    assert "tar" in content, "The backup.sh script must still use 'tar'."

    # Check if tar is used with wildcard
    for line in content.splitlines():
        if "tar " in line:
            assert "*" not in line, f"Wildcard '*' found in tar command: {line}"

def test_flag_decrypted():
    path = "/home/user/flag.txt"
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "FLAG{x0r_1s_n0t_s3cur3_3ncrypt10n}", f"Incorrect flag in {path}"

def test_frontend_health():
    url = "http://127.0.0.1:8080/health"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to frontend health endpoint: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    try:
        json_data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert json_data.get("status") == "ok", f"Expected {{'status': 'ok'}}, got {json_data}"

def test_frontend_encrypt_proxy():
    url = "http://127.0.0.1:8080/encrypt"
    try:
        response = requests.post(url, data={"text": "hello"}, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to frontend encrypt endpoint: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"
    assert response.text.strip(), "Expected a non-empty response from the encrypt endpoint."

def test_crypto_service_listening():
    url = "http://127.0.0.1:5000"
    try:
        # Just check if the port is open and accepting connections
        response = requests.get(url, timeout=5)
        # We don't care about the status code, just that it didn't raise a ConnectionError
    except requests.ConnectionError:
        pytest.fail("Crypto service is not listening on 127.0.0.1:5000")
    except requests.RequestException:
        pass # Other exceptions like 404, 405 are fine, it means the service is up