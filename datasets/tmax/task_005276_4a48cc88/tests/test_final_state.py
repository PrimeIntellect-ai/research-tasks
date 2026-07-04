# test_final_state.py

import os
import hashlib
import subprocess
import pytest

def test_build_payload_exists():
    """Check that build_payload.py exists."""
    path = "/home/user/build_payload.py"
    assert os.path.exists(path), f"{path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

def test_exploit_html_content():
    """Check that exploit.html contains the correct nonce."""
    path = "/home/user/exploit.html"
    assert os.path.exists(path), f"{path} does not exist."

    seed = b"RED_TEAM_SEED_X9_2024_!@#"
    nonce = hashlib.sha256(seed).hexdigest()
    expected_script_tag = f'<script nonce="{nonce}">'

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert expected_script_tag in content, f"Expected script tag {expected_script_tag} not found in {path}."

def test_sshd_config_exfil():
    """Check that sshd_config_exfil has the required hardened settings."""
    path = "/home/user/sshd_config_exfil"
    assert os.path.exists(path), f"{path} does not exist."

    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:
        # Remove comments and strip whitespace
        line = line.split('#')[0].strip().lower()
        if line:
            # Replace multiple spaces with a single space
            line = ' '.join(line.split())
            cleaned_lines.append(line)

    assert "passwordauthentication no" in cleaned_lines, "PasswordAuthentication is not explicitly disabled."

    has_ed25519 = any(
        "pubkeyacceptedalgorithms ssh-ed25519" in line or "pubkeyacceptedkeytypes ssh-ed25519" in line
        for line in cleaned_lines
    )
    assert has_ed25519, "The configuration does not explicitly restrict public key algorithms to ssh-ed25519."

def test_exfil_key():
    """Check that exfil_key exists and is a valid ed25519 private key."""
    path = "/home/user/exfil_key"
    assert os.path.exists(path), f"{path} does not exist."

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    assert content.startswith("-----BEGIN OPENSSH PRIVATE KEY-----"), f"{path} does not appear to be an OpenSSH private key."

    # Verify with ssh-keygen
    try:
        result = subprocess.run(
            ['ssh-keygen', '-l', '-f', path],
            capture_output=True,
            text=True,
            check=True
        )
        assert "ED25519" in result.stdout.upper(), f"Key {path} is not an ED25519 key."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"ssh-keygen failed to read the key {path}: {e.stderr}")