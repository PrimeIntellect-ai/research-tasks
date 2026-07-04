# test_final_state.py

import os
import json
import subprocess
import pytest

PAYLOAD_FILE = "/home/user/payload.hex"
KEY = b"REDSQUADRONKEY12"
IV = b"INITIALVECTOR123"

def decrypt_aes_cbc(hex_data: str, key: bytes, iv: bytes) -> bytes:
    key_hex = key.hex()
    iv_hex = iv.hex()

    try:
        bin_data = bytes.fromhex(hex_data)
    except ValueError:
        raise ValueError("Payload is not a valid hex string.")

    process = subprocess.run(
        ["openssl", "enc", "-d", "-aes-128-cbc", "-K", key_hex, "-iv", iv_hex],
        input=bin_data,
        capture_output=True
    )
    if process.returncode != 0:
        raise ValueError(f"Decryption failed: {process.stderr.decode(errors='ignore')}")

    return process.stdout

def test_payload_file_exists():
    assert os.path.exists(PAYLOAD_FILE), f"File {PAYLOAD_FILE} does not exist."

def test_payload_contents():
    with open(PAYLOAD_FILE, "r") as f:
        hex_data = f.read().strip()

    assert hex_data, "Payload file is empty."

    try:
        plaintext_bytes = decrypt_aes_cbc(hex_data, KEY, IV)
    except Exception as e:
        pytest.fail(f"Failed to decrypt payload: {e}")

    try:
        plaintext = plaintext_bytes.decode('utf-8')
        data = json.loads(plaintext)
    except Exception as e:
        pytest.fail(f"Decrypted plaintext is not valid JSON: {e}")

    assert data.get("username") == "admin", "Username is not admin."

    bio = data.get("bio", "")
    bio_lower = bio.lower()

    blocked = ["script", "onload", "onerror", "javascript:", "eval"]
    for b in blocked:
        assert b not in bio_lower, f"Payload contains blocked WAF keyword: {b}"

    assert "<details" in bio_lower, "Payload missing <details> tag."
    assert "ontoggle=" in bio_lower.replace(" ", ""), "Payload missing ontoggle attribute."
    assert "console.log(document.cookie)" in bio, "Payload does not execute exact required JS."
    assert "open" in bio_lower, "Payload missing 'open' attribute to trigger automatically."