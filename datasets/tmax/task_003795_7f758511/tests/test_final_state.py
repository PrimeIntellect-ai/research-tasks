# test_final_state.py
import requests
import struct
import pytest

URL = "http://127.0.0.1:8888/pack"

def test_pack_success():
    payload = {
        "project_id": 999,
        "files": [
            {"name": "test.txt", "content": "12345"},
            {"name": "dir/file", "content": "abcdef"}
        ]
    }
    try:
        response = requests.post(URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {URL}: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Body: {response.text}"

    # Check binary content
    expected_magic = b"ARCH"
    expected_proj_id = struct.pack("<I", 999)
    expected_num_files = struct.pack("<H", 2)

    file1_name_len = struct.pack("<H", 8)
    file1_name = b"test.txt"
    file1_content_len = struct.pack("<I", 5)
    file1_content = b"12345"

    file2_name_len = struct.pack("<H", 8)
    file2_name = b"dir/file"
    file2_content_len = struct.pack("<I", 6)
    file2_content = b"abcdef"

    expected_body = (
        expected_magic + expected_proj_id + expected_num_files +
        file1_name_len + file1_name + file1_content_len + file1_content +
        file2_name_len + file2_name + file2_content_len + file2_content
    )

    assert response.content == expected_body, f"Binary response mismatch. Expected {expected_body.hex()}, got {response.content.hex()}"
    assert response.headers.get("Content-Type") == "application/octet-stream", "Expected Content-Type: application/octet-stream"

def test_pack_dynamic():
    payload = {
        "project_id": 42,
        "files": [
            {"name": "a", "content": "b"}
        ]
    }
    try:
        response = requests.post(URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {URL}: {e}")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Body: {response.text}"

    expected_body = b"ARCH" + struct.pack("<I", 42) + struct.pack("<H", 1) + \
                    struct.pack("<H", 1) + b"a" + struct.pack("<I", 1) + b"b"

    assert response.content == expected_body, f"Binary response mismatch for dynamic test."

def test_malformed_json():
    try:
        response = requests.post(URL, data="not json", headers={"Content-Type": "application/json"}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Server crashed or failed to connect on malformed JSON: {e}")

    assert response.status_code != 200, f"Expected non-200 status code for malformed JSON, got {response.status_code}"