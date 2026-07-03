# test_final_state.py

import os
import re
import base64
import hmac
import hashlib

def extract_secret(binary_path):
    with open(binary_path, "rb") as f:
        data = f.read()
    match = re.search(b"COMPLIANCE_KEY_[A-Za-z0-9_]+", data)
    if not match:
        raise ValueError("Could not find COMPLIANCE_KEY_ in binary")
    return match.group(0)

def is_valid_jwt(token, secret):
    parts = token.split('.')
    if len(parts) != 3:
        return False
    header_payload = f"{parts[0]}.{parts[1]}".encode('utf-8')
    expected_sig = base64.urlsafe_b64encode(
        hmac.new(secret, header_payload, hashlib.sha256).digest()
    ).decode('utf-8').rstrip('=')
    return hmac.compare_digest(expected_sig, parts[2])

def process_line(line, secret):
    def replacer(m):
        token = m.group(1)
        if is_valid_jwt(token, secret):
            return "--token [REDACTED]"
        return m.group(0)
    return re.sub(r'--token\s+(\S+)', replacer, line)

def test_audit_redactor_script_exists():
    script_path = "/home/user/audit_redactor.py"
    assert os.path.exists(script_path), f"The script {script_path} was not found."
    assert os.path.isfile(script_path), f"{script_path} should be a file."

def test_clean_audit_log_correctness():
    raw_log_path = "/home/user/raw_audit.log"
    clean_log_path = "/home/user/clean_audit.log"
    binary_path = "/home/user/legacy_worker"

    assert os.path.exists(clean_log_path), f"The output log {clean_log_path} was not found."

    secret = extract_secret(binary_path)

    with open(raw_log_path, "r") as f:
        raw_lines = f.readlines()

    expected_lines = [process_line(line, secret) for line in raw_lines]
    expected_content = "".join(expected_lines)

    with open(clean_log_path, "r") as f:
        actual_content = f.read()

    assert actual_content == expected_content, (
        f"The content of {clean_log_path} does not match the expected redacted output. "
        "Ensure only valid JWTs signed with the extracted secret are redacted."
    )