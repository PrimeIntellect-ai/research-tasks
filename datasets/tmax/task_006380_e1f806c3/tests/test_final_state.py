# test_final_state.py
import os
import json
import pytest

def test_blocklist_contents():
    blocklist_path = "/home/user/blocklist.txt"
    assert os.path.isfile(blocklist_path), f"File {blocklist_path} does not exist. The Go program failed to create it."

    with open(blocklist_path, 'r') as f:
        ips = [line.strip() for line in f if line.strip()]

    expected_ips = {"10.0.0.5", "172.16.0.8"}
    actual_ips = set(ips)

    assert actual_ips == expected_ips, f"Blocklist does not contain the expected IPs. Expected {expected_ips}, but found {actual_ips}."
    assert len(ips) == 2, f"Blocklist should contain exactly 2 IPs, but found {len(ips)}."

def test_audit_trail_contents():
    audit_path = "/home/user/audit_trail.jsonl"
    assert os.path.isfile(audit_path), f"File {audit_path} does not exist. The Go program failed to create it."

    with open(audit_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Audit trail should contain exactly 2 entries, but found {len(lines)}."

    expected_entries = [
        {"ip": "192.168.1.10", "endpoint": "/api/data", "token": "REDACTED"},
        {"ip": "192.168.1.11", "endpoint": "/api/users", "token": "REDACTED"}
    ]

    actual_entries = []
    for line in lines:
        try:
            entry = json.loads(line)
            actual_entries.append(entry)
        except json.JSONDecodeError:
            pytest.fail(f"Audit trail contains an invalid JSON line: {line}")

    for expected in expected_entries:
        assert expected in actual_entries, f"Expected entry {expected} was not found in the audit trail. Actual entries: {actual_entries}"