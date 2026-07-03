# test_final_state.py

import os
import stat
import pytest
import base64
import hashlib

def test_send_payload_script():
    script_path = "/home/user/send_payload.sh"

    # 1. Check that the script exists
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    # 2. Check that it is executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    # 3. Check for curl
    assert "curl" in content, "The script does not contain the 'curl' command."

    # 4. Check for the target URL
    assert "http://localhost:8000/admin" in content, "The script does not contain the correct target URL."

    # 5. Check for the custom header
    assert "X-Evasion-Mode: Active" in content, "The script does not contain the expected 'X-Evasion-Mode: Active' header."

    # Calculate the expected payload dynamically
    plaintext = "database"
    xor_bytes = bytes([ord(c) ^ 0x5A for c in plaintext])
    expected_payload = base64.b64encode(xor_bytes).decode('utf-8')

    # 6. Check for the encoded payload in the Session-Token cookie
    expected_cookie = f"Session-Token={expected_payload}"
    assert expected_cookie in content, f"The script does not contain the correct cookie payload. Expected to find '{expected_cookie}'."