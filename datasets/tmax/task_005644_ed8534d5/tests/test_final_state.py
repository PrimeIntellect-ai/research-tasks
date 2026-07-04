# test_final_state.py

import os
import subprocess

def test_attacker_ip_extracted():
    ip_file = "/home/user/attacker_ip.txt"
    assert os.path.isfile(ip_file), f"File not found: {ip_file}"

    with open(ip_file, "r") as f:
        content = f.read().strip()

    assert content == "192.168.137.42", f"Expected IP '192.168.137.42', but found '{content}' in {ip_file}"

def test_c_program_exists_and_compiled():
    c_file = "/home/user/decrypt.c"
    bin_file = "/home/user/decrypt"

    assert os.path.isfile(c_file), f"C source file not found: {c_file}"
    with open(c_file, "r") as f:
        c_code = f.read()
    assert "main" in c_code, f"C source file {c_file} does not appear to contain a main function"

    assert os.path.isfile(bin_file), f"Compiled binary not found: {bin_file}"
    assert os.access(bin_file, os.X_OK), f"Compiled binary is not executable: {bin_file}"

def test_tls_certificate_and_key():
    cert_file = "/home/user/cert.pem"
    key_file = "/home/user/key.pem"

    assert os.path.isfile(cert_file), f"Certificate file not found: {cert_file}"
    assert os.path.isfile(key_file), f"Key file not found: {key_file}"

    # Check key validity
    key_check = subprocess.run(
        ["openssl", "rsa", "-in", key_file, "-check", "-noout"],
        capture_output=True, text=True
    )
    assert key_check.returncode == 0, f"Invalid RSA key in {key_file}:\n{key_check.stderr}"

    # Check certificate subject
    cert_subject = subprocess.run(
        ["openssl", "x509", "-in", cert_file, "-noout", "-subject"],
        capture_output=True, text=True
    )
    assert cert_subject.returncode == 0, f"Failed to read certificate {cert_file}:\n{cert_subject.stderr}"
    subject_output = cert_subject.stdout.strip()
    assert "CN = secure-service" in subject_output or "CN=secure-service" in subject_output, \
        f"Certificate does not have Common Name 'secure-service'. Subject found: {subject_output}"

    # Check RSA key size (2048-bit)
    key_size_check = subprocess.run(
        ["openssl", "rsa", "-in", key_file, "-text", "-noout"],
        capture_output=True, text=True
    )
    assert "Private-Key: (2048 bit" in key_size_check.stdout, \
        "RSA key is not 2048-bit as requested."