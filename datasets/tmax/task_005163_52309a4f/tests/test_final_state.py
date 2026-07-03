# test_final_state.py
import os
import stat
import subprocess
import pytest
from pathlib import Path

def test_ssh_audit_fixed():
    """Verify that the ssh-audit.py script has been fixed and runs successfully."""
    script_path = "/app/ssh-audit-3.1.0/ssh-audit.py"
    assert os.path.isfile(script_path), f"ssh-audit script not found at {script_path}"

    result = subprocess.run(
        ["python3", script_path, "-h"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"ssh-audit.py failed to run. Exit code: {result.returncode}, Stderr: {result.stderr}"

def test_validate_auth_keys_filter():
    """Verify the validate_auth_keys.sh script correctly filters evil keys and preserves clean keys."""
    script_path = "/home/user/validate_auth_keys.sh"
    assert os.path.isfile(script_path), f"Filter script not found at {script_path}"

    clean_dir = Path("/app/corpora/clean")
    evil_dir = Path("/app/corpora/evil")

    assert clean_dir.is_dir(), "Clean corpus directory missing."
    assert evil_dir.is_dir(), "Evil corpus directory missing."

    # Test Clean Corpus
    clean_modified = []
    for clean_file in clean_dir.iterdir():
        if clean_file.is_file():
            with open(clean_file, "r") as f:
                original_content = f.read()

            result = subprocess.run(
                ["bash", script_path],
                input=original_content,
                capture_output=True,
                text=True
            )

            if result.stdout != original_content:
                clean_modified.append(clean_file.name)

    # Test Evil Corpus
    evil_bypassed = []
    for evil_file in evil_dir.iterdir():
        if evil_file.is_file():
            with open(evil_file, "r") as f:
                original_content = f.read()

            result = subprocess.run(
                ["bash", script_path],
                input=original_content,
                capture_output=True,
                text=True
            )

            if result.stdout.strip() != "":
                evil_bypassed.append(evil_file.name)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(list(evil_dir.iterdir()))} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(list(clean_dir.iterdir()))} clean modified: {', '.join(clean_modified)}")

    assert not error_msgs, " | ".join(error_msgs)

def test_admin_key_generated():
    """Verify that the admin ed25519 key was generated correctly with proper permissions."""
    key_path = "/home/user/admin_key"
    assert os.path.isfile(key_path), f"Admin key not found at {key_path}"

    # Check permissions
    st = os.stat(key_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Expected permissions 600 for {key_path}, got {oct(perms)}"

    # Check if it's a valid ed25519 private key
    with open(key_path, "r") as f:
        content = f.read()

    assert "BEGIN OPENSSH PRIVATE KEY" in content, "Key does not appear to be a valid OpenSSH private key."

    # Use ssh-keygen to verify it's an ed25519 key and has no passphrase
    result = subprocess.run(
        ["ssh-keygen", "-y", "-P", "", "-f", key_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Key validation failed (might have a passphrase or be invalid). Error: {result.stderr}"
    assert "ssh-ed25519" in result.stdout, "Generated key is not an ed25519 key."