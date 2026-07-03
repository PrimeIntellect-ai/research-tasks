# test_final_state.py

import os
import stat
import subprocess
import re

def test_audit_runner_modified():
    path = "/home/user/audit_runner.py"
    assert os.path.exists(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert '["/home/user/scanner.sh", args.token]' not in content, "The audit_runner.py script still passes the token via CLI arguments."

def test_audit_log_redacted():
    path = "/home/user/audit_log.txt"
    assert os.path.exists(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "[REDACTED]" in content, "The string [REDACTED] was not found in the audit log."
    assert "super_secret_audit_token_991" not in content, "The sensitive token was found in the audit log."

def test_payload_decoded():
    path = "/home/user/payload.txt"
    assert os.path.exists(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "CRITICAL_VULN_FOUND:CVE-2023-12345", f"Content of {path} is incorrect."

def test_ssh_key_exists_and_perms():
    key_path = "/home/user/.ssh/audit_key"
    assert os.path.exists(key_path), f"SSH key {key_path} is missing."
    with open(key_path, "r") as f:
        content = f.read()
    assert "OPENSSH PRIVATE KEY" in content, f"File {key_path} does not appear to be a valid OpenSSH private key."

    st = os.stat(key_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Permissions for {key_path} are {oct(perms)}, expected 0o600."

def test_ssh_config():
    config_path = "/home/user/.ssh/config"
    assert os.path.exists(config_path), f"SSH config {config_path} is missing."
    with open(config_path, "r") as f:
        content = f.read().lower()

    assert re.search(r"passwordauthentication\s+no", content), "PasswordAuthentication no is missing or incorrectly configured in SSH config."
    assert re.search(r"identityfile\s+/home/user/\.ssh/audit_key", content), "IdentityFile is missing or incorrectly configured in SSH config."

def test_tls_certs():
    crt_path = "/home/user/certs/audit_server.crt"
    key_path = "/home/user/certs/audit_server.key"
    assert os.path.exists(crt_path), f"Certificate {crt_path} is missing."
    assert os.path.exists(key_path), f"Private key {key_path} is missing."

    result = subprocess.run(
        ["openssl", "x509", "-in", crt_path, "-noout", "-subject"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to read certificate with openssl."
    assert "CN = audit.local" in result.stdout or "CN=audit.local" in result.stdout, "The Common Name (CN) of the certificate is not set to audit.local."