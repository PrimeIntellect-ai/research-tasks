# test_final_state.py

import os
import pytest

def test_payload_hex_exists_and_valid():
    payload_path = "/home/user/payload.hex"
    assert os.path.exists(payload_path), f"Missing file: {payload_path}"
    assert os.path.isfile(payload_path), f"Not a file: {payload_path}"

    with open(payload_path, "r") as f:
        hex_content = f.read().strip()

    assert hex_content, "payload.hex is empty"

    try:
        encrypted_bytes = bytes.fromhex(hex_content)
    except ValueError:
        pytest.fail("payload.hex does not contain a valid hex string")

    key = bytes([0xDE, 0xAD, 0xBE, 0xEF])

    decrypted_bytes = bytearray()
    for i, b in enumerate(encrypted_bytes):
        decrypted_bytes.append(b ^ key[i % 4])

    # Convert to string (ignoring errors for the prefix if it's binary, but it should be a string)
    decrypted_str = decrypted_bytes.decode('utf-8', errors='replace')

    # Check that the first 16 bytes do not contain '../'
    prefix = decrypted_str[:16]
    assert "../" not in prefix, f"Sanitization bypass failed: first 16 bytes contain '../'. Prefix: {prefix}"

    # Check that the decrypted payload contains the required path traversal string
    assert "../../../etc/shadow" in decrypted_str, "Decrypted payload does not contain '../../../etc/shadow'"