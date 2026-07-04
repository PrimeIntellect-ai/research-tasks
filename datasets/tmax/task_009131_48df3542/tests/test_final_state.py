# test_final_state.py

import os
import re
import pytest

def test_stolen_key_exists_and_valid():
    """Verify that the exploit successfully retrieved the SSH key."""
    key_path = "/home/user/stolen_key.pem"
    assert os.path.exists(key_path), f"The file {key_path} does not exist. Did the exploit run successfully?"

    with open(key_path, "r") as f:
        content = f.read()

    assert "BEGIN OPENSSH PRIVATE KEY" in content, (
        f"The file {key_path} does not contain a valid OpenSSH private key. "
        "Ensure your exploit correctly bypassed the JWT validation and saved the exact response body."
    )

def test_audit_log_redaction():
    """Verify that the audit log was correctly redacted."""
    original_log_path = "/home/user/audit.log"
    clean_log_path = "/home/user/audit_clean.log"

    assert os.path.exists(original_log_path), f"The original log file {original_log_path} is missing."
    assert os.path.exists(clean_log_path), f"The redacted log file {clean_log_path} is missing."

    with open(original_log_path, "r") as f:
        original_lines = f.readlines()

    with open(clean_log_path, "r") as f:
        clean_lines = f.readlines()

    assert len(original_lines) == len(clean_lines), (
        f"The redacted log has {len(clean_lines)} lines, but the original has {len(original_lines)}. "
        "Lines should not be added or removed."
    )

    for i, (orig, clean) in enumerate(zip(original_lines, clean_lines)):
        # Derive expected line
        expected = re.sub(r'(Bearer\s+)[^\s]+', r'\g<1>[REDACTED]', orig)
        expected = re.sub(r'(password=)[^\s&]+', r'\g<1>[REDACTED]', expected)

        assert clean.strip() == expected.strip(), (
            f"Line {i+1} in {clean_log_path} was not redacted correctly.\n"
            f"Expected: {expected.strip()}\n"
            f"Found:    {clean.strip()}"
        )

def test_sshd_config_policy():
    """Verify that the SSH hardening policy contains the required directives."""
    policy_path = "/home/user/sshd_config.policy"
    assert os.path.exists(policy_path), f"The SSH policy file {policy_path} is missing."

    with open(policy_path, "r") as f:
        content = f.read().lower()

    # We check line by line to ensure the directives are present and properly configured
    lines = [line.strip() for line in content.splitlines() if line.strip()]

    required_directives = {
        "permitrootlogin no",
        "passwordauthentication no",
        "x11forwarding no"
    }

    found_directives = set()
    for line in lines:
        # Normalize whitespace
        normalized_line = re.sub(r'\s+', ' ', line)
        if normalized_line in required_directives:
            found_directives.add(normalized_line)

    missing = required_directives - found_directives
    assert not missing, (
        f"The SSH policy file {policy_path} is missing or has incorrect values for the following directives: "
        f"{', '.join(missing)}"
    )