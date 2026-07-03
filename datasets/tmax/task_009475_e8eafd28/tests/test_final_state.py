# test_final_state.py

import os
import json
import pytest

REPORT_FILE = "/home/user/audit_report.json"
GO_SOURCE = "/home/user/generate_report.go"

def test_go_source_exists():
    assert os.path.isfile(GO_SOURCE), f"Go source file {GO_SOURCE} is missing."

def test_audit_report_exists():
    assert os.path.isfile(REPORT_FILE), f"Audit report {REPORT_FILE} is missing."

def test_audit_report_contents():
    with open(REPORT_FILE, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{REPORT_FILE} is not a valid JSON file.")

    # Check weak_ssh_key_lines
    assert "weak_ssh_key_lines" in report, "Missing 'weak_ssh_key_lines' in report."
    expected_lines = [2, 4]
    assert report["weak_ssh_key_lines"] == expected_lines, \
        f"Expected weak_ssh_key_lines to be {expected_lines}, got {report.get('weak_ssh_key_lines')}."

    # Check privesc_files
    assert "privesc_files" in report, "Missing 'privesc_files' in report."
    expected_files = [
        "/opt/app/config.yml",
        "/tmp/shared_cache",
        "/usr/bin/ping"
    ]
    assert report["privesc_files"] == expected_files, \
        f"Expected privesc_files to be {expected_files}, got {report.get('privesc_files')}."

    # Check cwe78_injected_command
    assert "cwe78_injected_command" in report, "Missing 'cwe78_injected_command' in report."
    expected_cmd = "ping -c 4 -W 2 "
    assert report["cwe78_injected_command"] == expected_cmd, \
        f"Expected cwe78_injected_command to be '{expected_cmd}', got '{report.get('cwe78_injected_command')}'."