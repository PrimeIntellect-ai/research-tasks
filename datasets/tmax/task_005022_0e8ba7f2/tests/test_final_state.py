# test_final_state.py

import os
import re
import base64
import subprocess
import pytest

def get_expected_subject():
    crt_path = "/home/user/server.crt"
    assert os.path.isfile(crt_path), f"Certificate file {crt_path} is missing."
    result = subprocess.run(
        ["openssl", "x509", "-in", crt_path, "-noout", "-subject"],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()

def test_processed_audit_log_contents():
    b64_path = "/home/user/audit_log.b64"
    processed_path = "/home/user/processed_audit.log"

    assert os.path.isfile(b64_path), f"Input file {b64_path} is missing."
    assert os.path.isfile(processed_path), f"Output file {processed_path} is missing."

    with open(b64_path, "r") as f:
        encoded_content = f.read()

    decoded_content = base64.b64decode(encoded_content).decode('utf-8')

    # Redact IP addresses
    ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    redacted_content = re.sub(ipv4_pattern, "[REDACTED_IP]", decoded_content)

    # Check for privilege escalation
    needs_warning = "sudo " in decoded_content or "chmod 777" in decoded_content

    expected_lines = redacted_content.splitlines()
    if needs_warning:
        expected_lines.append("WARNING: PRIVILEGE ESCALATION DETECTED")

    expected_lines.append(get_expected_subject())

    expected_output = "\n".join(expected_lines) + "\n"

    with open(processed_path, "r") as f:
        actual_output = f.read()

    # Strip trailing newlines for comparison to avoid minor formatting differences
    assert actual_output.strip() == expected_output.strip(), (
        f"Contents of {processed_path} do not match the expected output.\n"
        f"Expected:\n{expected_output}\n\nActual:\n{actual_output}"
    )