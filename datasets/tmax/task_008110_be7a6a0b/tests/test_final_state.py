# test_final_state.py

import os
import stat
import pytest
from urllib.parse import urlparse, parse_qs

def test_client2_key_permissions():
    key_path = "/home/user/certs/client2.key"
    assert os.path.isfile(key_path), f"File {key_path} is missing."

    mode = os.stat(key_path).st_mode
    perms = stat.S_IMODE(mode)

    assert perms in (0o400, 0o600), f"Permissions for {key_path} are {oct(perms)}, expected 0o400 or 0o600."

def test_exploit_sh_exists_and_executable():
    script_path = "/home/user/exploit.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    # Check if executable by owner
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_exploit_sh_content():
    script_path = "/home/user/exploit.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    # Recompute the expected signature
    payload = "http://evil.com/exploit"
    xor_key = 0x42
    expected_sig = "".join(f"{ord(c) ^ xor_key:02x}" for c in payload)

    # Check for required curl arguments
    assert "curl " in content, "The script must contain a curl command."
    assert "--cacert /home/user/certs/ca.crt" in content, "Missing or incorrect --cacert argument."
    assert "--cert /home/user/certs/client2.crt" in content, "Missing or incorrect --cert argument."
    assert "--key /home/user/certs/client2.key" in content, "Missing or incorrect --key argument."

    # Extract the URL from the curl command
    # We look for the string starting with https://localhost:8443/login
    url_start = content.find("https://localhost:8443/login")
    assert url_start != -1, "The target URL https://localhost:8443/login is missing in the curl command."

    # Extract the URL part (assuming it ends with a quote or space)
    url_substring = content[url_start:]
    end_idx = -1
    for i, char in enumerate(url_substring):
        if char in ('"', "'", " ", "\n"):
            end_idx = i
            break

    if end_idx != -1:
        full_url = url_substring[:end_idx]
    else:
        full_url = url_substring

    parsed_url = urlparse(full_url)
    query_params = parse_qs(parsed_url.query)

    assert "redirect" in query_params, "The 'redirect' query parameter is missing."
    assert query_params["redirect"][0] == payload, f"Expected redirect parameter to be {payload}."

    assert "sig" in query_params, "The 'sig' query parameter is missing."
    assert query_params["sig"][0] == expected_sig, f"Expected sig parameter to be {expected_sig}."