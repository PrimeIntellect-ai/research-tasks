# test_final_state.py

import os
import json
import csv
import hashlib
import ipaddress
import pytest
import re

REPORT_PATH = "/home/user/audit_report.json"
DATA_DIR = "/home/user/sec_data"

def compute_expected_integrity():
    manifest_path = os.path.join(DATA_DIR, "manifest.sha256")
    expected = {}

    if not os.path.isfile(manifest_path):
        return expected

    manifest_hashes = {}
    with open(manifest_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                manifest_hashes[parts[1]] = parts[0]

    for filename in ["auth_logs.json", "network_policy.json", "connections.csv"]:
        filepath = os.path.join(DATA_DIR, filename)
        if not os.path.isfile(filepath):
            continue

        with open(filepath, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        if filename in manifest_hashes and manifest_hashes[filename] == file_hash:
            expected[filename] = "PASS"
        else:
            expected[filename] = "FAIL"

    return expected

def compute_expected_auth_violations():
    logs_path = os.path.join(DATA_DIR, "auth_logs.json")
    violations = []

    if not os.path.isfile(logs_path):
        return violations

    with open(logs_path, "r") as f:
        logs = json.load(f)

    for entry in logs:
        violation = False
        req_headers = entry.get("request", {}).get("headers", {})
        res_headers = entry.get("response", {}).get("headers", {})

        auth_header = req_headers.get("Authorization")
        if auth_header and not auth_header.startswith("Bearer "):
            violation = True

        set_cookie = res_headers.get("Set-Cookie")
        if set_cookie:
            # Check for exact word matches using regex for word boundaries or splitting by ;
            parts = [p.strip() for p in set_cookie.split(";")]
            if "Secure" not in parts or "HttpOnly" not in parts:
                violation = True

        if violation:
            violations.append(entry["id"])

    return sorted(violations)

def compute_expected_connections():
    policy_path = os.path.join(DATA_DIR, "network_policy.json")
    conn_path = os.path.join(DATA_DIR, "connections.csv")
    evaluations = {}

    if not os.path.isfile(policy_path) or not os.path.isfile(conn_path):
        return evaluations

    with open(policy_path, "r") as f:
        policies = json.load(f)

    with open(conn_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            conn_id = row["conn_id"]
            src_ip = ipaddress.ip_address(row["src_ip"])
            dest_port = int(row["dest_port"])

            allowed = False
            for rule in policies:
                rule_net = ipaddress.ip_network(rule["src_ip_range"])
                rule_port = int(rule["dest_port"])

                if src_ip in rule_net and dest_port == rule_port:
                    allowed = True
                    break

            evaluations[conn_id] = "ALLOWED" if allowed else "DENIED"

    return evaluations

@pytest.fixture(scope="module")
def audit_report():
    assert os.path.isfile(REPORT_PATH), f"Output file {REPORT_PATH} was not created."
    with open(REPORT_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REPORT_PATH} is not a valid JSON file.")

def test_integrity_checks(audit_report):
    assert "integrity_checks" in audit_report, "Missing 'integrity_checks' key in report."
    expected = compute_expected_integrity()
    actual = audit_report["integrity_checks"]

    for filename, status in expected.items():
        assert filename in actual, f"Missing integrity check for {filename}"
        assert actual[filename] == status, f"Integrity check for {filename} should be {status}, got {actual[filename]}"

def test_auth_violations(audit_report):
    assert "auth_violations" in audit_report, "Missing 'auth_violations' key in report."
    expected = compute_expected_auth_violations()
    actual = sorted(audit_report["auth_violations"])

    assert actual == expected, f"Auth violations mismatch. Expected {expected}, got {actual}"

def test_connection_evaluations(audit_report):
    assert "connection_evaluations" in audit_report, "Missing 'connection_evaluations' key in report."
    expected = compute_expected_connections()
    actual = audit_report["connection_evaluations"]

    for conn_id, status in expected.items():
        assert conn_id in actual, f"Missing connection evaluation for {conn_id}"
        assert actual[conn_id] == status, f"Connection evaluation for {conn_id} should be {status}, got {actual[conn_id]}"