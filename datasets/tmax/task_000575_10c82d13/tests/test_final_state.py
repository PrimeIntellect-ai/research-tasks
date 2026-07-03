# test_final_state.py

import os
import subprocess
import pytest

def test_pki_certificates():
    """Verify that the TLS certificates are correctly generated."""
    pki_dir = '/home/user/pki'
    crt_file = os.path.join(pki_dir, 'server.crt')
    key_file = os.path.join(pki_dir, 'server.key')

    assert os.path.isdir(pki_dir), f"Directory {pki_dir} does not exist."
    assert os.path.isfile(crt_file), f"Certificate {crt_file} does not exist."
    assert os.path.isfile(key_file), f"Private key {key_file} does not exist."

    # Check certificate properties using openssl
    result = subprocess.run(['openssl', 'x509', '-in', crt_file, '-noout', '-text'], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to parse certificate {crt_file}."
    assert "CN = localhost" in result.stdout or "CN=localhost" in result.stdout, "Certificate does not have CN=localhost."

    # Check private key validity
    result_key = subprocess.run(['openssl', 'rsa', '-in', key_file, '-check', '-noout'], capture_output=True, text=True)
    assert result_key.returncode == 0, f"Private key {key_file} is invalid."


def test_server_binary_behavior():
    """Verify that the C++ code is patched and compiled properly."""
    binary = '/home/user/server'
    assert os.path.isfile(binary), f"Compiled binary {binary} does not exist."
    assert os.access(binary, os.X_OK), f"Binary {binary} is not executable."

    # Test that the vulnerability is patched (should reject 'sig:none')
    res_bypass = subprocess.run([binary, "admin|sig:none"], capture_output=True, text=True)
    assert res_bypass.returncode == 1, "Server still accepts 'admin|sig:none' (vulnerability not patched)."

    # Test that a legitimate token is accepted
    res_valid = subprocess.run([binary, "admin|sig:VALID_MAC"], capture_output=True, text=True)
    assert res_valid.returncode == 0, "Server rejects valid token 'admin|sig:VALID_MAC'."


def test_sandbox_script():
    """Verify that the sandboxing script contains the required bwrap flags."""
    script = '/home/user/run_secure.sh'
    assert os.path.isfile(script), f"Script {script} does not exist."
    assert os.access(script, os.X_OK), f"Script {script} is not executable."

    with open(script, 'r') as f:
        content = f.read()

    assert 'bwrap' in content, "Script does not use 'bwrap'."
    assert '--unshare-net' in content, "Script does not isolate network (--unshare-net)."
    assert '--ro-bind / /' in content, "Script does not mount root as read-only (--ro-bind / /)."
    assert '/home/user/server' in content, "Script does not execute /home/user/server."


def test_suid_audit():
    """Verify that the privilege escalation auditing found the correct SUID binary."""
    audit_file = '/home/user/suid_audit.txt'
    assert os.path.isfile(audit_file), f"Audit file {audit_file} does not exist."

    with open(audit_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 1, f"Audit file should contain exactly 1 line, found {len(lines)}."
    assert lines[0] == '/home/user/test_env/fake_sudo', f"Audit file contains incorrect SUID file path: {lines[0]}."