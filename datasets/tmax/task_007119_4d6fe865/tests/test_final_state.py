# test_final_state.py

import os
import json
import hashlib
import subprocess
import pytest

DEPLOY_DIR = "/home/user/deploy_artifact"
REPORT_FILE = "/home/user/audit_report.json"

def get_expected_integrity_failures():
    manifest_path = os.path.join(DEPLOY_DIR, "manifest.txt")
    failures = []
    if not os.path.exists(manifest_path):
        return failures
    with open(manifest_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                expected_hash, filename = parts
                file_path = os.path.join(DEPLOY_DIR, filename)
                if not os.path.exists(file_path):
                    failures.append(filename)
                    continue
                with open(file_path, 'rb') as tf:
                    actual_hash = hashlib.sha256(tf.read()).hexdigest()
                if actual_hash != expected_hash:
                    failures.append(filename)
    return sorted(failures)

def get_expected_certificate_valid():
    ca_crt = os.path.join(DEPLOY_DIR, "ca.crt")
    server_crt = os.path.join(DEPLOY_DIR, "server.crt")
    if not os.path.exists(ca_crt) or not os.path.exists(server_crt):
        return False
    result = subprocess.run(
        ["openssl", "verify", "-CAfile", ca_crt, server_crt],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.returncode == 0

def get_expected_vulnerable_files():
    vulnerable = []
    if not os.path.exists(DEPLOY_DIR):
        return vulnerable
    for filename in os.listdir(DEPLOY_DIR):
        if filename.endswith(".py"):
            file_path = os.path.join(DEPLOY_DIR, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    if "os.popen(" in f.read():
                        vulnerable.append(filename)
    return sorted(vulnerable)

def get_expected_world_writable_files():
    world_writable = []
    if not os.path.exists(DEPLOY_DIR):
        return world_writable
    for filename in os.listdir(DEPLOY_DIR):
        file_path = os.path.join(DEPLOY_DIR, filename)
        if os.path.isfile(file_path):
            st = os.stat(file_path)
            if st.st_mode & 0o002:
                world_writable.append(filename)
    return sorted(world_writable)

@pytest.fixture
def report_data():
    assert os.path.exists(REPORT_FILE), f"Audit report file {REPORT_FILE} does not exist."
    with open(REPORT_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_FILE} is not valid JSON.")
    return data

def test_report_structure(report_data):
    expected_keys = {"integrity_failures", "certificate_valid", "vulnerable_files", "world_writable_files"}
    actual_keys = set(report_data.keys())
    assert expected_keys.issubset(actual_keys), f"Report is missing keys. Expected: {expected_keys}, Found: {actual_keys}"

def test_integrity_failures(report_data):
    expected = get_expected_integrity_failures()
    actual = sorted(report_data.get("integrity_failures", []))
    assert actual == expected, f"Integrity failures mismatch. Expected: {expected}, Actual: {actual}"

def test_certificate_valid(report_data):
    expected = get_expected_certificate_valid()
    actual = report_data.get("certificate_valid")
    assert actual is expected, f"Certificate validation mismatch. Expected: {expected}, Actual: {actual}"

def test_vulnerable_files(report_data):
    expected = get_expected_vulnerable_files()
    actual = sorted(report_data.get("vulnerable_files", []))
    assert actual == expected, f"Vulnerable files mismatch. Expected: {expected}, Actual: {actual}"

def test_world_writable_files(report_data):
    expected = get_expected_world_writable_files()
    actual = sorted(report_data.get("world_writable_files", []))
    assert actual == expected, f"World writable files mismatch. Expected: {expected}, Actual: {actual}"