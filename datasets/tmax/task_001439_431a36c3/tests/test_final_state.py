# test_final_state.py

import os
import subprocess
import requests
import pytest
import time

def test_service_root_exists():
    assert os.path.isdir("/home/user/service_root/bin"), "The build script was not run successfully; /home/user/service_root/bin is missing."
    assert os.path.isfile("/home/user/service_root/bin/socat"), "socat is missing from the service root bin directory."
    assert os.path.isfile("/home/user/service_root/bin/jq"), "jq is missing from the service root bin directory."

def get_expected_result(hex_payload: str) -> str:
    # Use the legacy processor to determine the expected output
    proc = subprocess.run(
        ["/app/legacy_processor", hex_payload],
        capture_output=True,
        text=True
    )
    if proc.returncode != 0:
        raise ValueError("Invalid payload for legacy processor")
    return proc.stdout.strip()

def test_server_valid_request():
    payload = "48656c6c6f" # "Hello" in hex
    expected_output = get_expected_result(payload)

    try:
        response = requests.post(
            "http://127.0.0.1:9000/api/process",
            json={"payload": payload},
            timeout=5
        )
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the server at 127.0.0.1:9000. Is the server running?")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"
    assert "application/json" in response.headers.get("Content-Type", ""), "Expected Content-Type to be application/json"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response was not valid JSON: {response.text}")

    assert "result" in data, f"Expected 'result' key in JSON response, got {data}"
    assert data["result"] == expected_output, f"Expected result '{expected_output}', got '{data['result']}'"

def test_server_invalid_request():
    payload = "invalidhex!"

    try:
        response = requests.post(
            "http://127.0.0.1:9000/api/process",
            json={"payload": payload},
            timeout=5
        )
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the server at 127.0.0.1:9000. Is the server running?")

    assert response.status_code == 400, f"Expected status code 400 for invalid payload, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response was not valid JSON: {response.text}")

    assert "error" in data, f"Expected 'error' key in JSON response, got {data}"
    assert data["error"] == "invalid payload", f"Expected error message 'invalid payload', got '{data['error']}'"