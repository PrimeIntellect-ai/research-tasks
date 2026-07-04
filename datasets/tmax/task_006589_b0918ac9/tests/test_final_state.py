# test_final_state.py

import os
import re

def test_attacker_ips():
    log_path = "/home/user/upload.log"
    ips_path = "/home/user/attacker_ips.txt"

    assert os.path.exists(log_path), f"Original log file {log_path} is missing."
    assert os.path.exists(ips_path), f"Output file {ips_path} is missing."

    expected_ips = set()
    with open(log_path, 'r') as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 3:
                ip = parts[0]
                path = parts[2]
                if "../" in path:
                    expected_ips.add(ip)

    expected_ips_sorted = sorted(list(expected_ips))

    with open(ips_path, 'r') as f:
        actual_ips = [line.strip() for line in f if line.strip()]

    assert actual_ips == expected_ips_sorted, f"Expected IPs {expected_ips_sorted}, but got {actual_ips} in {ips_path}."

def test_upload_clean_log():
    log_path = "/home/user/upload.log"
    clean_log_path = "/home/user/upload_clean.log"

    assert os.path.exists(log_path), f"Original log file {log_path} is missing."
    assert os.path.exists(clean_log_path), f"Cleaned log file {clean_log_path} is missing."

    with open(log_path, 'r') as f:
        original_content = f.read()

    # Replace AKIA followed by 16 uppercase alphanumeric characters with [REDACTED]
    expected_clean_content = re.sub(r'AKIA[A-Z0-9]{16}', '[REDACTED]', original_content)

    with open(clean_log_path, 'r') as f:
        actual_clean_content = f.read()

    assert actual_clean_content == expected_clean_content, f"The content of {clean_log_path} does not match the expected redacted content."

def test_new_creds_decrypted():
    creds_path = "/home/user/new_creds.txt"

    assert os.path.exists(creds_path), f"Decrypted credentials file {creds_path} is missing."

    with open(creds_path, 'r') as f:
        actual_creds = f.read().strip()

    expected_creds = "SUPER_SECRET_ROTATED_CREDENTIALS_99283"
    assert actual_creds == expected_creds, f"The decrypted credentials do not match the expected plaintext."