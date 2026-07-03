# test_final_state.py

import os
import pytest

def test_exploit_source_exists():
    """Verify that the student wrote the exploit source code."""
    path = "/home/user/exploit.cpp"
    assert os.path.isfile(path), f"Exploit source code is missing at {path}"
    assert os.path.getsize(path) > 0, f"Exploit source code at {path} is empty"

def test_exploit_binary_exists_and_executable():
    """Verify that the exploit was compiled and is executable."""
    path = "/home/user/exploit"
    assert os.path.isfile(path), f"Compiled exploit binary is missing at {path}"
    assert os.access(path, os.X_OK), f"Compiled exploit binary at {path} is not executable"

def test_forged_token_correct():
    """Verify that the forged token matches the expected XORed and hex-encoded output."""
    token_path = "/home/user/forged_token.txt"
    key_path = "/home/user/ssh_keys/service_ed25519.pub"

    assert os.path.isfile(token_path), f"Forged token file is missing at {token_path}"
    assert os.path.isfile(key_path), f"SSH public key file is missing at {key_path}"

    with open(key_path, "rb") as f:
        key = f.read()

    payload = b"admin|root|NONE"

    # Recompute the expected XORed hex string
    xored = bytes(p ^ key[i % len(key)] for i, p in enumerate(payload))
    expected_hex = xored.hex().upper()

    with open(token_path, "r") as f:
        actual_hex = f.read().strip().upper()

    assert actual_hex == expected_hex, (
        f"The forged token in {token_path} is incorrect. "
        f"Expected {expected_hex}, but got {actual_hex}."
    )