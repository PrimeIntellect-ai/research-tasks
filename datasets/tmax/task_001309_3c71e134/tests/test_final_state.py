# test_final_state.py

import os
import json
import base64
import requests
import pytest

def test_config_exists():
    """Verify that the configuration file was created correctly."""
    config_path = "/app/config.json"
    assert os.path.exists(config_path), f"Configuration file {config_path} is missing."

    with open(config_path, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Configuration file {config_path} is not valid JSON.")

    assert config.get("environment") == "production", "Config 'environment' is not 'production'."
    assert config.get("version") == 3, "Config 'version' is not 3."

def test_rust_library_compiled():
    """Verify that the Rust library was compiled in release mode."""
    so_path = "/app/rust_math/target/release/librust_math.so"
    assert os.path.exists(so_path), f"Compiled Rust library {so_path} is missing. Did you build with --release?"

def test_server_unauthorized():
    """Verify that the server rejects requests without the correct Authorization header."""
    url = "http://127.0.0.1:8080/encode"

    # Missing header
    try:
        response = requests.post(url, json={"data": "test"})
        assert response.status_code == 401, f"Expected 401 Unauthorized for missing auth header, got {response.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the server. Is it running on 127.0.0.1:8080?")

    # Wrong header
    response = requests.post(url, headers={"Authorization": "Bearer wrong-token"}, json={"data": "test"})
    assert response.status_code == 401, f"Expected 401 Unauthorized for wrong auth header, got {response.status_code}"

def test_server_encode_success():
    """Verify that the server correctly encodes data using the Rust library and the OCR multiplier."""
    url = "http://127.0.0.1:8080/encode"
    headers = {"Authorization": "Bearer migrate-token-2024"}

    test_string = "test_string"
    payload = {"data": test_string}

    try:
        response = requests.post(url, headers=headers, json=payload)
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the server. Is it running on 127.0.0.1:8080?")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        resp_json = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Server response is not valid JSON: {response.text}")

    assert "result" in resp_json, "Response JSON missing 'result' key."

    # Calculate expected result
    multiplier = 17
    expected_bytes = bytes([(b * multiplier) % 256 for b in test_string.encode('utf-8')])
    expected_base64 = base64.b64encode(expected_bytes).decode('utf-8')

    assert resp_json["result"] == expected_base64, f"Expected encoded result '{expected_base64}', got '{resp_json['result']}'"