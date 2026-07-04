# test_final_state.py

import os
import stat
import subprocess
import hashlib
import pytest

def test_phase1_tls_certificates():
    cert_path = "/home/user/certs/server.crt"
    key_path = "/home/user/certs/server.key"

    assert os.path.isfile(cert_path), f"Certificate file missing at {cert_path}"
    assert os.path.isfile(key_path), f"Key file missing at {key_path}"

    # Check permissions of the key
    st = os.stat(key_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Expected {key_path} to have 600 permissions, got {oct(perms)}"

    # Check Common Name using openssl
    result = subprocess.run(
        ["openssl", "x509", "-in", cert_path, "-noout", "-subject"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, "Failed to parse certificate with openssl"
    # The output format can vary, but typically contains CN = staging.local or CN=staging.local
    assert "CN = staging.local" in result.stdout or "CN=staging.local" in result.stdout, \
        f"Certificate does not have the correct Common Name. Subject: {result.stdout}"

def test_phase2_file_permissions():
    web_root = "/home/user/web_root"
    assert os.path.isdir(web_root), f"Directory missing: {web_root}"

    for root, dirs, files in os.walk(web_root):
        # Check current directory
        st_dir = os.stat(root)
        dir_perms = stat.S_IMODE(st_dir.st_mode)
        assert dir_perms == 0o755, f"Directory {root} should have 755 permissions, got {oct(dir_perms)}"

        # Check files
        for f in files:
            file_path = os.path.join(root, f)
            st_file = os.stat(file_path)
            file_perms = stat.S_IMODE(st_file.st_mode)
            assert file_perms == 0o644, f"File {file_path} should have 644 permissions, got {oct(file_perms)}"

def test_phase3_csp_enforcement():
    index_path = "/home/user/web_root/index.html"
    assert os.path.isfile(index_path), f"File missing: {index_path}"

    with open(index_path, "r") as f:
        content = f.read()

    expected_csp = "<meta http-equiv=\"Content-Security-Policy\" content=\"default-src 'self';\">"
    assert expected_csp in content, "CSP meta tag is missing or incorrect in index.html"

    # Check if it is immediately after <head>
    # Find <head> and check what follows
    head_idx = content.find("<head>")
    assert head_idx != -1, "<head> tag missing in index.html"

    after_head = content[head_idx + len("<head>"):].strip()
    assert after_head.startswith(expected_csp), "CSP meta tag is not immediately after the <head> tag"

def test_phase4_sensitive_data_redaction():
    script_path = "/home/user/redact.sh"
    redacted_log_path = "/home/user/logs/app_redacted.log"

    assert os.path.isfile(script_path), f"Script missing: {script_path}"
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable"

    assert os.path.isfile(redacted_log_path), f"Redacted log missing: {redacted_log_path}"

    with open(redacted_log_path, "r") as f:
        content = f.read()

    assert "XXXX-XXXX-XXXX-4444" in content, "First credit card was not correctly redacted"
    assert "XXXX-XXXX-XXXX-8888" in content, "Second credit card was not correctly redacted"

    assert "4111-2222-3333-4444" not in content, "Original first credit card is still present in redacted log"
    assert "5555-6666-7777-8888" not in content, "Original second credit card is still present in redacted log"

def test_phase5_audit_summary():
    summary_path = "/home/user/audit_summary.txt"
    cert_path = "/home/user/certs/server.crt"

    assert os.path.isfile(summary_path), f"Summary file missing: {summary_path}"

    with open(summary_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().split("\n")]

    assert len(lines) == 4, f"Expected exactly 4 lines in {summary_path}, got {len(lines)}"

    # Line 1: MD5 hash of server.crt
    if os.path.isfile(cert_path):
        with open(cert_path, "rb") as cf:
            expected_md5 = hashlib.md5(cf.read()).hexdigest()
    else:
        expected_md5 = "CERT_MISSING"

    assert lines[0] == expected_md5, f"Line 1 expected MD5 {expected_md5}, got {lines[0]}"

    # Line 2: Permissions of index.html
    assert lines[1] == "644", f"Line 2 expected '644', got {lines[1]}"

    # Line 3: Number of redacted lines
    assert lines[2] == "2", f"Line 3 expected '2', got {lines[2]}"

    # Line 4: AUDIT_COMPLETE
    assert lines[3] == "AUDIT_COMPLETE", f"Line 4 expected 'AUDIT_COMPLETE', got {lines[3]}"