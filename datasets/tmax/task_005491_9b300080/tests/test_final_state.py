# test_final_state.py

import os
import re
import json
import base64
import hmac
import hashlib
import pytest

def decode_b64url(data):
    # Add padding if necessary
    pad = len(data) % 4
    if pad:
        data += '=' * (4 - pad)
    return base64.urlsafe_b64decode(data)

def extract_secret_from_elf(filepath):
    with open(filepath, 'rb') as f:
        content = f.read()

    # Look for the prefix and extract the null-terminated string
    match = re.search(b'KEY_MATERIAL_([^\x00]+)\x00', content)
    if match:
        return match.group(1).decode('utf-8')
    return None

def analyze_logs(log_path, secret_key):
    with open(log_path, 'r') as f:
        content = f.read()

    # Extract all session_token values
    tokens = re.findall(r'session_token=([a-zA-Z0-9_\-\.]+)', content)

    forged_count = 0
    admin_pin = None

    for token in tokens:
        parts = token.split('.')
        if len(parts) < 2:
            continue

        try:
            header_json = decode_b64url(parts[0]).decode('utf-8')
            header = json.loads(header_json)

            payload_json = decode_b64url(parts[1]).decode('utf-8')
            payload = json.loads(payload_json)
        except Exception:
            continue

        alg = header.get('alg', '').lower()

        if alg == 'none':
            forged_count += 1
        elif alg == 'hs256' and len(parts) == 3 and secret_key:
            # Verify signature
            msg = f"{parts[0]}.{parts[1]}"
            expected_sig = base64.urlsafe_b64encode(
                hmac.new(secret_key.encode(), msg.encode(), hashlib.sha256).digest()
            ).decode('utf-8').rstrip('=')

            if parts[2] == expected_sig and payload.get('user') == 'admin':
                pin_hash = payload.get('pin_hash')
                if pin_hash:
                    # Brute-force 4-digit PIN
                    for i in range(10000):
                        pin = f"{i:04d}"
                        if hashlib.md5(pin.encode()).hexdigest() == pin_hash:
                            admin_pin = pin
                            break

    return forged_count, admin_pin

def test_report_exists():
    assert os.path.isfile('/home/user/report.txt'), "/home/user/report.txt does not exist. The C++ program must generate this file."

def test_report_contents():
    elf_path = '/home/user/audit_data/auth_daemon'
    log_path = '/home/user/audit_data/requests.log'

    assert os.path.isfile(elf_path), "auth_daemon binary is missing for verification"
    assert os.path.isfile(log_path), "requests.log is missing for verification"

    # Derive truth values
    expected_secret = extract_secret_from_elf(elf_path)
    assert expected_secret is not None, "Could not extract secret from auth_daemon for verification"

    expected_forged, expected_pin = analyze_logs(log_path, expected_secret)
    assert expected_pin is not None, "Could not determine expected admin PIN for verification"

    # Read student report
    with open('/home/user/report.txt', 'r') as f:
        lines = [line.strip() for line in f.read().strip().split('\n')]

    assert len(lines) == 3, f"Expected exactly 3 lines in report.txt, found {len(lines)}"

    assert lines[0] == expected_secret, f"Line 1 (secret key) is incorrect. Expected {expected_secret}, got {lines[0]}"
    assert lines[1] == str(expected_forged), f"Line 2 (forged count) is incorrect. Expected {expected_forged}, got {lines[1]}"
    assert lines[2] == expected_pin, f"Line 3 (admin PIN) is incorrect. Expected {expected_pin}, got {lines[2]}"