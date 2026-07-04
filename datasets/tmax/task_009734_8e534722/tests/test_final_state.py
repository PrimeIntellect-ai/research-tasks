# test_final_state.py
import os
import pytest

def test_original_files_unmodified():
    server_log = '/home/user/active_logs/app1/server.log'
    assert os.path.isfile(server_log), f"Original file {server_log} is missing"
    with open(server_log, 'r') as f:
        content = f.read()
        assert 'IP: 192.168.1.50' in content, "Original file was modified: missing IP"
        assert 'SSN: 123-45-6789' in content, "Original file was modified: missing SSN"

def test_archived_files_redacted():
    server_log = '/home/user/archived_logs/app1/server.log'
    db_log = '/home/user/archived_logs/app1/subs/db.log'
    api_log = '/home/user/archived_logs/app2/api.log'

    assert os.path.isfile(server_log), f"Archived file {server_log} is missing"
    assert os.path.isfile(db_log), f"Archived file {db_log} is missing"
    assert os.path.isfile(api_log), f"Archived file {api_log} is missing"

    with open(server_log, 'r') as f:
        content = f.read()
        assert 'IP: REDACTED' in content, f"Missing IP redaction in {server_log}"
        assert 'SSN: ***-**-****' in content, f"Missing SSN redaction in {server_log}"
        assert '192.168.1.50' not in content, f"Original IP found in {server_log}"
        assert '123-45-6789' not in content, f"Original SSN found in {server_log}"

    with open(db_log, 'r') as f:
        content = f.read()
        assert 'IP: REDACTED' in content, f"Missing IP redaction in {db_log}"
        assert 'SSN: ***-**-****' in content, f"Missing SSN redaction in {db_log}"
        assert '10.0.0.1' not in content, f"Original IP found in {db_log}"
        assert '172.16.254.1' not in content, f"Original IP found in {db_log}"
        assert '987-65-4321' not in content, f"Original SSN found in {db_log}"

    with open(api_log, 'r') as f:
        content = f.read()
        assert 'SSN: ***-**-****' in content, f"Missing SSN redaction in {api_log}"
        assert '111-22-3333' not in content, f"Original SSN found in {api_log}"

def test_summary_file():
    summary_file = '/home/user/redaction_summary.txt'
    assert os.path.isfile(summary_file), f"Summary file {summary_file} is missing"

    with open(summary_file, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "app1/server.log: 2",
        "app1/subs/db.log: 2",
        "app2/api.log: 1"
    ]

    assert lines == expected_lines, f"Summary file contents incorrect.\nExpected: {expected_lines}\nGot: {lines}"