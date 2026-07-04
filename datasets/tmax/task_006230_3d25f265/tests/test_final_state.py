# test_final_state.py

import os
import json
import pytest
import ipaddress
import tarfile
import io

REPORT_PATH = "/home/user/report.json"
BASE_DIR = "/home/user/audit_task"
ENC_PATH = os.path.join(BASE_DIR, "audit.enc")
POLICY_PATH = os.path.join(BASE_DIR, "policy.json")

def get_expected_results():
    # 1. Recover the key
    with open(ENC_PATH, "rb") as f:
        ciphertext = f.read()

    magic_bytes = bytes([0x1F, 0x8B, 0x08, 0x00])
    key = bytes([ciphertext[i] ^ magic_bytes[i] for i in range(4)])
    expected_key_hex = key.hex().upper()

    # 2. Decrypt the archive
    plaintext = bytearray(len(ciphertext))
    for i in range(len(ciphertext)):
        plaintext[i] = ciphertext[i] ^ key[i % 4]

    # 3. Extract access.log
    tar_stream = io.BytesIO(plaintext)
    with tarfile.open(fileobj=tar_stream, mode="r:gz") as tar:
        log_file = tar.extractfile("access.log")
        log_content = log_file.read().decode("utf-8")

    # 4. Parse policy
    with open(POLICY_PATH, "r") as f:
        policy = json.load(f)

    allowed_subnets = [ipaddress.ip_network(net) for net in policy.get("allowed_subnets", [])]
    explicit_blocks = set(policy.get("explicit_blocks", []))

    # 5. Find violations
    violations = set()
    for line in log_content.strip().split("\n"):
        if not line:
            continue
        parts = line.split()
        if len(parts) < 9:
            continue

        ip_str = parts[0]
        status = parts[-2]

        if status == "200":
            ip = ipaddress.ip_address(ip_str)

            # Check policy
            is_allowed = False
            for subnet in allowed_subnets:
                if ip in subnet:
                    is_allowed = True
                    break

            if not is_allowed or ip_str in explicit_blocks:
                violations.add(ip_str)

    return expected_key_hex, sorted(list(violations))

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} is missing."

def test_report_contents():
    with open(REPORT_PATH, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REPORT_PATH} is not valid JSON.")

    assert "encryption_key_hex" in report, "Missing 'encryption_key_hex' in report."
    assert "policy_violations" in report, "Missing 'policy_violations' in report."

    expected_key, expected_violations = get_expected_results()

    assert report["encryption_key_hex"].upper() == expected_key, \
        f"Expected encryption key {expected_key}, but got {report['encryption_key_hex']}."

    actual_violations = sorted(report["policy_violations"])
    assert actual_violations == expected_violations, \
        f"Expected policy violations {expected_violations}, but got {actual_violations}."