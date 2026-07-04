# test_final_state.py

import os
import re
import hashlib
import subprocess
import pytest

RESULT_FILE = "/home/user/rotation_result.txt"
KEY_FILE = "/home/user/key.txt"
IV_FILE = "/home/user/iv.txt"
ACCESS_LOG = "/home/user/access.log"

def get_expected_leaked_token():
    # In a real scenario, we would parse the log, but we know the 200 OK log contains the token.
    # We can rely on the deterministic setup for the plaintext, but let's extract it logically
    # or just use the known plaintext from the prompt's truth data for validation.
    return "super_secret_admin_token_2023"

def test_result_file_exists():
    assert os.path.isfile(RESULT_FILE), f"The result file {RESULT_FILE} is missing."

def test_result_format_and_leaked_token():
    with open(RESULT_FILE, "r") as f:
        content = f.read()

    match = re.search(r"^Leaked:\s*(.+)$", content, re.MULTILINE)
    assert match is not None, "Could not find 'Leaked: <token>' in the result file."

    leaked_token = match.group(1).strip()
    assert leaked_token == get_expected_leaked_token(), f"Incorrect leaked token. Expected {get_expected_leaked_token()}, got {leaked_token}"

def test_result_new_hash():
    with open(RESULT_FILE, "r") as f:
        content = f.read()

    match = re.search(r"^New_Hash:\s*(.+)$", content, re.MULTILINE)
    assert match is not None, "Could not find 'New_Hash: <hash>' in the result file."

    actual_hash = match.group(1).strip()
    expected_new_token = get_expected_leaked_token() + "_rotated"
    expected_hash = hashlib.sha256(expected_new_token.encode('utf-8')).hexdigest()

    assert actual_hash == expected_hash, f"Incorrect New_Hash. Expected {expected_hash}, got {actual_hash}"

def test_result_new_encrypted_token():
    with open(RESULT_FILE, "r") as f:
        content = f.read()

    match = re.search(r"^New_Encrypted:\s*(.+)$", content, re.MULTILINE)
    assert match is not None, "Could not find 'New_Encrypted: <token>' in the result file."

    b64_encrypted = match.group(1).strip()

    # Read key and IV
    with open(KEY_FILE, "r") as f:
        key = f.read().strip()
    with open(IV_FILE, "r") as f:
        iv = f.read().strip()

    key_hex = key.encode('utf-8').hex()
    iv_hex = iv.encode('utf-8').hex()

    # Use openssl to decrypt the base64 string
    # openssl enc -d -aes-128-cbc -K <key_hex> -iv <iv_hex> -base64 -A
    process = subprocess.Popen(
        ['openssl', 'enc', '-d', '-aes-128-cbc', '-K', key_hex, '-iv', iv_hex, '-base64', '-A'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate(input=b64_encrypted.encode('utf-8'))

    assert process.returncode == 0, f"Failed to decrypt New_Encrypted token using openssl. Is it valid base64 and properly encrypted? Error: {stderr.decode()}"

    decrypted_new_token = stdout.decode('utf-8')
    expected_new_token = get_expected_leaked_token() + "_rotated"

    assert decrypted_new_token == expected_new_token, f"Decrypted new token does not match expected. Expected {expected_new_token}, got {decrypted_new_token}"