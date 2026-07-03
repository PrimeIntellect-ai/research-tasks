# test_final_state.py

import os
import subprocess
import hmac
import hashlib
from pathlib import Path

def run_cmd(cmd, input_data=None):
    result = subprocess.run(
        cmd,
        input=input_data,
        capture_output=True,
        text=True,
        check=False
    )
    return result

def test_rotated_agent_exists():
    assert Path("/home/user/rotated_agent").exists(), "/home/user/rotated_agent does not exist."
    assert os.access("/home/user/rotated_agent", os.X_OK), "/home/user/rotated_agent is not executable."

def test_rotation_summary_exists():
    assert Path("/home/user/rotation_summary.txt").exists(), "/home/user/rotation_summary.txt does not exist."

def test_elf_section_and_payload():
    agent_path = "/home/user/rotated_agent"
    extracted_path = "/tmp/extracted_secret_auth.bin"

    # Extract the .secret_auth section
    res = run_cmd(["objcopy", "-O", "binary", "-j", ".secret_auth", agent_path, extracted_path])
    assert res.returncode == 0, f"Failed to extract .secret_auth section: {res.stderr}"
    assert Path(extracted_path).exists(), "Extracted section file not found."

    with open(extracted_path, "r") as f:
        payload = f.read()

    lines = payload.strip().split("\n")
    assert len(lines) > 3, "Payload does not contain enough lines for HMAC, Cert, and Key."

    hmac_hex = lines[0].strip()

    # Extract Cert and Key from payload
    cert_start = payload.find("-----BEGIN CERTIFICATE-----")
    cert_end = payload.find("-----END CERTIFICATE-----") + len("-----END CERTIFICATE-----")
    key_start = payload.find("-----BEGIN PRIVATE KEY-----")
    if key_start == -1:
        key_start = payload.find("-----BEGIN RSA PRIVATE KEY-----")
    key_end = payload.find("-----END PRIVATE KEY-----") + len("-----END PRIVATE KEY-----")
    if key_end < key_start:
        key_end = payload.find("-----END RSA PRIVATE KEY-----") + len("-----END RSA PRIVATE KEY-----")

    assert cert_start != -1 and cert_end > cert_start, "Certificate not found in payload."
    assert key_start != -1 and key_end > key_start, "Private key not found in payload."

    cert_pem = payload[cert_start:cert_end]

    # Verify Cert Subject
    res = run_cmd(["openssl", "x509", "-noout", "-subject"], input_data=cert_pem)
    assert res.returncode == 0, "Failed to parse certificate."
    assert "CN = auth-agent" in res.stdout or "CN=auth-agent" in res.stdout, f"Certificate subject is incorrect: {res.stdout}"

    # Verify Key Length is 2048
    res = run_cmd(["openssl", "x509", "-noout", "-text"], input_data=cert_pem)
    assert "2048 bit" in res.stdout, "Certificate is not 2048-bit RSA."

    # Get Fingerprint
    res = run_cmd(["openssl", "x509", "-noout", "-fingerprint", "-sha256"], input_data=cert_pem)
    assert res.returncode == 0, "Failed to get certificate fingerprint."
    fingerprint_line = res.stdout.strip()
    assert "Fingerprint=" in fingerprint_line, "Unexpected fingerprint output format."
    fingerprint = fingerprint_line.split("Fingerprint=")[1].strip()

    # Compute Expected HMAC
    with open("/home/user/master.key", "r") as f:
        master_key = f.read().encode('utf-8')

    expected_hmac = hmac.new(master_key, fingerprint.encode('utf-8'), hashlib.sha256).hexdigest()

    assert hmac_hex == expected_hmac, f"HMAC in payload ({hmac_hex}) does not match expected HMAC ({expected_hmac})."

    # Verify rotation_summary.txt
    with open("/home/user/rotation_summary.txt", "r") as f:
        summary = f.read().strip().split("\n")

    assert len(summary) == 2, "rotation_summary.txt must contain exactly two lines."
    assert summary[0] == f"FINGERPRINT={fingerprint}", f"rotation_summary.txt FINGERPRINT line incorrect. Expected FINGERPRINT={fingerprint}"
    assert summary[1] == f"TOKEN={expected_hmac}", f"rotation_summary.txt TOKEN line incorrect. Expected TOKEN={expected_hmac}"