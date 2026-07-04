# test_final_state.py
import os
import stat
import hashlib
import subprocess
import pytest

WEB_CERTS_DIR = "/home/user/web_certs"
SERVER_KEY = "/home/user/web_certs/server.key"
SERVER_CRT = "/home/user/web_certs/server.crt"
AUDIT_REPORT = "/home/user/audit_report.txt"

def test_enc_files_deleted():
    assert not os.path.exists(os.path.join(WEB_CERTS_DIR, "backup_alpha.enc")), "backup_alpha.enc should have been deleted."
    assert not os.path.exists(os.path.join(WEB_CERTS_DIR, "backup_beta.enc")), "backup_beta.enc should have been deleted."

def test_server_key_exists_and_perms():
    assert os.path.isfile(SERVER_KEY), f"{SERVER_KEY} should exist."
    st = os.stat(SERVER_KEY)
    assert stat.S_IMODE(st.st_mode) == 0o600, f"{SERVER_KEY} should have 600 permissions."

def test_server_crt_exists_and_perms():
    assert os.path.isfile(SERVER_CRT), f"{SERVER_CRT} should exist."
    st = os.stat(SERVER_CRT)
    assert stat.S_IMODE(st.st_mode) == 0o644, f"{SERVER_CRT} should have 644 permissions."

def test_key_matches_cert():
    # Get modulus of key
    key_mod_proc = subprocess.run(
        ["openssl", "rsa", "-noout", "-modulus", "-in", SERVER_KEY],
        capture_output=True, text=True
    )
    assert key_mod_proc.returncode == 0, "Failed to get modulus from server.key. Is it a valid RSA key?"
    key_mod = key_mod_proc.stdout.strip()

    # Get modulus of cert
    cert_mod_proc = subprocess.run(
        ["openssl", "x509", "-noout", "-modulus", "-in", SERVER_CRT],
        capture_output=True, text=True
    )
    assert cert_mod_proc.returncode == 0, "Failed to get modulus from server.crt."
    cert_mod = cert_mod_proc.stdout.strip()

    assert key_mod == cert_mod, "The RSA modulus of server.key does not match server.crt."

def test_audit_report_format():
    assert os.path.isfile(AUDIT_REPORT), f"{AUDIT_REPORT} should exist."

    with open(SERVER_KEY, "rb") as f:
        key_data = f.read()
    key_sha256 = hashlib.sha256(key_data).hexdigest()

    key_mod_proc = subprocess.run(
        ["openssl", "rsa", "-noout", "-modulus", "-in", SERVER_KEY],
        capture_output=True, text=True
    )
    key_mod = key_mod_proc.stdout.strip()
    # the modulus output includes "Modulus=" prefix, so we hash the whole string or just the hex?
    # The prompt says "MD5 hash of the RSA modulus of server.key" and verification says:
    # `openssl rsa -noout -modulus -in /home/user/web_certs/server.key | openssl md5`
    # We should replicate this exact command pipeline to get the expected hash.
    md5_proc = subprocess.run(
        ["openssl", "md5"],
        input=key_mod_proc.stdout.encode('utf-8'),
        capture_output=True, text=True
    )
    # openssl md5 output might be "(stdin)= <hash>" or just "<hash>" depending on version.
    # Let's just use hashlib on the stdout.
    mod_md5 = hashlib.md5(key_mod_proc.stdout.encode('utf-8')).hexdigest()

    with open(AUDIT_REPORT, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n')]

    assert len(lines) == 4, "Audit report should have exactly 4 lines."

    assert lines[0] == f"MATCHED KEY SHA256: {key_sha256}", "Line 1 does not match the expected SHA256 format or value."

    # Handle possible differences in openssl md5 output formats
    # The prompt example: MODULUS MD5: d41d8cd98f00b204e9800998ecf8427e
    assert lines[1] == f"MODULUS MD5: {mod_md5}", "Line 2 does not match the expected MD5 format or value."

    assert lines[2] == f"{SERVER_CRT} 644", "Line 3 does not match expected cert permissions."
    assert lines[3] == f"{SERVER_KEY} 600", "Line 4 does not match expected key permissions."

def test_no_extra_files_in_web_certs():
    files = set(os.listdir(WEB_CERTS_DIR))
    assert files == {"server.crt", "server.key"}, "There should be no extra files in /home/user/web_certs."