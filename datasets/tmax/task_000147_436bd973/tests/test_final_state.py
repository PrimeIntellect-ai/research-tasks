# test_final_state.py
import os
import json
import base64
import pytest
import re

TRAFFIC_LOG_PATH = "/home/user/traffic_capture.json"
REPORT_PATH = "/home/user/report.json"
MALWARE_PATH = "/home/user/malware.elf"

def derive_truth():
    """Derive the expected truth values from the traffic log."""
    assert os.path.exists(TRAFFIC_LOG_PATH), f"Missing {TRAFFIC_LOG_PATH}"
    with open(TRAFFIC_LOG_PATH, 'r', encoding='utf-8') as f:
        traffic_log = json.load(f)

    malicious_jwt = None
    sqli_payload = None

    for entry in traffic_log:
        auth_header = entry.get("headers", {}).get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[len("Bearer "):]
            parts = token.split(".")
            if len(parts) >= 2:
                try:
                    # Add padding if needed
                    header_pad = parts[0] + "=" * ((4 - len(parts[0]) % 4) % 4)
                    payload_pad = parts[1] + "=" * ((4 - len(parts[1]) % 4) % 4)

                    header = json.loads(base64.urlsafe_b64decode(header_pad).decode('utf-8'))
                    payload = json.loads(base64.urlsafe_b64decode(payload_pad).decode('utf-8'))

                    if header.get("alg", "").lower() == "none" and payload.get("role") == "admin":
                        malicious_jwt = token
                        sqli_payload = entry.get("data", "")
                        break
                except Exception:
                    continue

    assert malicious_jwt is not None, "Could not find malicious JWT in traffic log."
    assert sqli_payload is not None, "Could not find SQLi payload in traffic log."

    # Extract base64 payload from SQLi string
    # Assuming the format is something like "... 'BASE64_STRING' ..."
    match = re.search(r"'([A-Za-z0-9+/=]+)'", sqli_payload)
    assert match is not None, "Could not find base64 payload in SQLi data."
    b64_payload = match.group(1)

    encrypted_elf = base64.b64decode(b64_payload)

    # Brute force XOR key
    xor_key = None
    decrypted_elf = None
    for k in range(256):
        dec = bytes([b ^ k for b in encrypted_elf])
        if dec.startswith(b'\x7fELF'):
            xor_key = k
            decrypted_elf = dec
            break

    assert xor_key is not None, "Could not find XOR key to decrypt ELF."

    # Extract C2 server
    c2_server_address = None
    c2_match = re.search(b'C2_SERVER=([^\x00]+)', decrypted_elf)
    if c2_match:
        c2_server_address = c2_match.group(1).decode('utf-8', errors='ignore')

    assert c2_server_address is not None, "Could not find C2 server address in decrypted ELF."

    return {
        "malicious_jwt": malicious_jwt,
        "xor_key_decimal": xor_key,
        "c2_server_address": c2_server_address,
        "decrypted_elf": decrypted_elf
    }

@pytest.fixture(scope="module")
def truth_data():
    return derive_truth()

def test_report_exists_and_valid_json():
    assert os.path.exists(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."
    assert os.path.isfile(REPORT_PATH), f"Report path {REPORT_PATH} is not a file."
    try:
        with open(REPORT_PATH, 'r', encoding='utf-8') as f:
            json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"Report file {REPORT_PATH} is not valid JSON.")

def test_report_contents(truth_data):
    with open(REPORT_PATH, 'r', encoding='utf-8') as f:
        report = json.load(f)

    assert "malicious_jwt" in report, "Report missing 'malicious_jwt' key."
    assert report["malicious_jwt"] == truth_data["malicious_jwt"], "Incorrect malicious_jwt in report."

    assert "xor_key_decimal" in report, "Report missing 'xor_key_decimal' key."
    assert report["xor_key_decimal"] == truth_data["xor_key_decimal"], "Incorrect xor_key_decimal in report."

    assert "c2_server_address" in report, "Report missing 'c2_server_address' key."
    assert report["c2_server_address"] == truth_data["c2_server_address"], "Incorrect c2_server_address in report."

def test_malware_elf_exists_and_valid(truth_data):
    assert os.path.exists(MALWARE_PATH), f"Malware file {MALWARE_PATH} does not exist."
    assert os.path.isfile(MALWARE_PATH), f"Malware path {MALWARE_PATH} is not a file."

    with open(MALWARE_PATH, 'rb') as f:
        content = f.read()

    assert content.startswith(b'\x7fELF'), "The saved malware file does not start with ELF magic bytes."
    assert content == truth_data["decrypted_elf"], "The saved malware file content does not match the fully decrypted payload."