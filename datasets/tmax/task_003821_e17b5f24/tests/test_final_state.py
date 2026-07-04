# test_final_state.py

import os
import stat
import hashlib
import re
import pytest

WORKSPACE_DIR = "/home/user/workspace"
EXTRACTED_DIR = os.path.join(WORKSPACE_DIR, "extracted")
REPORT_PATH = os.path.join(WORKSPACE_DIR, "report.txt")
SSH_KEY_PATH = "/home/user/.ssh/id_rsa"
SSHD_CONFIG_PATH = os.path.join(EXTRACTED_DIR, "sshd_config")
REDACTED_LOG_PATH = os.path.join(WORKSPACE_DIR, "db_backup_redacted.log")

def test_report_exists_and_content():
    assert os.path.isfile(REPORT_PATH), f"Report file {REPORT_PATH} does not exist."

    with open(REPORT_PATH, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n')]

    assert len(lines) == 3, f"Report should have exactly 3 lines, found {len(lines)}."

    assert lines[0] == "dragonfly2023", f"Line 1 of report should be 'dragonfly2023', got '{lines[0]}'."
    assert lines[1] == "legacy.internal.corp", f"Line 2 of report should be 'legacy.internal.corp', got '{lines[1]}'."

    assert os.path.isfile(SSHD_CONFIG_PATH), f"Extracted sshd_config does not exist at {SSHD_CONFIG_PATH}."

    with open(SSHD_CONFIG_PATH, "rb") as f:
        sshd_config_content = f.read()
    expected_hash = hashlib.sha256(sshd_config_content).hexdigest()

    assert lines[2] == expected_hash, f"Line 3 of report should be the SHA256 sum of sshd_config ({expected_hash}), got '{lines[2]}'."

def test_ssh_key_permissions():
    assert os.path.isfile(SSH_KEY_PATH), f"SSH key {SSH_KEY_PATH} does not exist."
    st = os.stat(SSH_KEY_PATH)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"SSH key {SSH_KEY_PATH} must have 600 permissions, got {oct(perms)}."

def test_sshd_config_hardened():
    assert os.path.isfile(SSHD_CONFIG_PATH), f"Extracted sshd_config does not exist at {SSHD_CONFIG_PATH}."
    with open(SSHD_CONFIG_PATH, "r") as f:
        content = f.read()

    assert "PermitEmptyPasswords no" in content, "sshd_config does not contain 'PermitEmptyPasswords no'."
    assert "PermitEmptyPasswords yes" not in content, "sshd_config still contains 'PermitEmptyPasswords yes'."

def test_db_backup_redacted():
    assert os.path.isfile(REDACTED_LOG_PATH), f"Redacted log file {REDACTED_LOG_PATH} does not exist."
    with open(REDACTED_LOG_PATH, "r") as f:
        content = f.read()

    # Check that there are no AKIA keys left
    matches = re.findall(r"AKIA[A-Z0-9]{16}", content)
    assert len(matches) == 0, f"Found unredacted API keys in {REDACTED_LOG_PATH}: {matches}"

    # Check that redaction string is present
    assert "[REDACTED]" in content, f"Redaction string '[REDACTED]' not found in {REDACTED_LOG_PATH}."