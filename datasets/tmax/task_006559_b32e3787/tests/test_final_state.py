# test_final_state.py
import os
import base64
import subprocess

def test_decoded_payload_bin():
    path = "/home/user/decoded_payload.bin"
    assert os.path.isfile(path), f"File {path} does not exist."

    expected_b64 = "YmFkZ3V5OmludHJ1ZGVyAAAAAAAAAAAAAAAAAAAAAAAB"
    expected_bytes = base64.b64decode(expected_b64)

    with open(path, "rb") as f:
        content = f.read()

    assert content == expected_bytes, f"Contents of {path} do not match the expected decoded payload."

def test_token_validator_fixed_c_exists():
    path = "/home/user/token_validator_fixed.c"
    assert os.path.isfile(path), f"File {path} does not exist."

def test_token_validator_fixed_binary():
    path = "/home/user/token_validator_fixed"
    assert os.path.isfile(path), f"Binary {path} does not exist."
    assert os.access(path, os.X_OK), f"Binary {path} is not executable."

def test_token_validator_fixed_behavior_short():
    path = "/home/user/token_validator_fixed"
    result = subprocess.run([path, "short_token"], capture_output=True, text=True)
    assert result.returncode == 0, f"Expected return code 0 for short token, got {result.returncode}"
    assert result.stdout == "Access Granted: User\n", f"Expected 'Access Granted: User\\n', got {repr(result.stdout)}"

def test_token_validator_fixed_behavior_attacker():
    path = "/home/user/token_validator_fixed"
    payload_path = "/home/user/decoded_payload.bin"
    assert os.path.isfile(payload_path), f"Missing {payload_path} required for this test."

    with open(payload_path, "rb") as f:
        payload = f.read()

    result = subprocess.run([path, payload], capture_output=True)
    assert result.returncode == 1, f"Expected return code 1 for attacker payload, got {result.returncode}"
    assert result.stdout == b"Error: Token too long\n", f"Expected 'Error: Token too long\\n', got {repr(result.stdout)}"

def test_token_validator_fixed_behavior_exact_32():
    path = "/home/user/token_validator_fixed"
    payload = "12345678901234567890123456789012"
    result = subprocess.run([path, payload], capture_output=True, text=True)
    assert result.returncode == 1, f"Expected return code 1 for exactly 32-byte token, got {result.returncode}"
    assert result.stdout == "Error: Token too long\n", f"Expected 'Error: Token too long\\n', got {repr(result.stdout)}"