# test_final_state.py

import os
import re
import subprocess
import pytest

def get_expected_issuer():
    """Derive the expected issuer CN from the actual certificate using openssl."""
    cert_path = "/home/user/server/certs/server.crt"
    if not os.path.exists(cert_path):
        return "Vulnerable Pentest CA" # Fallback if cert is missing, though test will fail elsewhere

    try:
        output = subprocess.check_output(
            ["openssl", "x509", "-in", cert_path, "-noout", "-issuer"],
            text=True
        )
        # Example output: issuer=C = US, ST = CA, L = SanFrancisco, O = Pentest Corp, CN = Vulnerable Pentest CA
        match = re.search(r'CN\s*=\s*([^,\n]+)', output)
        if match:
            return match.group(1).strip()
    except subprocess.CalledProcessError:
        pass

    return "Vulnerable Pentest CA"

def get_expected_flag():
    """Extract the expected flag from the Go source code."""
    main_go_path = "/home/user/server/main.go"
    if not os.path.exists(main_go_path):
        return "FLAG{b1t_fl1pp1ng_m4st3r_992}"

    with open(main_go_path, "r") as f:
        content = f.read()
        match = re.search(r'FLAG\{[^}]+\}', content)
        if match:
            return match.group(0)

    return "FLAG{b1t_fl1pp1ng_m4st3r_992}"

def test_issuer_extracted_correctly():
    """Verify that the issuer CN was correctly extracted and saved."""
    issuer_file = "/home/user/issuer.txt"
    assert os.path.isfile(issuer_file), f"The file {issuer_file} does not exist. You must create it."

    with open(issuer_file, "r") as f:
        actual_issuer = f.read().strip()

    expected_issuer = get_expected_issuer()
    assert actual_issuer == expected_issuer, (
        f"The content of {issuer_file} is incorrect. "
        f"Expected '{expected_issuer}', but found '{actual_issuer}'."
    )

def test_flag_extracted_correctly():
    """Verify that the flag was successfully obtained and saved."""
    flag_file = "/home/user/flag.txt"
    assert os.path.isfile(flag_file), f"The file {flag_file} does not exist. You must create it."

    with open(flag_file, "r") as f:
        actual_flag = f.read().strip()

    expected_flag = get_expected_flag()
    assert actual_flag == expected_flag, (
        f"The content of {flag_file} is incorrect. "
        f"Expected '{expected_flag}', but found '{actual_flag}'. "
        "Ensure your bit-flipping exploit successfully forged the admin session."
    )