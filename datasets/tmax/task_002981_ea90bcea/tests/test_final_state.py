# test_final_state.py

import os
import socket
import hashlib
import re
import pytest

AUDIT_DIR = "/home/user/audit"
TAR_FILE = os.path.join(AUDIT_DIR, "server_config.tar.gz")
SHA_FILE = os.path.join(AUDIT_DIR, "server_config.tar.gz.sha256")
TRAFFIC_LOG = os.path.join(AUDIT_DIR, "traffic.log")
REPORT_FILE = "/home/user/audit_report.txt"
ANALYZER_C = "/home/user/analyzer.c"
ANALYZER_BIN = "/home/user/analyzer"

def compute_expected_integrity():
    if not os.path.isfile(TAR_FILE) or not os.path.isfile(SHA_FILE):
        return "INTEGRITY_FAILED"
    with open(TAR_FILE, 'rb') as f:
        actual_sha = hashlib.sha256(f.read()).hexdigest()
    with open(SHA_FILE, 'r') as f:
        sha_content = f.read().strip()
    if actual_sha in sha_content:
        return "INTEGRITY_OK"
    return "INTEGRITY_FAILED"

def find_open_port():
    for port in range(8080, 8091):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            if s.connect_ex(('127.0.0.1', port)) == 0:
                return port
    return None

def compute_expected_exploits():
    if not os.path.isfile(TRAFFIC_LOG):
        return []

    exploits = []
    log_pattern = re.compile(r'^(\S+)\s+\[.*?\]\s+"GET\s+/login\?redirect=([^&]+)&token=([0-9a-fA-F]{2})\s+HTTP/1\.1"\s+\d+')

    with open(TRAFFIC_LOG, 'r') as f:
        for line in f:
            match = log_pattern.search(line)
            if match:
                ip, redirect, token = match.groups()
                if redirect.startswith("http://") or redirect.startswith("https://"):
                    ascii_sum = sum(ord(c) for c in redirect)
                    expected_token = (ascii_sum % 256) ^ 0x42
                    if expected_token == int(token, 16):
                        exploits.append(ip)
    return exploits

def test_analyzer_c_exists():
    assert os.path.isfile(ANALYZER_C), f"Expected C source file {ANALYZER_C} is missing."

def test_analyzer_bin_exists_and_executable():
    assert os.path.isfile(ANALYZER_BIN), f"Expected compiled executable {ANALYZER_BIN} is missing."
    assert os.access(ANALYZER_BIN, os.X_OK), f"File {ANALYZER_BIN} is not executable."

def test_audit_report_content():
    assert os.path.isfile(REPORT_FILE), f"Expected report file {REPORT_FILE} is missing."

    with open(REPORT_FILE, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_integrity = compute_expected_integrity()
    expected_port = find_open_port()
    expected_exploits = compute_expected_exploits()

    expected_lines = [
        expected_integrity,
        f"SERVER_PORT={expected_port}" if expected_port else "SERVER_PORT=UNKNOWN"
    ]
    for ip in expected_exploits:
        expected_lines.append(f"EXPLOIT_IP={ip}")

    assert len(lines) == len(expected_lines), f"Report file {REPORT_FILE} has {len(lines)} lines, expected {len(expected_lines)}."

    assert lines[0] == expected_lines[0], f"Line 1 of report should be '{expected_lines[0]}', found '{lines[0]}'."
    assert lines[1] == expected_lines[1], f"Line 2 of report should be '{expected_lines[1]}', found '{lines[1]}'."

    for i in range(2, len(expected_lines)):
        assert lines[i] == expected_lines[i], f"Line {i+1} of report should be '{expected_lines[i]}', found '{lines[i]}'."