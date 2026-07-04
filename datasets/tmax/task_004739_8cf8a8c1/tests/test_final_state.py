# test_final_state.py

import os
import re
import subprocess
from pathlib import Path
import pytest

def test_ssh_hardening():
    """Verify SSH key generation and config hardening."""
    ssh_dir = Path("/home/user/.ssh")
    key_path = ssh_dir / "audit_id_ed25519"
    config_path = ssh_dir / "config"

    assert key_path.exists(), f"SSH key not found at {key_path}"
    assert config_path.exists(), f"SSH config not found at {config_path}"

    config_content = config_path.read_text()

    # Check for required directives (case-insensitive for keys, flexible whitespace)
    assert re.search(r'(?i)^\s*PasswordAuthentication\s+no\b', config_content, re.MULTILINE), \
        "SSH config missing 'PasswordAuthentication no'"

    assert re.search(r'(?i)^\s*Ciphers\s+chacha20-poly1305@openssh\.com\b', config_content, re.MULTILINE), \
        "SSH config missing 'Ciphers chacha20-poly1305@openssh.com'"

    # IdentityFile can be absolute or relative to ~
    assert re.search(r'(?i)^\s*IdentityFile\s+(~|/home/user)/\.ssh/audit_id_ed25519\b', config_content, re.MULTILINE), \
        "SSH config missing correct 'IdentityFile' directive"

def test_sanitizer_adversarial_corpus():
    """Verify the sanitizer script against the clean and evil corpora."""
    script_path = Path("/home/user/sanitizer.py")
    assert script_path.exists(), f"Sanitizer script not found at {script_path}"

    clean_dir = Path("/app/corpus/clean")
    evil_dir = Path("/app/corpus/evil")

    assert clean_dir.exists() and clean_dir.is_dir(), "Clean corpus directory missing"
    assert evil_dir.exists() and evil_dir.is_dir(), "Evil corpus directory missing"

    # Test Clean Corpus
    clean_files = list(clean_dir.iterdir())
    failed_clean = []
    for f in clean_files:
        if not f.is_file():
            continue
        original_content = f.read_bytes()
        result = subprocess.run(["python3", str(script_path), str(f)], capture_output=True)
        if result.returncode != 0 or result.stdout != original_content:
            failed_clean.append(f.name)

    # Test Evil Corpus
    evil_files = list(evil_dir.iterdir())
    failed_evil = []
    regex_pattern = re.compile(rb'TRK-[A-Z0-9]{6}-[A-Z0-9]{6}')
    ssh_key_pattern = b'BEGIN OPENSSH PRIVATE KEY'

    for f in evil_files:
        if not f.is_file():
            continue
        result = subprocess.run(["python3", str(script_path), str(f)], capture_output=True)
        if result.returncode != 0:
            failed_evil.append(f.name)
            continue

        output = result.stdout
        if regex_pattern.search(output) or ssh_key_pattern in output:
            failed_evil.append(f.name)

    error_messages = []
    if failed_clean:
        error_messages.append(f"{len(failed_clean)} of {len(clean_files)} clean modified: {', '.join(failed_clean)}")
    if failed_evil:
        error_messages.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")

    assert not error_messages, " | ".join(error_messages)