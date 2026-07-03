# test_final_state.py

import os
import hashlib
import re

def test_audit_report_csv():
    report_path = "/home/user/audit_report.csv"
    assert os.path.isfile(report_path), f"File {report_path} is missing."

    # Compute expected results based on access.log
    log_path = "/home/user/access.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing."

    expected_lines = []
    log_regex = re.compile(r'^(\S+).*"GET /login\?redirect=([^ ]+) HTTP.*')

    with open(log_path, "r") as f:
        for line in f:
            match = log_regex.search(line)
            if match:
                ip = match.group(1)
                redirect_url = match.group(2)
                if redirect_url.startswith("http://") or redirect_url.startswith("https://"):
                    url_hash = hashlib.sha256(redirect_url.encode('utf-8')).hexdigest()
                    expected_lines.append(f"{ip},{redirect_url},{url_hash}")

    with open(report_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in audit_report.csv, but found {len(actual_lines)}."

    for expected in expected_lines:
        assert expected in actual_lines, f"Expected line '{expected}' not found in audit_report.csv."

def test_ssh_key_generated():
    priv_key_path = "/home/user/.ssh/audit_key"
    pub_key_path = "/home/user/.ssh/audit_key.pub"

    assert os.path.isfile(priv_key_path), f"Private key file {priv_key_path} is missing."
    assert os.path.isfile(pub_key_path), f"Public key file {pub_key_path} is missing."

    with open(priv_key_path, "r") as f:
        priv_content = f.read()

    assert "BEGIN OPENSSH PRIVATE KEY" in priv_content, f"Private key {priv_key_path} does not appear to be a valid OpenSSH private key."

    with open(pub_key_path, "r") as f:
        pub_content = f.read()

    assert "ssh-ed25519" in pub_content, f"Public key {pub_key_path} does not appear to be an ed25519 key."