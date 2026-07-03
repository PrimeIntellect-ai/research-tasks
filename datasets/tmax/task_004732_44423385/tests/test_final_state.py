# test_final_state.py

import os
import subprocess
import hashlib
import pytest

def test_audit_trail_txt():
    audit_file = "/home/user/audit_trail.txt"
    assert os.path.isfile(audit_file), f"File {audit_file} is missing"

    # Derive expected audit trail
    base_dir = "/home/user/proc_dump"
    expected_entries = []

    if os.path.isdir(base_dir):
        for pid in os.listdir(base_dir):
            if not pid.isdigit():
                continue
            cmdline_path = os.path.join(base_dir, pid, "cmdline")
            if os.path.isfile(cmdline_path):
                with open(cmdline_path, "rb") as f:
                    args = f.read().split(b"\0")
                    for arg in args:
                        arg_str = arg.decode("utf-8", errors="ignore")
                        if arg_str.startswith("--secret-token="):
                            token = arg_str.split("=", 1)[1]
                            expected_entries.append((int(pid), f"{pid}:{token}"))

    expected_entries.sort(key=lambda x: x[0])
    expected_lines = [e[1] for e in expected_entries]
    expected_content = "\n".join(expected_lines) + "\n"

    with open(audit_file, "r") as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), f"Content of {audit_file} does not match expected output."

def test_audit_trail_enc():
    enc_file = "/home/user/audit_trail.enc"
    key_file = "/home/user/audit.key"
    audit_file = "/home/user/audit_trail.txt"

    assert os.path.isfile(enc_file), f"File {enc_file} is missing"
    assert os.path.isfile(key_file), f"File {key_file} is missing"
    assert os.path.isfile(audit_file), f"File {audit_file} is missing"

    # Decrypt using openssl
    cmd = [
        "openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2",
        "-pass", f"file:{key_file}",
        "-in", enc_file
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert result.returncode == 0, f"Failed to decrypt {enc_file}. OpenSSL error: {result.stderr.decode()}"

    decrypted_content = result.stdout.decode("utf-8")

    with open(audit_file, "r") as f:
        expected_content = f.read()

    assert decrypted_content.strip() == expected_content.strip(), f"Decrypted content of {enc_file} does not match {audit_file}"

def test_compromised_files_txt():
    compromised_file = "/home/user/compromised_files.txt"
    manifest_file = "/home/user/manifest.sha256"
    web_app_dir = "/home/user/web_app"

    assert os.path.isfile(compromised_file), f"File {compromised_file} is missing"
    assert os.path.isfile(manifest_file), f"File {manifest_file} is missing"

    expected_compromised = []

    with open(manifest_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(None, 1)
            if len(parts) != 2:
                continue
            expected_hash, filename = parts

            # Remove leading asterisk or space from sha256sum output format
            if filename.startswith("*") or filename.startswith(" "):
                filename = filename[1:]

            full_path = os.path.join(web_app_dir, filename)

            if not os.path.isfile(full_path):
                expected_compromised.append(filename)
            else:
                with open(full_path, "rb") as target_f:
                    actual_hash = hashlib.sha256(target_f.read()).hexdigest()
                if actual_hash != expected_hash:
                    expected_compromised.append(filename)

    expected_compromised.sort()

    with open(compromised_file, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_compromised, f"Content of {compromised_file} does not match expected compromised files."

def test_csp_header_txt():
    csp_file = "/home/user/csp_header.txt"
    domains_file = "/home/user/trusted_domains.txt"

    assert os.path.isfile(csp_file), f"File {csp_file} is missing"
    assert os.path.isfile(domains_file), f"File {domains_file} is missing"

    with open(domains_file, "r") as f:
        domains = [line.strip() for line in f if line.strip()]

    domains_str = " ".join(domains)
    expected_csp = f"Content-Security-Policy: default-src 'self'; script-src 'self' {domains_str};"

    with open(csp_file, "r") as f:
        actual_csp = f.read().strip()

    assert actual_csp == expected_csp, f"Content of {csp_file} does not match expected CSP header."