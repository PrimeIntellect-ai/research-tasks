# test_final_state.py

import os
import json
import base64
import re
import subprocess
import pytest
from datetime import datetime

def decode_base64url(data):
    """Decode base64url encoded string."""
    data = data.replace('-', '+').replace('_', '/')
    padding = len(data) % 4
    if padding:
        data += '=' * (4 - padding)
    try:
        return base64.b64decode(data).decode('utf-8')
    except Exception:
        return ""

def get_expected_expired_cn():
    """Find the expired certificate in /home/user/certs/ and return its CN."""
    certs_dir = "/home/user/certs"
    expired_cns = []

    if not os.path.exists(certs_dir):
        return None

    for filename in os.listdir(certs_dir):
        if filename.endswith(".pem"):
            filepath = os.path.join(certs_dir, filename)
            # Check end dates
            try:
                end_date_str = subprocess.check_output(
                    ["openssl", "x509", "-enddate", "-noout", "-in", filepath],
                    stderr=subprocess.DEVNULL
                ).decode('utf-8').strip().split('=')[1]

                end_date = datetime.strptime(end_date_str, "%b %d %H:%M:%S %Y %Z")

                if end_date < datetime.utcnow():
                    # Extract CN
                    subject_str = subprocess.check_output(
                        ["openssl", "x509", "-subject", "-noout", "-in", filepath],
                        stderr=subprocess.DEVNULL
                    ).decode('utf-8').strip()

                    # Parse CN from subject line (e.g., subject=C = US, ST = CA, L = SF, O = Org, CN = legacy-api.internal.com)
                    match = re.search(r'CN\s*=\s*([^,\n]+)', subject_str)
                    if match:
                        expired_cns.append(match.group(1).strip())
            except Exception:
                continue

    return expired_cns[0] if expired_cns else None

def get_expected_vulnerable_subjects():
    """Parse access.log to find vulnerable JWT subjects."""
    log_path = "/home/user/access.log"
    if not os.path.exists(log_path):
        return []

    vulnerable_subjects = []

    with open(log_path, 'r') as f:
        for line in f:
            # Find Bearer token
            match = re.search(r'Bearer\s+([a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.?[a-zA-Z0-9_-]*)', line)
            if match:
                token = match.group(1)
                parts = token.split('.')
                if len(parts) >= 2:
                    header_str = decode_base64url(parts[0])
                    payload_str = decode_base64url(parts[1])

                    try:
                        header = json.loads(header_str)
                        if header.get('alg', '').lower() == 'none':
                            payload = json.loads(payload_str)
                            if 'sub' in payload:
                                vulnerable_subjects.append(payload['sub'])
                    except json.JSONDecodeError:
                        continue

    return sorted(vulnerable_subjects)

def test_expired_cert_file_exists():
    assert os.path.isfile("/home/user/expired_cert.txt"), "The file /home/user/expired_cert.txt was not created."

def test_expired_cert_content():
    expected_cn = get_expected_expired_cn()
    assert expected_cn is not None, "Could not determine the expected expired certificate CN from /home/user/certs/."

    with open("/home/user/expired_cert.txt", "r") as f:
        content = f.read().strip()

    assert content == expected_cn, f"Expected /home/user/expired_cert.txt to contain '{expected_cn}', but got '{content}'."

def test_scan_jwts_script_exists_and_executable():
    script_path = "/home/user/scan_jwts.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_vulnerable_subjects_file_exists():
    assert os.path.isfile("/home/user/vulnerable_subjects.txt"), "The file /home/user/vulnerable_subjects.txt was not created."

def test_vulnerable_subjects_content():
    expected_subjects = get_expected_vulnerable_subjects()

    with open("/home/user/vulnerable_subjects.txt", "r") as f:
        actual_subjects = [line.strip() for line in f if line.strip()]

    assert actual_subjects == expected_subjects, (
        f"Expected vulnerable subjects to be {expected_subjects}, "
        f"but got {actual_subjects}. Ensure the output is sorted alphabetically and contains only the subjects."
    )