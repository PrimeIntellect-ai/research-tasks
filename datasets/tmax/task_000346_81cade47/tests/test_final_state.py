# test_final_state.py
import os
import json
import base64
import hashlib
import subprocess

PENTEST_DIR = "/home/user/pentest"
AUTH_FILE = os.path.join(PENTEST_DIR, "auth_capture.txt")
SERVER_BIN = os.path.join(PENTEST_DIR, "server.bin")
SERVER_CRT = os.path.join(PENTEST_DIR, "server.crt")
REPORT_FILE = os.path.join(PENTEST_DIR, "report.txt")

def get_expected_values():
    # 1. Extract client_id and file_hash from auth_capture.txt
    client_id = None
    expected_file_hash = None
    with open(AUTH_FILE, 'r') as f:
        for line in f:
            if line.startswith("Authorization: Bearer "):
                token_b64 = line.strip().split(" ")[2]
                token_json = base64.b64decode(token_b64).decode('utf-8')
                token_data = json.loads(token_json)
                client_id = token_data.get("client_id")
                expected_file_hash = token_data.get("file_hash")
                break

    # 2. Compute SHA-256 of server.bin
    hasher = hashlib.sha256()
    with open(SERVER_BIN, 'rb') as f:
        hasher.update(f.read())
    actual_file_hash = hasher.hexdigest()

    integrity = "Valid" if actual_file_hash == expected_file_hash else "Invalid"

    # 3. Extract Issuer CN from server.crt using openssl
    result = subprocess.run(["openssl", "x509", "-in", SERVER_CRT, "-noout", "-issuer"], capture_output=True, text=True)
    issuer_line = result.stdout.strip()
    issuer_cn = None
    if "CN = " in issuer_line:
        issuer_cn = issuer_line.split("CN = ")[1].split(",")[0].strip()
    elif "CN=" in issuer_line:
        issuer_cn = issuer_line.split("CN=")[1].split("/")[0].strip()

    return client_id, integrity, issuer_cn

def test_report_exists_and_correct():
    assert os.path.isfile(REPORT_FILE), f"Report file {REPORT_FILE} does not exist. Ensure your script writes to this exact path."

    expected_client_id, expected_integrity, expected_issuer_cn = get_expected_values()

    with open(REPORT_FILE, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 3, f"Expected at least 3 lines in {REPORT_FILE}, found {len(lines)}."

    assert lines[0] == f"Client ID: {expected_client_id}", f"Line 1 is incorrect. Expected 'Client ID: {expected_client_id}', got '{lines[0]}'"
    assert lines[1] == f"Integrity: {expected_integrity}", f"Line 2 is incorrect. Expected 'Integrity: {expected_integrity}', got '{lines[1]}'"
    assert lines[2] == f"Certificate Issuer CN: {expected_issuer_cn}", f"Line 3 is incorrect. Expected 'Certificate Issuer CN: {expected_issuer_cn}', got '{lines[2]}'"