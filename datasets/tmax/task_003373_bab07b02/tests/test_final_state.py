# test_final_state.py

import os
import subprocess
import glob
import pytest
import socket

def test_git_repo_is_bare():
    repo_dir = "/home/user/sre-repo.git"
    assert os.path.isdir(repo_dir), f"Git repo directory {repo_dir} does not exist."

    # Check if it's a bare repo
    config_path = os.path.join(repo_dir, "config")
    assert os.path.isfile(config_path), f"Git config missing in {repo_dir}."

    with open(config_path, "r") as f:
        content = f.read()
    assert "bare = true" in content.lower(), f"Repository at {repo_dir} is not a bare repository."

def test_pre_receive_hook_deployed():
    hook_path = "/home/user/sre-repo.git/hooks/pre-receive"
    assert os.path.isfile(hook_path), f"pre-receive hook missing at {hook_path}."
    assert os.access(hook_path, os.X_OK), f"pre-receive hook at {hook_path} is not executable."

def test_ssh_tunnel_active():
    # Check if port 9999 is listening
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(2)
        result = s.connect_ex(('127.0.0.1', 9999))
        assert result == 0, "Port 9999 is not listening (SSH tunnel not active)."

        # Verify it speaks SSH
        s.sendall(b"SSH-2.0-Test\r\n")
        response = s.recv(1024)
        assert b"SSH" in response, "Port 9999 is listening but does not appear to be an SSH tunnel."
    finally:
        s.close()

def test_detector_binary_exists():
    binary_path = "/home/user/detector"
    assert os.path.isfile(binary_path), f"Detector binary missing at {binary_path}."
    assert os.access(binary_path, os.X_OK), f"Detector at {binary_path} is not executable."

def test_detector_adversarial_corpus():
    binary_path = "/home/user/detector"
    evil_dir = "/app/corpora/evil"
    clean_dir = "/app/corpora/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*"))
    clean_files = glob.glob(os.path.join(clean_dir, "*"))

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_failures = []
    for f in evil_files:
        try:
            output = subprocess.check_output([binary_path, f], text=True, stderr=subprocess.STDOUT).strip()
            if output != "EVIL":
                evil_failures.append(os.path.basename(f))
        except subprocess.CalledProcessError as e:
            evil_failures.append(f"{os.path.basename(f)} (crashed/errored)")

    clean_failures = []
    for f in clean_files:
        try:
            output = subprocess.check_output([binary_path, f], text=True, stderr=subprocess.STDOUT).strip()
            if output != "CLEAN":
                clean_failures.append(os.path.basename(f))
        except subprocess.CalledProcessError as e:
            clean_failures.append(f"{os.path.basename(f)} (crashed/errored)")

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/flagged: {', '.join(clean_failures)}")

    assert not evil_failures and not clean_failures, " / ".join(error_messages)