# test_final_state.py
import os
import re
import hashlib

def test_flag_file():
    flag_path = "/home/user/flag.txt"
    assert os.path.exists(flag_path), f"Missing required file: {flag_path}"
    assert os.path.isfile(flag_path), f"Path is not a file: {flag_path}"

    with open(flag_path, 'r') as f:
        content = f.read().strip()

    expected_flag = "FLAG{jwt_alg_none_byp4ss_1337}"
    assert content == expected_flag, f"Incorrect flag in {flag_path}. Expected '{expected_flag}', got '{content}'"

def test_redacted_logs():
    original_path = "/home/user/api_logs.txt"
    redacted_path = "/home/user/redacted_logs.txt"

    assert os.path.exists(original_path), f"Original log file missing: {original_path}"
    assert os.path.exists(redacted_path), f"Redacted log file missing: {redacted_path}"
    assert os.path.isfile(redacted_path), f"Path is not a file: {redacted_path}"

    with open(original_path, 'r') as f:
        original_content = f.read()

    # Regex for a JWT: three base64-url encoded segments separated by periods
    jwt_pattern = re.compile(r'[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+')
    expected_redacted_content = jwt_pattern.sub('[REDACTED_JWT]', original_content)

    with open(redacted_path, 'r') as f:
        actual_redacted_content = f.read()

    assert actual_redacted_content == expected_redacted_content, "The redacted logs do not match the expected output. Ensure all validly formatted JWTs are replaced with '[REDACTED_JWT]'."

def test_hash_file():
    redacted_path = "/home/user/redacted_logs.txt"
    hash_path = "/home/user/hash.txt"

    assert os.path.exists(redacted_path), f"Redacted log file missing: {redacted_path}"
    assert os.path.exists(hash_path), f"Hash file missing: {hash_path}"
    assert os.path.isfile(hash_path), f"Path is not a file: {hash_path}"

    with open(redacted_path, 'rb') as f:
        expected_hash = hashlib.sha256(f.read()).hexdigest()

    with open(hash_path, 'r') as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Hash mismatch in {hash_path}. Expected {expected_hash}, got {actual_hash}"