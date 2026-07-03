# test_final_state.py

import os
import stat
import re
import pytest

AUDIT_LOG_PATH = "/home/user/vault/audit.log"
MASTER_KEY_PATH = "/home/user/vault/config/master.key"

def test_audit_log_exists():
    """Check if the audit log exists."""
    assert os.path.isfile(AUDIT_LOG_PATH), f"FAIL: {AUDIT_LOG_PATH} does not exist."

def test_master_key_state():
    """Check if the master.key exists, has correct content, and correct restored permissions (0600)."""
    assert os.path.isfile(MASTER_KEY_PATH), f"FAIL: {MASTER_KEY_PATH} does not exist."

    with open(MASTER_KEY_PATH, "r") as f:
        content = f.read().strip()
    assert content == "SECRET_KEY_DATA", f"FAIL: {MASTER_KEY_PATH} content is incorrect."

    st = os.stat(MASTER_KEY_PATH)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"FAIL: {MASTER_KEY_PATH} does not have 0600 permissions. Got: {oct(perms)}"

def test_audit_log_contents():
    """Check the audit log contents for exact sequence of LOCKED and UNLOCKED and idempotency."""
    assert os.path.isfile(AUDIT_LOG_PATH), f"FAIL: {AUDIT_LOG_PATH} does not exist."

    with open(AUDIT_LOG_PATH, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 2, f"FAIL: audit.log contains extra lines. Expected exactly 2 non-empty lines, found {len(lines)}."

    locked_pattern = re.compile(r"^LOCKED \d{10,}$")
    unlocked_pattern = re.compile(r"^UNLOCKED \d{10,}$")

    assert locked_pattern.match(lines[0]), f"FAIL: First line of audit.log does not match expected LOCKED format. Got: '{lines[0]}'"
    assert unlocked_pattern.match(lines[1]), f"FAIL: Second line of audit.log does not match expected UNLOCKED format. Got: '{lines[1]}'"