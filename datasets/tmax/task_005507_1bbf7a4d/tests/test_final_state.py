# test_final_state.py

import os
import pytest

def decode_payload(hex_str: str) -> str:
    """Decodes the hex payload using the XOR key 0x5A."""
    try:
        raw_bytes = bytes.fromhex(hex_str)
        return bytes([b ^ 0x5A for b in raw_bytes]).decode('utf-8')
    except Exception as e:
        pytest.fail(f"Failed to decode payload {hex_str} during test setup: {e}")

def resolve_path(decoded_str: str) -> str:
    """Resolves the path relative to the simulated sandbox directory."""
    # os.path.normpath resolves '..' and '.' 
    # os.path.join safely appends the relative path to the base
    # Note: if decoded_str starts with '/', os.path.join discards the base,
    # but based on the problem description, these are treated as relative paths.
    # To strictly treat it as appended, we can strip leading slashes if any.
    clean_str = decoded_str.lstrip('/')
    return os.path.normpath(os.path.join('/var/www/uploads', clean_str))

def test_escapes_log_correctness():
    payloads_path = "/home/user/payloads.txt"
    log_path = "/home/user/escapes.log"

    assert os.path.isfile(payloads_path), f"Input file {payloads_path} is missing."
    assert os.path.isfile(log_path), f"Output file {log_path} is missing. Did you run your analyzer?"

    with open(payloads_path, "r") as f:
        payloads = [line.strip() for line in f if line.strip()]

    expected_log_lines = []
    base_dir = "/var/www/uploads"
    base_dir_prefix = base_dir + "/"

    for payload in payloads:
        decoded = decode_payload(payload)
        resolved = resolve_path(decoded)

        # Check if it escapes the sandbox
        # It escapes if it doesn't start with /var/www/uploads/ and isn't exactly /var/www/uploads
        if not (resolved == base_dir or resolved.startswith(base_dir_prefix)):
            expected_log_lines.append(f"{payload} -> {decoded} -> {resolved}")

    with open(log_path, "r") as f:
        actual_log_lines = [line.strip() for line in f if line.strip()]

    assert actual_log_lines == expected_log_lines, (
        f"Contents of {log_path} do not match the expected output.\n"
        f"Expected:\n" + "\n".join(expected_log_lines) + "\n\n"
        f"Actual:\n" + "\n".join(actual_log_lines)
    )