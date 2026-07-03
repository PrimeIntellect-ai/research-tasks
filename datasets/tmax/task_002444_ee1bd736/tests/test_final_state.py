# test_final_state.py

import os
import json
import re
import hashlib
import pytest

def get_expected_session_id():
    log_path = "/home/user/traffic.log"
    assert os.path.isfile(log_path), f"Missing required file: {log_path}"

    with open(log_path, 'r') as f:
        content = f.read()

    # Split by blank lines to get request/response blocks
    blocks = re.split(r'\n\s*\n', content.strip())

    for i, block in enumerate(blocks):
        if "Content-Security-Policy" in block and "'unsafe-inline'" in block:
            # The preceding block should be the request
            if i > 0:
                req_block = blocks[i-1]
                match = re.search(r'Cookie:\s*.*Session-Id=([A-Za-z0-9_]+)', req_block)
                if match:
                    return match.group(1)
    return None

def get_expected_cn():
    cert_path = "/home/user/cert.pem"
    assert os.path.isfile(cert_path), f"Missing required file: {cert_path}"

    with open(cert_path, 'r') as f:
        content = f.read()

    match = re.search(r'Subject:.*?CN=([A-Za-z0-9_]+)', content)
    if match:
        return match.group(1)
    return None

def get_expected_pins(cn):
    hashes_path = "/home/user/hashes.txt"
    assert os.path.isfile(hashes_path), f"Missing required file: {hashes_path}"

    with open(hashes_path, 'r') as f:
        target_hashes = [line.strip() for line in f if line.strip()]

    expected_pins = []
    # Precompute hashes for 0000-9999
    hash_to_pin = {}
    for i in range(10000):
        pin = f"{i:04d}"
        payload = (pin + cn).encode('utf-8')
        h = hashlib.sha256(payload).hexdigest()
        hash_to_pin[h] = pin

    for th in target_hashes:
        assert th in hash_to_pin, f"Hash {th} in hashes.txt does not correspond to a valid 4-digit PIN with salt {cn}"
        expected_pins.append(hash_to_pin[th])

    return expected_pins

def test_report_exists():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"The final report file was not found at {report_path}. Ensure your Rust program outputs to the correct absolute path."

def test_report_content():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Report file missing: {report_path}"

    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    # Derive expected truth dynamically
    expected_session_id = get_expected_session_id()
    assert expected_session_id is not None, "Could not derive expected session ID from traffic.log"

    expected_cn = get_expected_cn()
    assert expected_cn is not None, "Could not derive expected CN from cert.pem"

    expected_pins = get_expected_pins(expected_cn)

    # Assertions
    assert "vulnerable_session_id" in report_data, "Report JSON is missing the 'vulnerable_session_id' key."
    assert report_data["vulnerable_session_id"] == expected_session_id, \
        f"Expected vulnerable_session_id to be {expected_session_id}, but got {report_data['vulnerable_session_id']}."

    assert "certificate_cn" in report_data, "Report JSON is missing the 'certificate_cn' key."
    assert report_data["certificate_cn"] == expected_cn, \
        f"Expected certificate_cn to be {expected_cn}, but got {report_data['certificate_cn']}."

    assert "cracked_pins" in report_data, "Report JSON is missing the 'cracked_pins' key."
    assert isinstance(report_data["cracked_pins"], list), "'cracked_pins' must be a JSON array."
    assert report_data["cracked_pins"] == expected_pins, \
        f"Expected cracked_pins to be {expected_pins}, but got {report_data['cracked_pins']}. Ensure PINs are in the same order as hashes.txt."