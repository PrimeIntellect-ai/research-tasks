# test_final_state.py

import os
import struct
import zlib
import requests
import pytest

def generate_payload(text: bytes, valid_checksum: bool = True) -> bytes:
    magic = b"CFG\x01"
    uncompressed_len = len(text)

    crc = zlib.crc32(text) & 0xFFFFFFFF
    checksum = crc ^ 0xDEADBEEF
    if not valid_checksum:
        checksum = (checksum ^ 0xFFFFFFFF) & 0xFFFFFFFF

    compressed = zlib.compress(text)

    return struct.pack(">4sII", magic, uncompressed_len, checksum) + compressed

def test_valid_config_push():
    url = "http://127.0.0.1:8000/api/v1/config/push"
    headers = {"Authorization": "Bearer track-configs-2024"}
    text = b"TEST_KEY_1=100\nTEST_KEY_2=active\n"
    payload = generate_payload(text, valid_checksum=True)

    try:
        resp = requests.post(url, headers=headers, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert data.get("status") == "applied", f"Expected status 'applied', got: {data.get('status')}"
    updated = data.get("updated_keys", [])
    assert "TEST_KEY_1" in updated, "TEST_KEY_1 missing from updated_keys"
    assert "TEST_KEY_2" in updated, "TEST_KEY_2 missing from updated_keys"

    # Verify filesystem
    store_path_1 = "/home/user/config_store/TEST_KEY_1.conf"
    store_path_2 = "/home/user/config_store/TEST_KEY_2.conf"

    assert os.path.exists(store_path_1), f"Expected config file {store_path_1} was not created."
    with open(store_path_1, "r") as f:
        assert f.read() == "100", "Content of TEST_KEY_1.conf does not match."

    assert os.path.exists(store_path_2), f"Expected config file {store_path_2} was not created."
    with open(store_path_2, "r") as f:
        assert f.read() == "active", "Content of TEST_KEY_2.conf does not match."

def test_invalid_checksum_push():
    url = "http://127.0.0.1:8000/api/v1/config/push"
    headers = {"Authorization": "Bearer track-configs-2024"}
    text = b"BAD_KEY=1\n"
    payload = generate_payload(text, valid_checksum=False)

    try:
        resp = requests.post(url, headers=headers, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert resp.status_code == 400, f"Expected 400 Bad Request for invalid checksum, got {resp.status_code}. Response: {resp.text}"

    store_path = "/home/user/config_store/BAD_KEY.conf"
    assert not os.path.exists(store_path), "Config file created despite invalid checksum."

def test_missing_or_invalid_auth():
    url = "http://127.0.0.1:8000/api/v1/config/push"
    text = b"AUTH_KEY=1\n"
    payload = generate_payload(text, valid_checksum=True)

    # No auth header
    try:
        resp1 = requests.post(url, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")
    assert resp1.status_code != 200, "Service accepted request without Authorization header."

    # Invalid auth header
    headers = {"Authorization": "Bearer wrong-token"}
    try:
        resp2 = requests.post(url, headers=headers, data=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")
    assert resp2.status_code != 200, "Service accepted request with invalid Authorization header."