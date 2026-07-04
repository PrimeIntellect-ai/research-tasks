# test_final_state.py

import os
import base64
import subprocess
import tempfile
import pytest

def get_rogue_key_fingerprint():
    auth_keys_path = "/home/user/.ssh/authorized_keys"
    valid_keys_path = "/home/user/evidence/valid_keys.pub"

    with open(auth_keys_path, "r") as f:
        auth_keys = set(line.strip() for line in f if line.strip())

    with open(valid_keys_path, "r") as f:
        valid_keys = set(line.strip() for line in f if line.strip())

    rogue_keys = list(auth_keys - valid_keys)
    assert len(rogue_keys) == 1, f"Expected exactly 1 rogue key, found {len(rogue_keys)}"

    rogue_key = rogue_keys[0]

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_key_file:
        temp_key_file.write(rogue_key + "\n")
        temp_key_path = temp_key_file.name

    try:
        result = subprocess.run(
            ['ssh-keygen', '-l', '-E', 'md5', '-f', temp_key_path], 
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    finally:
        os.remove(temp_key_path)

def get_malicious_url():
    payload_path = "/home/user/evidence/payload.b64"
    with open(payload_path, "r") as f:
        encoded_payload = f.read().strip()

    decoded_payload = base64.b64decode(encoded_payload).decode('utf-8')
    urls = decoded_payload.split(',')

    malicious_urls = [url for url in urls if url.endswith('.xyz') or url.endswith('.ru')]
    assert len(malicious_urls) == 1, f"Expected exactly 1 malicious URL, found {len(malicious_urls)}"

    return malicious_urls[0]

def test_forensics_report():
    report_path = "/home/user/forensics_report.txt"
    assert os.path.exists(report_path), f"Report file not found at {report_path}"

    expected_fingerprint = get_rogue_key_fingerprint()
    expected_url = get_malicious_url()

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Report must contain exactly two non-empty lines, found {len(lines)}"

    assert lines[0] == expected_fingerprint, f"Line 1 mismatch. Expected '{expected_fingerprint}', got '{lines[0]}'"
    assert lines[1] == expected_url, f"Line 2 mismatch. Expected '{expected_url}', got '{lines[1]}'"