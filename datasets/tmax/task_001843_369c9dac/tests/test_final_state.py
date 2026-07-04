# test_final_state.py

import os
import json
import hashlib
import requests
import pytest

def test_ready_file_exists():
    assert os.path.exists("/home/user/ready.txt"), "The /home/user/ready.txt file does not exist. Did you write it after starting the service?"

def test_orchestrator_api():
    # Create test artifact
    test_file_path = "/tmp/test_artifact.bin"
    test_content = b"verification_payload_123"
    with open(test_file_path, "wb") as f:
        f.write(test_content)

    expected_signature = hashlib.sha256(test_content).hexdigest()

    payload = {
        "expr": "A & (B | C)",
        "cache_data": "cache_key_999",
        "file_path": test_file_path
    }

    try:
        response = requests.post("http://127.0.0.1:8080/process", json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the orchestrator API at 127.0.0.1:8080: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response body: {response.text}")

    assert "ast" in data, f"Response JSON missing 'ast' key. Got: {data}"
    assert "hash" in data, f"Response JSON missing 'hash' key. Got: {data}"
    assert "signature" in data, f"Response JSON missing 'signature' key. Got: {data}"

    expected_ast = {"parsed_expr": "A & (B | C)"}
    assert data["ast"] == expected_ast, f"Unexpected 'ast' value. Expected {expected_ast}, got {data['ast']}"

    expected_hash = "cache_key_999_hashed"
    assert data["hash"] == expected_hash, f"Unexpected 'hash' value. Expected '{expected_hash}', got '{data['hash']}'"

    assert data["signature"] == expected_signature, f"Unexpected 'signature' value. Expected '{expected_signature}', got '{data['signature']}'"