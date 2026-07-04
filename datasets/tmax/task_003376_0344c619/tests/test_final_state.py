# test_final_state.py

import os
import json
import hashlib
import subprocess
import pytest

def check_permissions(path, expected_mode):
    try:
        mode = os.stat(path).st_mode & 0o777
        return mode == expected_mode
    except FileNotFoundError:
        return False

def check_hash(path, expected_hash):
    try:
        with open(path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest() == expected_hash
    except FileNotFoundError:
        return False

def check_cert(path, expected_cn):
    try:
        output = subprocess.check_output(
            ['openssl', 'x509', '-noout', '-subject', '-in', path], 
            stderr=subprocess.STDOUT
        ).decode()
        return f"CN = {expected_cn}" in output or f"CN={expected_cn}" in output
    except Exception:
        return False

def check_vuln_report():
    try:
        with open('/home/user/vuln_report.json', 'r') as f:
            data = json.load(f)
            if not isinstance(data, list): 
                return False
            expected = {
                '/home/user/app/source/main.py',
                '/home/user/app/source/config.js'
            }
            return set(data) == expected
    except Exception:
        return False

def test_security_posture_score():
    points = 0
    total = 5
    failures = []

    # 1. config.yml permissions (0600)
    if check_permissions('/home/user/app/config.yml', 0o600):
        points += 1
    else:
        failures.append("config.yml does not have 0600 permissions")

    # 2. server.key permissions (0400)
    if check_permissions('/home/user/app/certs/server.key', 0o400):
        points += 1
    else:
        failures.append("server.key does not have 0400 permissions")

    # 3. secure_exec hash (backup_B.bin)
    target_hash = hashlib.sha256(b"echo 'correct binary v2'\n").hexdigest()
    if check_hash('/home/user/app/bin/secure_exec', target_hash):
        points += 1
    else:
        failures.append("secure_exec does not match the expected SHA-256 hash")

    # 4. TLS Cert CN
    if check_cert('/home/user/app/certs/server.crt', 'secure-internal.local'):
        points += 1
    else:
        failures.append("server.crt does not have the expected CN 'secure-internal.local'")

    # 5. Vulnerability report
    if check_vuln_report():
        points += 1
    else:
        failures.append("vuln_report.json is missing, malformed, or contains incorrect findings")

    score = points / total

    assert score >= 0.8, (
        f"Security Posture Score is {score} (threshold >= 0.8). "
        f"Passed {points}/{total} checks. "
        f"Failures: {', '.join(failures)}"
    )