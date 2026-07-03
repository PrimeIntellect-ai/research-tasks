# test_final_state.py

import os
import base64
import hashlib

def extract_key(binary_path):
    with open(binary_path, "rb") as f:
        content = f.read()

    prefix = b"XOR_KEY="
    idx = content.find(prefix)
    assert idx != -1, f"Could not find {prefix} in {binary_path}"

    key = content[idx + len(prefix) : idx + len(prefix) + 8]
    assert len(key) == 8, "Extracted key is less than 8 bytes"
    return key

def test_audit_trail_log_correctness():
    log_path = "/home/user/audit_trail.log"
    tokens_path = "/home/user/tokens.txt"
    binary_path = "/home/user/legacy_auth"

    assert os.path.isfile(log_path), f"The file {log_path} does not exist."
    assert os.path.isfile(tokens_path), f"The file {tokens_path} does not exist."
    assert os.path.isfile(binary_path), f"The file {binary_path} does not exist."

    key = extract_key(binary_path)

    with open(tokens_path, "r") as f:
        tokens = [line.strip() for line in f if line.strip()]

    expected_lines = []
    for token in tokens:
        decoded = base64.b64decode(token)
        decrypted = bytearray()
        for i, b in enumerate(decoded):
            decrypted.append(b ^ key[i % len(key)])

        decrypted_hex = decrypted.hex()
        sha256_hex = hashlib.sha256(decrypted).hexdigest()

        expected_line = f"Original: {token} | DecryptedHex: {decrypted_hex} | SHA256: {sha256_hex}"
        expected_lines.append(expected_line)

    with open(log_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {log_path}, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in {log_path} is incorrect.\nExpected: {expected}\nActual:   {actual}"