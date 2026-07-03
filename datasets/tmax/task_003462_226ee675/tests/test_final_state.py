# test_final_state.py

import os
import pytest

def test_exploit_rs_exists():
    path = "/home/user/exploit.rs"
    assert os.path.isfile(path), f"File {path} does not exist. You must write your Rust program here."

def test_final_payload_exists():
    path = "/home/user/final_payload.txt"
    assert os.path.isfile(path), f"File {path} does not exist. You must save the output of your program here."

def test_final_payload_content():
    path = "/home/user/final_payload.txt"

    # Calculate expected token
    admin_user = "admin"
    salt = "r3dt3am_s4lt"
    expected_plain = f"{admin_user}:{salt}"
    expected_token = "".join(chr(ord(c) + 3) for c in expected_plain)

    # The payload needs to bypass `.replace("<script>", "").replace("</script>", "")`
    # and result in `<script>alert('pwned')</script>`
    # One valid payload is `<scr<script>ipt>alert('pwned')</scr</script>ipt>`
    # However, there are multiple ways to construct it (e.g., `<<script>script>`).
    # We will test if the payload part bypasses the sanitizer correctly.

    with open(path, "r") as f:
        content = f.read().strip()

    assert "|" in content, "The final_payload.txt must contain the format TOKEN|PAYLOAD."

    parts = content.split("|", 1)
    token = parts[0]
    payload = parts[1]

    assert token == expected_token, f"The generated token is incorrect. Expected {expected_token}, got {token}."

    # Simulate the sanitization process
    sanitized = payload.replace("<script>", "").replace("</script>", "")
    expected_sanitized = "<script>alert('pwned')</script>"

    assert sanitized == expected_sanitized, f"The payload did not bypass the XSS filter correctly. After sanitization, expected {expected_sanitized}, but got {sanitized}."