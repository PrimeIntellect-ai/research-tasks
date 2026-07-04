# test_final_state.py
import os
import re
import json
import hashlib
import pytest

RAW_LOGS_PATH = '/home/user/raw_logs.txt'
WORDLIST_PATH = '/home/user/wordlist.txt'
REDACTED_LOGS_PATH = '/home/user/redacted_logs.txt'
SECURITY_REPORT_PATH = '/home/user/security_report.json'

def get_expected_redacted_logs():
    with open(RAW_LOGS_PATH, 'r') as f:
        raw_logs = f.read()

    # Replace any 4 groups of 4 digits separated by hyphens with [REDACTED]
    redacted_logs = re.sub(r'\b\d{4}-\d{4}-\d{4}-\d{4}\b', '[REDACTED]', raw_logs)
    return redacted_logs

def get_expected_security_report():
    with open(RAW_LOGS_PATH, 'r') as f:
        lines = f.readlines()

    with open(WORDLIST_PATH, 'r') as f:
        words = [line.strip() for line in f if line.strip()]

    ip_malicious_counts = {}
    hashes_found = set()

    malicious_patterns = [
        re.compile(r'<script>', re.IGNORECASE),
        re.compile(r"' or '1'='1", re.IGNORECASE)
    ]

    for line in lines:
        # Parse log line: [TIMESTAMP] [IP] [LEVEL] MESSAGE
        match = re.match(r'^\[.*?\]\s+\[(.*?)\]\s+\[.*?\]\s+(.*)$', line)
        if match:
            ip = match.group(1)
            message = match.group(2)

            # Check for malicious requests
            is_malicious = any(p.search(message) for p in malicious_patterns)
            if is_malicious:
                ip_malicious_counts[ip] = ip_malicious_counts.get(ip, 0) + 1

            # Check for leaked hashes
            hash_match = re.search(r'Auth failed: hash=([a-fA-F0-9]{32})', message)
            if hash_match:
                hashes_found.add(hash_match.group(1))

    blocked_ips = sorted([ip for ip, count in ip_malicious_counts.items() if count >= 3])

    weak_passwords = {}
    for word in words:
        word_hash = hashlib.md5(word.encode('utf-8')).hexdigest()
        if word_hash in hashes_found:
            weak_passwords[word_hash] = word

    return {
        "blocked_ips": blocked_ips,
        "weak_passwords": weak_passwords
    }

def test_redacted_logs():
    assert os.path.exists(REDACTED_LOGS_PATH), f"The file {REDACTED_LOGS_PATH} was not created."

    expected_content = get_expected_redacted_logs()

    with open(REDACTED_LOGS_PATH, 'r') as f:
        actual_content = f.read()

    assert actual_content == expected_content, "The redacted logs do not match the expected output. Ensure exact formatting and line order are maintained, and all CC numbers are replaced with '[REDACTED]'."

def test_security_report():
    assert os.path.exists(SECURITY_REPORT_PATH), f"The file {SECURITY_REPORT_PATH} was not created."

    with open(SECURITY_REPORT_PATH, 'r') as f:
        try:
            actual_report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {SECURITY_REPORT_PATH} does not contain valid JSON.")

    expected_report = get_expected_security_report()

    assert "blocked_ips" in actual_report, "The security report is missing the 'blocked_ips' key."
    assert "weak_passwords" in actual_report, "The security report is missing the 'weak_passwords' key."

    assert isinstance(actual_report["blocked_ips"], list), "'blocked_ips' should be a list."
    assert isinstance(actual_report["weak_passwords"], dict), "'weak_passwords' should be a dictionary."

    assert sorted(actual_report["blocked_ips"]) == expected_report["blocked_ips"], "The 'blocked_ips' list does not match the expected IPs with 3 or more malicious requests."
    assert actual_report["weak_passwords"] == expected_report["weak_passwords"], "The 'weak_passwords' dictionary does not match the expected cracked hashes."