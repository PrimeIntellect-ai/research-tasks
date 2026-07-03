# test_final_state.py

import os
import json
import re
import glob
import subprocess
import pytest

def test_decrypted_key_validity():
    """Verify the decrypted private key exists, is unencrypted, and is valid."""
    key_path = "/home/user/certs/decrypted_app.key"
    assert os.path.isfile(key_path), f"Decrypted key file is missing at {key_path}."

    with open(key_path, "r") as f:
        content = f.read()

    assert "ENCRYPTED" not in content, f"The key at {key_path} still appears to be encrypted."
    assert "PRIVATE KEY" in content, f"The file at {key_path} does not appear to be a PEM-encoded private key."

    # Use openssl to verify it's a valid RSA key
    result = subprocess.run(
        ["openssl", "rsa", "-in", key_path, "-check", "-noout"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"OpenSSL failed to validate the decrypted key: {result.stderr}"

def test_certificate_validity_and_match():
    """Verify the certificate exists, matches the private key, and has the correct CN."""
    cert_path = "/home/user/certs/app.crt"
    key_path = "/home/user/certs/decrypted_app.key"

    assert os.path.isfile(cert_path), f"Certificate file is missing at {cert_path}."

    # Check Subject CN
    subj_result = subprocess.run(
        ["openssl", "x509", "-in", cert_path, "-subject", "-noout"],
        capture_output=True,
        text=True
    )
    assert subj_result.returncode == 0, f"Failed to read certificate subject: {subj_result.stderr}"

    # OpenSSL output formats can vary slightly (e.g., "subject=CN = secure.local" or "subject= /CN=secure.local")
    # We strip spaces and check for CN=secure.local
    normalized_subj = subj_result.stdout.replace(" ", "")
    assert "CN=secure.local" in normalized_subj, f"Certificate Subject does not contain CN=secure.local. Actual output: {subj_result.stdout.strip()}"

    # Verify the certificate matches the decrypted private key by comparing their moduli
    cert_mod_result = subprocess.run(
        ["openssl", "x509", "-in", cert_path, "-modulus", "-noout"],
        capture_output=True,
        text=True
    )
    key_mod_result = subprocess.run(
        ["openssl", "rsa", "-in", key_path, "-modulus", "-noout"],
        capture_output=True,
        text=True
    )

    assert cert_mod_result.returncode == 0, "Failed to extract certificate modulus."
    assert key_mod_result.returncode == 0, "Failed to extract private key modulus."

    cert_modulus = cert_mod_result.stdout.strip()
    key_modulus = key_mod_result.stdout.strip()

    assert cert_modulus == key_modulus, "The generated certificate does not match the decrypted private key."

def test_leak_report_json():
    """Verify the leak report exists and matches the expected derived JSON output."""
    report_path = "/home/user/leak_report.json"
    scripts_dir = "/home/user/scripts"

    assert os.path.isfile(report_path), f"Leak report is missing at {report_path}."

    # Derive the expected state based on the task rules
    expected_leaks = []
    script_files = glob.glob(os.path.join(scripts_dir, "*.sh"))

    for filepath in script_files:
        with open(filepath, "r") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            # Look for exact string '--password=' or '-p ' followed by non-whitespace
            match_long = re.search(r'--password=(\S+)', line)
            match_short = re.search(r'-p (\S+)', line)

            if match_long:
                expected_leaks.append({
                    "file": filepath,
                    "line_number": i + 1,
                    "leaked_password": match_long.group(1)
                })
            elif match_short:
                expected_leaks.append({
                    "file": filepath,
                    "line_number": i + 1,
                    "leaked_password": match_short.group(1)
                })

    # Sort expected leaks by file, then line number
    expected_leaks.sort(key=lambda x: (x["file"], x["line_number"]))
    expected_json = {"leaks": expected_leaks}

    # Read and parse the actual report
    with open(report_path, "r") as f:
        try:
            actual_json = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {report_path} does not contain valid JSON.")

    assert "leaks" in actual_json, "The JSON report is missing the top-level 'leaks' key."
    assert isinstance(actual_json["leaks"], list), "The 'leaks' key must contain a list."

    # Sort actual leaks to ensure order doesn't cause a false failure if the student didn't sort
    # (Though the prompt asked them to sort, we sort here to compare content accurately, 
    # and then we can also assert exact match to enforce the sorting rule).
    actual_leaks_sorted = sorted(actual_json["leaks"], key=lambda x: (x.get("file", ""), x.get("line_number", 0)))

    # First check if the contents match
    assert actual_leaks_sorted == expected_leaks, f"The extracted leaks do not match the expected findings. Expected: {expected_leaks}, Actual: {actual_leaks_sorted}"

    # Then enforce the exact sorting rule requested in the prompt
    assert actual_json["leaks"] == expected_leaks, "The 'leaks' list is correct but not sorted by file name and line number ascending as requested."