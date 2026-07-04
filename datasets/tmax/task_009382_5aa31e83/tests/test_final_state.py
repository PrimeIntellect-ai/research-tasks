# test_final_state.py

import os
import pytest

def generate_response(password: str, challenge: str) -> str:
    """Custom FNV-1a inspired weak hash for IoT authentication."""
    state = 0x811C9DC5
    for char in password + challenge:
        state = (state ^ ord(char)) * 0x01000193
        state &= 0xFFFFFFFF
    return f"{state:08x}"

def test_admin_response_correct():
    # 1. Parse traffic_capture.log to find the successful admin auth
    log_path = "/home/user/traffic_capture.log"
    assert os.path.exists(log_path), f"Missing file: {log_path}"

    with open(log_path, "r") as f:
        lines = f.readlines()

    admin_chal = None
    admin_resp = None

    for i, line in enumerate(lines):
        if "AUTH_REQ user=admin" in line:
            if i + 1 < len(lines) and "AUTH_CHAL" in lines[i+1]:
                admin_chal = lines[i+1].split("chal=")[1].strip()
            if i + 2 < len(lines) and "AUTH_RESP" in lines[i+2]:
                admin_resp = lines[i+2].split("resp=")[1].strip()
            if i + 3 < len(lines) and "AUTH_SUCCESS" in lines[i+3]:
                break

    assert admin_chal is not None, "Could not find admin challenge in traffic_capture.log"
    assert admin_resp is not None, "Could not find admin response in traffic_capture.log"

    # 2. Find password from wordlist
    wordlist_path = "/home/user/wordlist.txt"
    assert os.path.exists(wordlist_path), f"Missing file: {wordlist_path}"

    found_password = None
    with open(wordlist_path, "r") as f:
        for word in f:
            word = word.strip()
            if not word:
                continue
            if generate_response(word, admin_chal) == admin_resp:
                found_password = word
                break

    assert found_password is not None, f"Could not crack admin password using {wordlist_path}"

    # 3. Read next challenge
    next_chal_path = "/home/user/next_challenge.txt"
    assert os.path.exists(next_chal_path), f"Missing file: {next_chal_path}"
    with open(next_chal_path, "r") as f:
        next_chal = f.read().strip()

    # 4. Calculate expected response
    expected_resp = generate_response(found_password, next_chal)

    # 5. Check admin_response.txt
    resp_path = "/home/user/admin_response.txt"
    assert os.path.exists(resp_path), f"File {resp_path} does not exist. Task incomplete."

    with open(resp_path, "r") as f:
        actual_resp = f.read()

    assert actual_resp == expected_resp, (
        f"Incorrect response in {resp_path}. "
        f"Expected '{expected_resp}' (derived from password '{found_password}' and challenge '{next_chal}'), "
        f"but got '{actual_resp}'."
    )