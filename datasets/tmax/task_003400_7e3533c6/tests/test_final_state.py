# test_final_state.py
import os
import stat
import subprocess
import pytest

def test_compromised_files_list():
    compromised_file = "/home/user/audit/compromised.txt"
    assert os.path.isfile(compromised_file), f"Missing {compromised_file}"

    with open(compromised_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["log2.txt", "log3.txt"]
    assert lines == expected, f"Expected {expected} in compromised.txt, got {lines}"

def test_tls_certificate_and_key():
    cert_file = "/home/user/audit/cert.pem"
    key_file = "/home/user/audit/key.pem"

    assert os.path.isfile(cert_file), f"Missing {cert_file}"
    assert os.path.isfile(key_file), f"Missing {key_file}"

    # Check certificate subject
    subject_cmd = ["openssl", "x509", "-in", cert_file, "-noout", "-subject"]
    result = subprocess.run(subject_cmd, capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read certificate with openssl"
    assert "vulnerable.local" in result.stdout, f"Certificate subject does not contain 'vulnerable.local': {result.stdout}"

    # Check private key validity
    key_cmd = ["openssl", "rsa", "-in", key_file, "-check", "-noout"]
    result = subprocess.run(key_cmd, capture_output=True, text=True)
    assert result.returncode == 0, "Private key is invalid or encrypted with a passphrase"

    # Check if cert and key match
    cert_mod_cmd = ["openssl", "x509", "-in", cert_file, "-noout", "-modulus"]
    key_mod_cmd = ["openssl", "rsa", "-in", key_file, "-noout", "-modulus"]

    cert_mod = subprocess.run(cert_mod_cmd, capture_output=True, text=True).stdout.strip()
    key_mod = subprocess.run(key_mod_cmd, capture_output=True, text=True).stdout.strip()

    assert cert_mod == key_mod, "Certificate and private key do not match"

def test_vulnerability_payload():
    vuln_script = "/home/user/audit/scripts/vuln.sh"
    pwned_file = "/home/user/audit/pwned.txt"

    assert os.path.isfile(vuln_script), f"Missing {vuln_script}"

    # Check permissions are still world-writable
    st = os.stat(vuln_script)
    mode = stat.S_IMODE(st.st_mode)
    assert mode & stat.S_IWOTH, f"{vuln_script} is no longer world-writable"

    # Check original content is preserved
    with open(vuln_script, "r") as f:
        content = f.read()
    assert "Processing data..." in content, "Original content of vuln.sh was overwritten"

    # Clean up pwned.txt if it exists from manual testing
    if os.path.exists(pwned_file):
        os.remove(pwned_file)

    # Execute the script
    result = subprocess.run([vuln_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Execution of {vuln_script} failed"

    # Verify pwned.txt was created and contains correct text
    assert os.path.isfile(pwned_file), f"Payload did not create {pwned_file}"
    with open(pwned_file, "r") as f:
        pwned_content = f.read().strip()

    assert pwned_content == "EXPLOITED", f"Expected 'EXPLOITED' in {pwned_file}, got '{pwned_content}'"