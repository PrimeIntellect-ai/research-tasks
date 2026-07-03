# test_final_state.py

import os
import subprocess
import pytest
import hashlib

WAF_SCRIPT = "/home/user/waf_filter.sh"
NETWORK_SCRIPT = "/home/user/network_harden.sh"
SSH_SCRIPT = "/home/user/ssh_harden.sh"

EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
AUTHORIZED_KEYS_PATH = "/home/user/.ssh/authorized_keys"
CHECKSUM_PATH = "/home/user/.ssh/authorized_keys.sha256"

def test_scripts_exist_and_executable():
    for script in [WAF_SCRIPT, NETWORK_SCRIPT, SSH_SCRIPT]:
        assert os.path.isfile(script), f"Expected script {script} does not exist."
        assert os.access(script, os.X_OK), f"Expected script {script} to be executable."

def test_waf_filter_adversarial_corpus():
    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if os.path.isfile(os.path.join(EVIL_CORPUS_DIR, f))]
    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if os.path.isfile(os.path.join(CLEAN_CORPUS_DIR, f))]

    bypassed_evil = []
    modified_clean = []

    for evil_file in evil_files:
        result = subprocess.run(["/bin/bash", WAF_SCRIPT, evil_file], capture_output=True, text=True)
        output = result.stdout.strip()
        if result.returncode != 1 or output != "EVIL":
            bypassed_evil.append(os.path.basename(evil_file))

    for clean_file in clean_files:
        result = subprocess.run(["/bin/bash", WAF_SCRIPT, clean_file], capture_output=True, text=True)
        output = result.stdout.strip()
        if result.returncode != 0 or output != "CLEAN":
            modified_clean.append(os.path.basename(clean_file))

    error_msg = []
    if bypassed_evil:
        error_msg.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_msg.append(f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}")

    assert not error_msg, "WAF Filter failed: " + "; ".join(error_msg)

def test_network_harden_script_contents():
    with open(NETWORK_SCRIPT, "r") as f:
        content = f.read()

    # Check for blocking port 8080
    assert ("8080" in content and ("DROP" in content or "REJECT" in content)), \
        "Network harden script does not appear to block TCP port 8080."

    # Check for allowing port 443
    assert ("443" in content and "ACCEPT" in content), \
        "Network harden script does not appear to explicitly allow TCP port 443."

def test_ssh_harden_script():
    # Setup mock authorized_keys
    os.makedirs(os.path.dirname(AUTHORIZED_KEYS_PATH), exist_ok=True)

    initial_keys = [
        "ssh-rsa AAAAB3NzaC1yc2E... user1@host",
        "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5... user2@host",
        "ssh-dss AAAAB3NzaC1kc3M... user3@host",
        "ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTY... user4@host"
    ]

    with open(AUTHORIZED_KEYS_PATH, "w") as f:
        f.write("\n".join(initial_keys) + "\n")

    # Run the student's script
    result = subprocess.run(["/bin/bash", SSH_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"SSH harden script failed with error: {result.stderr}"

    # Verify the cleaned keys
    assert os.path.isfile(AUTHORIZED_KEYS_PATH), "authorized_keys file was deleted."
    with open(AUTHORIZED_KEYS_PATH, "r") as f:
        cleaned_keys = f.read().splitlines()

    for key in cleaned_keys:
        assert not key.startswith("ssh-rsa"), "ssh-rsa key was not removed."
        assert not key.startswith("ssh-dss"), "ssh-dss key was not removed."

    assert any(key.startswith("ssh-ed25519") for key in cleaned_keys), "Valid ssh-ed25519 key was incorrectly removed."
    assert any(key.startswith("ecdsa-sha2-nistp256") for key in cleaned_keys), "Valid ecdsa key was incorrectly removed."

    # Verify the checksum
    assert os.path.isfile(CHECKSUM_PATH), f"Checksum file {CHECKSUM_PATH} was not created."

    with open(AUTHORIZED_KEYS_PATH, "rb") as f:
        expected_hash = hashlib.sha256(f.read()).hexdigest()

    with open(CHECKSUM_PATH, "r") as f:
        actual_checksum_content = f.read().strip()

    assert expected_hash in actual_checksum_content, "The SHA256 checksum does not match the cleaned authorized_keys file."