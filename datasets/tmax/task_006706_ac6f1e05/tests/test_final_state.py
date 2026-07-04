# test_final_state.py

import os
import json
import pytest

def test_rogue_ca_extracted():
    """Verify that the rogue CA Common Name was correctly identified and saved."""
    file_path = "/home/user/rogue_ca.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    expected_cn = "Evil Proxy Intercept CA"
    assert content == expected_cn, f"Expected '{expected_cn}' in {file_path}, but found '{content}'."

def test_payload_extracted():
    """Verify that the malicious payload was correctly decoded and saved."""
    file_path = "/home/user/payload.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    # We can verify it's valid JSON and contains the injection
    try:
        payload_json = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"The content in {file_path} is not valid JSON.")

    assert "username" in payload_json, "Payload JSON missing 'username' key."
    assert "role" in payload_json, "Payload JSON missing 'role' key."
    assert "$(cat /etc/passwd)" in payload_json["role"], "The payload does not contain the expected command injection string."

def test_exploit_script_exists():
    """Verify that the exploit script was created."""
    file_path = "/home/user/exploit.py"
    assert os.path.isfile(file_path), f"Exploit script {file_path} was not created."

def test_flag_extracted():
    """Verify that the flag was successfully retrieved from the vulnerable server."""
    file_path = "/home/user/flag.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    expected_flag = "FLAG{c0mm4nd_1nj3ct10n_byp4ss}"
    assert content == expected_flag, f"Incorrect flag found in {file_path}."