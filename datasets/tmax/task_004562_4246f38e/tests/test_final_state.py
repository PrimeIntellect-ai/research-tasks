# test_final_state.py
import os
import json
import urllib.request
import urllib.error

def test_flag_file_exists_and_correct():
    """Verify that the flag file exists and contains the correct flag."""
    flag_path = '/home/user/flag.txt'
    assert os.path.isfile(flag_path), f"Flag file not found at {flag_path}"

    with open(flag_path, 'r') as f:
        content = f.read().strip()

    expected_flag = "FLAG{cbc_b1t_fl1pp1ng_m4st3r}"
    assert content == expected_flag, f"Flag file content is incorrect. Expected '{expected_flag}', got '{content}'"

def test_payload_file_and_validity():
    """Verify that the payload file exists and contains a valid token that bypasses the WAF."""
    payload_path = '/home/user/payload.txt'
    assert os.path.isfile(payload_path), f"Payload file not found at {payload_path}"

    with open(payload_path, 'r') as f:
        token = f.read().strip()

    assert ':' in token, "Payload token must be in the format 'hex_iv:hex_ciphertext'"

    # Verify the token against the running server
    url = 'http://127.0.0.1:8080/submit'
    data = json.dumps({"token": token}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req) as response:
            resp_data = json.loads(response.read().decode('utf-8'))
            assert resp_data.get('status') == 'success', f"Server rejected the payload token. Response: {resp_data}"
            assert resp_data.get('message') == 'Evasion successful!', "Payload did not trigger the expected success message."
    except urllib.error.URLError as e:
        if hasattr(e, 'read'):
            error_body = e.read().decode('utf-8')
            assert False, f"Failed to submit payload to server. HTTP Error {e.code}: {error_body}"
        else:
            assert False, f"Failed to connect to server at {url}: {e.reason}"