# test_final_state.py
import os
import time
import struct
import zlib
import requests
import pytest

def create_cpk(text_payload: str, timestamp: int) -> bytes:
    magic = b"CPK\x01"
    compressed = zlib.compress(text_payload.encode('utf-8'))
    payload_len = len(compressed)
    crc = zlib.crc32(compressed) & 0xFFFFFFFF

    header = struct.pack("<4sIII", magic, timestamp, payload_len, crc)
    return header + compressed

def test_service_ready_log():
    log_path = "/home/user/service_ready.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist. Service might not be started."
    with open(log_path, "r") as f:
        content = f.read()
    assert "SERVICE RUNNING" in content, f"Log file {log_path} does not contain 'SERVICE RUNNING'."

def test_api_unauthorized():
    url = "http://127.0.0.1:8181/latest"
    try:
        response = requests.get(url, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API on 127.0.0.1:8181: {e}")

    assert response.status_code in (401, 403), f"Expected 401 or 403 for unauthorized request, got {response.status_code}"

def test_api_upload_and_latest():
    base_url = "http://127.0.0.1:8181"
    headers = {"Authorization": "Bearer conf-sync-secret"}

    # Generate first CPK
    ts1 = int(time.time()) - 1000
    text1 = "config_data_version_1"
    cpk1 = create_cpk(text1, ts1)

    # Upload first CPK
    upload_res1 = requests.post(f"{base_url}/upload", headers=headers, data=cpk1, timeout=5)
    assert upload_res1.status_code == 200, f"Upload failed: {upload_res1.status_code} {upload_res1.text}"

    # Give the background watcher a moment to process
    time.sleep(1)

    # Check latest
    latest_res1 = requests.get(f"{base_url}/latest", headers=headers, timeout=5)
    assert latest_res1.status_code == 200, f"GET /latest failed: {latest_res1.status_code} {latest_res1.text}"
    data1 = latest_res1.json()
    assert data1.get("status") == "ok", "Expected status 'ok'"
    assert data1.get("timestamp") == ts1, f"Expected timestamp {ts1}, got {data1.get('timestamp')}"
    assert data1.get("data") == text1, f"Expected data '{text1}', got '{data1.get('data')}'"

    # Generate second CPK (newer timestamp)
    ts2 = ts1 + 500
    text2 = "config_data_version_2_updated"
    cpk2 = create_cpk(text2, ts2)

    # Upload second CPK
    upload_res2 = requests.post(f"{base_url}/upload", headers=headers, data=cpk2, timeout=5)
    assert upload_res2.status_code == 200, f"Upload failed: {upload_res2.status_code} {upload_res2.text}"

    # Give the background watcher a moment to process
    time.sleep(1)

    # Check latest again
    latest_res2 = requests.get(f"{base_url}/latest", headers=headers, timeout=5)
    assert latest_res2.status_code == 200, f"GET /latest failed: {latest_res2.status_code} {latest_res2.text}"
    data2 = latest_res2.json()
    assert data2.get("timestamp") == ts2, f"Expected updated timestamp {ts2}, got {data2.get('timestamp')}"
    assert data2.get("data") == text2, f"Expected updated data '{text2}', got '{data2.get('data')}'"