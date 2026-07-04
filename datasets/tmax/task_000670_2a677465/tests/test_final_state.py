# test_final_state.py
import os
import hashlib
import tempfile
import subprocess
import requests
import pytest

GATEWAY_URL = "http://127.0.0.1:9090/build"
SEED_VALUE = b"K3yV4lUe99"

def test_gateway_invalid_payload():
    payload = {"source": "invalid_instruction_test xyz"}

    try:
        response = requests.post(GATEWAY_URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the gateway at {GATEWAY_URL}: {e}")

    assert response.status_code == 400, f"Expected HTTP 400 for invalid assembly, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert "error" in data, "Response JSON is missing the 'error' key."
    assert data["error"] == "compilation failed", f"Expected error 'compilation failed', got '{data['error']}'."

def test_gateway_valid_payload():
    source_code = "global _start\n_start:\nmov rax, 60\nxor rdi, rdi\nsyscall\n"
    payload = {"source": source_code}

    try:
        response = requests.post(GATEWAY_URL, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the gateway at {GATEWAY_URL}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 for valid assembly, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got: {response.text}")

    assert "hash" in data, "Response JSON is missing the 'hash' key."

    # Compute the expected hash locally
    with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False) as f:
        f.write(source_code)
        asm_file = f.name

    obj_file = asm_file.replace('.asm', '.o')

    try:
        subprocess.run(['nasm', '-f', 'elf64', asm_file, '-o', obj_file], check=True, capture_output=True)
        with open(obj_file, 'rb') as f:
            obj_bytes = f.read()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Local nasm compilation failed during test setup: {e.stderr.decode()}")
    finally:
        if os.path.exists(asm_file):
            os.remove(asm_file)
        if os.path.exists(obj_file):
            os.remove(obj_file)

    expected_hash = hashlib.sha256(obj_bytes + SEED_VALUE).hexdigest()

    assert data["hash"] == expected_hash, f"Hash mismatch. Expected {expected_hash}, but got {data['hash']}."