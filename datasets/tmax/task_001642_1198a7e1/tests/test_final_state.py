# test_final_state.py

import os
import hmac
import hashlib
import pytest

def test_suid_bin_evidence():
    evidence_file = "/home/user/evidence/suid_bin.txt"
    assert os.path.isfile(evidence_file), f"Evidence file {evidence_file} is missing."

    with open(evidence_file, "r") as f:
        content = f.read().strip()

    expected_bin = "/home/user/bin/backup_util"
    assert content == expected_bin, f"Expected {expected_bin} in {evidence_file}, but got {content}."

def test_attacker_ip_evidence():
    evidence_file = "/home/user/evidence/attacker_ip.txt"
    assert os.path.isfile(evidence_file), f"Evidence file {evidence_file} is missing."

    with open(evidence_file, "r") as f:
        content = f.read().strip()

    expected_ip = "172.16.0.4"
    assert content == expected_ip, f"Expected IP {expected_ip} in {evidence_file}, but got {content}."

def test_forged_token_evidence():
    evidence_file = "/home/user/evidence/forged_token.txt"
    assert os.path.isfile(evidence_file), f"Evidence file {evidence_file} is missing."

    with open(evidence_file, "r") as f:
        content = f.read().strip()

    ip = "172.16.0.4"
    exp = "1900000000"
    key = b"F0r3ns1csK3y!"
    payload = f"IP:{ip}:EXP:{exp}".encode('utf-8')

    signature = hmac.new(key, payload, hashlib.sha256).hexdigest()
    expected_token = f"IP:{ip}:EXP:{exp}.{signature}"

    assert content == expected_token, f"Expected token {expected_token} in {evidence_file}, but got {content}."