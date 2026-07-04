# test_final_state.py
import os
import json
import base64
import hashlib
import binascii

INCIDENT_DIR = "/home/user/incident"
SERVER_LOG = os.path.join(INCIDENT_DIR, "server.log")
AUTHORIZED_KEYS = os.path.join(INCIDENT_DIR, "authorized_keys")
REPORT_JSON = "/home/user/report.json"

def get_ssh_fingerprint(pubkey_line):
    parts = pubkey_line.strip().split()
    if len(parts) >= 2:
        try:
            key_data = base64.b64decode(parts[1])
            digest = hashlib.sha256(key_data).digest()
            b64_digest = base64.b64encode(digest).decode('ascii').rstrip('=')
            return f"SHA256:{b64_digest}"
        except Exception:
            pass
    return None

def parse_server_log():
    attacker_ip = None
    decoded_payload = None
    fingerprints = {}

    with open(SERVER_LOG, 'r') as f:
        for line in f:
            line = line.strip()
            if "APP_REQ" in line:
                # Extract IP and PAYLOAD
                parts = line.split("APP_REQ: ")[1].split()
                ip = parts[0].split("=")[1]
                payload_hex = parts[1].split("=")[1]
                try:
                    payload_ascii = binascii.unhexlify(payload_hex).decode('ascii')
                    if "evil.com" in payload_ascii:
                        attacker_ip = ip
                        decoded_payload = payload_ascii
                except Exception:
                    pass
            elif "SSH_LOGIN" in line:
                parts = line.split("SSH_LOGIN: ")[1].split()
                ip = parts[0].split("=")[1]
                fp = parts[1].split("=")[1]
                fingerprints[ip] = fp

    return attacker_ip, decoded_payload, fingerprints

def test_report_json_correctness():
    assert os.path.isfile(REPORT_JSON), f"Report file {REPORT_JSON} is missing."

    attacker_ip, expected_payload, fingerprints = parse_server_log()
    assert attacker_ip is not None, "Could not find attacker IP in server.log."
    expected_fp = fingerprints.get(attacker_ip)
    assert expected_fp is not None, "Could not find attacker fingerprint in server.log."

    with open(REPORT_JSON, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REPORT_JSON} is not valid JSON.")

    assert "attacker_ip" in report, "Missing 'attacker_ip' in report."
    assert report["attacker_ip"] == attacker_ip, f"Expected attacker_ip {attacker_ip}, got {report['attacker_ip']}"

    assert "decoded_payload" in report, "Missing 'decoded_payload' in report."
    assert report["decoded_payload"] == expected_payload, f"Expected decoded_payload '{expected_payload}', got '{report['decoded_payload']}'"

    assert "compromised_fingerprint" in report, "Missing 'compromised_fingerprint' in report."
    assert report["compromised_fingerprint"] == expected_fp, f"Expected compromised_fingerprint {expected_fp}, got {report['compromised_fingerprint']}"

def test_authorized_keys_cleaned():
    assert os.path.isfile(AUTHORIZED_KEYS), f"File {AUTHORIZED_KEYS} is missing."

    attacker_ip, _, fingerprints = parse_server_log()
    bad_fp = fingerprints.get(attacker_ip)

    with open(AUTHORIZED_KEYS, 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) > 0, f"{AUTHORIZED_KEYS} is empty. It should contain the legitimate keys."

    for line in lines:
        line = line.strip()
        if not line:
            continue
        fp = get_ssh_fingerprint(line)
        assert fp != bad_fp, f"The compromised key with fingerprint {bad_fp} is still in {AUTHORIZED_KEYS}."