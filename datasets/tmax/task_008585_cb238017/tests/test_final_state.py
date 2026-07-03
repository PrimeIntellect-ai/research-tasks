# test_final_state.py

import os
import stat
import base64
import pytest

def test_admin_id_rsa_exists_and_permissions():
    path = "/home/user/admin_id_rsa"
    assert os.path.isfile(path), f"File {path} does not exist."

    st = os.stat(path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"File {path} has permissions {oct(perms)}, expected 0o600."

def test_admin_id_rsa_content():
    path = "/home/user/admin_id_rsa"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    expected_header = "-----BEGIN OPENSSH PRIVATE KEY-----"
    expected_footer = "-----END OPENSSH PRIVATE KEY-----"
    expected_body = "b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW\nQyNTUxOQAAACBA1/1+xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    assert expected_header in content, f"{path} is missing the SSH private key header."
    assert expected_footer in content, f"{path} is missing the SSH private key footer."
    assert expected_body in content.replace("\r", ""), f"{path} does not contain the correct mock key material."

def test_forged_token_exists_and_valid():
    path = "/home/user/forged_token.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        token = f.read().strip()

    assert token, f"File {path} is empty."

    parts = token.split(".")
    assert len(parts) >= 2, f"Token in {path} does not appear to be a valid JWT (missing dots)."

    header_b64 = parts[0]
    payload_b64 = parts[1]

    # Add padding if necessary for python's base64 decoder
    header_b64 += "=" * ((4 - len(header_b64) % 4) % 4)
    payload_b64 += "=" * ((4 - len(payload_b64) % 4) % 4)

    try:
        header_bytes = base64.urlsafe_b64decode(header_b64)
        header_str = header_bytes.decode('utf-8', errors='ignore')
    except Exception as e:
        pytest.fail(f"Failed to Base64URL decode the token header: {e}")

    try:
        payload_bytes = base64.urlsafe_b64decode(payload_b64)
        payload_str = payload_bytes.decode('utf-8', errors='ignore')
    except Exception as e:
        pytest.fail(f"Failed to Base64URL decode the token payload: {e}")

    header_no_spaces = header_str.replace(" ", "")
    payload_no_spaces = payload_str.replace(" ", "")

    assert '"alg":"none"' in header_no_spaces, f"Token header does not contain 'alg: none'. Found: {header_str}"
    assert '"role":"admin"' in payload_no_spaces, f"Token payload does not contain 'role: admin'. Found: {payload_str}"