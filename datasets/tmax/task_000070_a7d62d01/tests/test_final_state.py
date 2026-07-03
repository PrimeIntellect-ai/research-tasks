# test_final_state.py
import os
import requests
import base64
import pytest

def test_server_running_and_correct():
    url = "http://127.0.0.1:8080/mask"

    test_cases = [
        (b"Hello", 42),
        (b"Testing 123", 255),
        (b"\x00\x01\x02", 0),
        (b"", 12),
        (b"A" * 1000, 128),
    ]

    for raw_bytes, key in test_cases:
        payload_b64 = base64.b64encode(raw_bytes).decode('utf-8')
        req_json = {"payload": payload_b64, "key": key}

        try:
            resp = requests.post(url, json=req_json, timeout=5)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to server at {url} or request timed out: {e}")

        assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}. Response: {resp.text}"

        try:
            resp_json = resp.json()
        except ValueError:
            pytest.fail(f"Response is not valid JSON. Response text: {resp.text}")

        assert "masked_base64" in resp_json, f"Response JSON missing 'masked_base64' key. Response: {resp_json}"

        masked_b64 = resp_json["masked_base64"]
        try:
            masked_bytes = base64.b64decode(masked_b64)
        except Exception as e:
            pytest.fail(f"Failed to decode base64 response: {masked_b64}. Error: {e}")

        assert len(masked_bytes) == len(raw_bytes), "Masked payload length does not match original payload length"

        # Verify XOR logic
        expected_bytes = bytes(b ^ key for b in raw_bytes)
        assert masked_bytes == expected_bytes, f"Masked payload incorrect for key {key}."

def test_files_unmodified():
    test_file = "/app/pr_workspace/test_wrapper.py"
    assert os.path.exists(test_file), f"{test_file} is missing"
    with open(test_file, "r") as f:
        content = f.read()
        assert "from hypothesis import given" in content, "test_wrapper.py appears to have been modified (missing hypothesis import)"
        assert "def test_mask_roundtrip(data, key):" in content, "test_wrapper.py appears to have been modified (missing test_mask_roundtrip)"

def test_server_log_exists():
    log_file = "/app/pr_workspace/server.log"
    assert os.path.exists(log_file), f"Log file {log_file} is missing. The server output should be redirected here."
    assert os.path.isfile(log_file), f"{log_file} is not a regular file."