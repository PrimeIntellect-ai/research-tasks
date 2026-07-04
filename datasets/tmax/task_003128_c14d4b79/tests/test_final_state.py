# test_final_state.py

import os
import stat
import pytest
import requests

def test_filesystem_state():
    """Test the filesystem state for the vault."""
    vault_dir = "/home/user/vault"
    data_dir = os.path.join(vault_dir, "data")
    active_data = os.path.join(vault_dir, "active_data")
    app_users = os.path.join(vault_dir, "app_users.conf")

    # Check vault dir permissions
    assert os.path.isdir(vault_dir), f"{vault_dir} is not a directory."
    vault_stat = os.stat(vault_dir)
    assert stat.S_IMODE(vault_stat.st_mode) == 0o700, f"Permissions of {vault_dir} are not 0700."

    # Check data dir and chunks
    assert os.path.isdir(data_dir), f"{data_dir} is not a directory."
    chunk1 = os.path.join(data_dir, "chunk1.dat")
    chunk2 = os.path.join(data_dir, "chunk2.dat")
    chunk3 = os.path.join(data_dir, "chunk3.dat")

    assert os.path.isfile(chunk1), f"{chunk1} is missing."
    assert os.path.isfile(chunk2), f"{chunk2} is missing."
    assert os.path.isfile(chunk3), f"{chunk3} is missing."

    assert os.path.getsize(chunk1) == 1024, f"{chunk1} size is not 1024 bytes."
    assert os.path.getsize(chunk2) == 2048, f"{chunk2} size is not 2048 bytes."
    assert os.path.getsize(chunk3) == 4096, f"{chunk3} size is not 4096 bytes."

    # Check symlink
    assert os.path.islink(active_data), f"{active_data} is not a symlink."
    assert os.readlink(active_data) == "/home/user/vault/data", f"{active_data} does not point to /home/user/vault/data."

    # Check app_users.conf
    assert os.path.isfile(app_users), f"{app_users} is missing."
    app_users_stat = os.stat(app_users)
    assert stat.S_IMODE(app_users_stat.st_mode) == 0o400, f"Permissions of {app_users} are not 0400."

    with open(app_users, "r") as f:
        content = f.read().strip()
    expected_content = "api_admin:x:1001:1001:API Administrator:/home/user/vault:/bin/false"
    assert content == expected_content, f"Content of {app_users} is incorrect."

def test_api_unauthorized():
    """Test that the API returns 401 Unauthorized without correct header."""
    url = "http://127.0.0.1:8123/metrics"

    # Missing header
    try:
        response = requests.get(url, timeout=5)
        assert response.status_code == 401, f"Expected 401 for missing header, got {response.status_code}."
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    # Wrong header
    try:
        response = requests.get(url, headers={"X-Vault-Auth": "wrong password"}, timeout=5)
        assert response.status_code == 401, f"Expected 401 for wrong header, got {response.status_code}."
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

def test_api_authorized():
    """Test that the API returns 200 OK and correct JSON with correct header."""
    url = "http://127.0.0.1:8123/metrics"
    headers = {"X-Vault-Auth": "the access code is crimson butterfly protocol"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Body: {response.text}"

        data = response.json()
        assert data.get("status") == "secure", "Expected status to be 'secure'."
        assert data.get("total_bytes") == 7168, f"Expected total_bytes to be 7168, got {data.get('total_bytes')}."
        assert data.get("acl_present") is True, "Expected acl_present to be True."
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")
    except ValueError:
        pytest.fail(f"API did not return valid JSON. Response text: {response.text}")