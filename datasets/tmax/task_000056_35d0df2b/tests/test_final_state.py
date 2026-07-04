# test_final_state.py

import os
import subprocess
import pytest

def test_report_exists_and_correct():
    report_path = "/home/user/audit_task/audit_report.txt"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = (
        "Total lines: 6\n"
        "Redacted lines: 3\n"
        "Intrusions detected: 2"
    )

    assert content == expected_content, f"Report content is incorrect. Expected:\n{expected_content}\nGot:\n{content}"

def test_encrypted_log_exists_and_decrypts():
    enc_path = "/home/user/audit_task/secure_audit.enc"
    key_path = "/home/user/audit_task/key.bin"
    iv_path = "/home/user/audit_task/iv.bin"

    assert os.path.isfile(enc_path), f"Encrypted log {enc_path} is missing."
    assert os.path.isfile(key_path), f"Key file {key_path} is missing."
    assert os.path.isfile(iv_path), f"IV file {iv_path} is missing."

    with open(key_path, "rb") as f:
        hex_key = f.read().hex().upper()

    with open(iv_path, "rb") as f:
        hex_iv = f.read().hex().upper()

    decrypted_path = "/home/user/audit_task/decrypted_audit.log"

    cmd = [
        "openssl", "enc", "-aes-256-cbc", "-d",
        "-in", enc_path,
        "-out", decrypted_path,
        "-K", hex_key,
        "-iv", hex_iv
    ]

    result = subprocess.run(cmd, capture_output=True)
    assert result.returncode == 0, f"Failed to decrypt {enc_path}. OpenSSL error: {result.stderr.decode()}"

    assert os.path.isfile(decrypted_path), "Decrypted output file was not created."

    with open(decrypted_path, "r") as f:
        decrypted_content = f.read()

    expected_lines = [
        '192.168.1.10 - - [10/Oct/2023:13:55:36 -0700] "GET /login?token=[REDACTED] HTTP/1.1" 200 2326',
        '10.0.0.5 - - [10/Oct/2023:13:56:10 -0700] "GET /product?id=1\' OR \'1\'=\'1 HTTP/1.1" 500 503',
        '172.16.0.4 - - [10/Oct/2023:13:57:00 -0700] "POST /checkout?cc=[REDACTED]&item=5 HTTP/1.1" 200 405',
        '192.168.1.11 - - [10/Oct/2023:13:58:12 -0700] "GET /../../../../etc/passwd HTTP/1.1" 403 125',
        '10.1.1.1 - - [10/Oct/2023:13:59:00 -0700] "GET /index.html HTTP/1.1" 200 1024',
        '192.168.1.10 - - [10/Oct/2023:14:00:00 -0700] "GET /dashboard?token=[REDACTED]&cc=[REDACTED] HTTP/1.1" 200 2326'
    ]

    decrypted_lines = decrypted_content.strip().split('\n')
    assert len(decrypted_lines) == len(expected_lines), f"Decrypted log has {len(decrypted_lines)} lines, expected {len(expected_lines)}."

    for i, (actual, expected) in enumerate(zip(decrypted_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: {expected}\nGot: {actual}"