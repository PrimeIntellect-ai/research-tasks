# test_final_state.py

import os
import subprocess
import base64
import codecs
import tempfile
import shutil
import pytest

def test_config_sanitizer_adversarial_corpus():
    sanitizer_path = "/home/user/config_sanitizer"
    assert os.path.exists(sanitizer_path), f"Sanitizer binary not found at {sanitizer_path}"
    assert os.access(sanitizer_path, os.X_OK), f"Sanitizer binary is not executable at {sanitizer_path}"

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    for cf in clean_files:
        with open(cf, 'rb') as f:
            result = subprocess.run([sanitizer_path], stdin=f, capture_output=True)
            if result.returncode != 0:
                clean_failed.append(os.path.basename(cf))

    evil_bypassed = []
    for ef in evil_files:
        with open(ef, 'rb') as f:
            result = subprocess.run([sanitizer_path], stdin=f, capture_output=True)
            if result.returncode == 0:
                evil_bypassed.append(os.path.basename(ef))

    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    assert not error_messages, " | ".join(error_messages)

def test_provision_daemon():
    daemon_path = "/home/user/provision_daemon.sh"
    log_path = "/home/user/provision.log"

    assert os.path.exists(daemon_path), f"Provision daemon not found at {daemon_path}"
    assert os.access(daemon_path, os.X_OK), f"Provision daemon is not executable at {daemon_path}"

    if os.path.exists(log_path):
        os.remove(log_path)

    # We use a clean corpus file
    test_file = "/app/corpus/clean/clean_1.txt"
    assert os.path.exists(test_file), f"Test file {test_file} missing"

    result = subprocess.run([daemon_path, test_file], capture_output=True)
    assert result.returncode == 0, f"Provision daemon failed with exit code {result.returncode}"

    assert os.path.exists(log_path), f"Log file {log_path} was not created"

    with open(log_path, 'r') as f:
        log_contents = f.read().strip().splitlines()

    expected_logs = [
        "[SUCCESS] Applied: useradd jdoe",
        "[SUCCESS] Applied: ip route add 192.168.1.0/24 via 10.0.0.1"
    ]

    assert log_contents == expected_logs, f"Log contents did not match expected. Got: {log_contents}"

def encode_for_decoder(text: str) -> bytes:
    # Decoder does base64 decode then rot13.
    # To encode: rot13 then base64 encode.
    rot13_text = codecs.encode(text, 'rot_13')
    return base64.b64encode(rot13_text.encode('utf-8'))

def test_git_hook():
    repo_path = "/home/user/infra-configs.git"
    hook_path = os.path.join(repo_path, "hooks", "pre-receive")

    assert os.path.exists(repo_path), f"Git repo not found at {repo_path}"
    assert os.path.exists(hook_path), f"pre-receive hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"pre-receive hook is not executable"

    # Create a temporary clone to test pushing
    with tempfile.TemporaryDirectory() as tmpdir:
        clone_dir = os.path.join(tmpdir, "clone")
        subprocess.run(["git", "clone", repo_path, clone_dir], check=True, capture_output=True)

        # Test pushing a safe file
        safe_file_path = os.path.join(clone_dir, "safe.enc")
        safe_content = "useradd alice\n"
        with open(safe_file_path, "wb") as f:
            f.write(encode_for_decoder(safe_content))

        subprocess.run(["git", "config", "user.name", "Test"], cwd=clone_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=clone_dir, check=True)
        subprocess.run(["git", "add", "safe.enc"], cwd=clone_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Add safe config"], cwd=clone_dir, check=True)

        push_safe = subprocess.run(["git", "push", "origin", "master"], cwd=clone_dir, capture_output=True)
        assert push_safe.returncode == 0, f"Pushing safe config failed: {push_safe.stderr.decode()}"

        # Test pushing an evil file
        evil_file_path = os.path.join(clone_dir, "evil.enc")
        evil_content = "useradd bob; rm -rf /\n"
        with open(evil_file_path, "wb") as f:
            f.write(encode_for_decoder(evil_content))

        subprocess.run(["git", "add", "evil.enc"], cwd=clone_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Add evil config"], cwd=clone_dir, check=True)

        push_evil = subprocess.run(["git", "push", "origin", "master"], cwd=clone_dir, capture_output=True)
        assert push_evil.returncode != 0, "Pushing evil config succeeded but should have been rejected by the hook"