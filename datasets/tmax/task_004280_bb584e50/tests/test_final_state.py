# test_final_state.py

import os
import subprocess
import shutil
import tempfile
import pytest

CHECK_TLS_PATH = "/home/user/check_tls.py"
PRE_RECEIVE_HOOK = "/home/user/proxy-repo.git/hooks/pre-receive"
REPO_PATH = "/home/user/proxy-repo.git"

def test_check_tls_exists_and_executable():
    assert os.path.isfile(CHECK_TLS_PATH), f"{CHECK_TLS_PATH} does not exist."
    assert os.access(CHECK_TLS_PATH, os.X_OK), f"{CHECK_TLS_PATH} is not executable."

def test_check_tls_logic():
    # Test cases: (input_text, expected_exit_code, expected_output)
    test_cases = [
        ("ssl_protocols TLSv1.2 TLSv1.3;", 0, ""),
        ("ssl_protocols TLSv1.1 TLSv1.2;", 1, "WEAK TLS DETECTED\n"),
        ("ssl_protocols TLSv1 TLSv1.2;", 1, "WEAK TLS DETECTED\n"),
        ("ssl_protocols TLSv1; TLSv1.2;", 1, "WEAK TLS DETECTED\n"),
        ("TLSv1.3 only", 0, ""),
        ("TLSv1.1", 1, "WEAK TLS DETECTED\n"),
    ]

    for input_text, expected_code, expected_output in test_cases:
        process = subprocess.Popen(
            [CHECK_TLS_PATH],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=input_text)

        assert process.returncode == expected_code, f"Expected exit code {expected_code} for input '{input_text}', got {process.returncode}"
        if expected_code == 1:
            assert expected_output.strip() in stdout.strip(), f"Expected '{expected_output.strip()}' in stdout for input '{input_text}', got '{stdout}'"

def test_pre_receive_hook_exists_and_executable():
    assert os.path.isfile(PRE_RECEIVE_HOOK), f"{PRE_RECEIVE_HOOK} does not exist."
    assert os.access(PRE_RECEIVE_HOOK, os.X_OK), f"{PRE_RECEIVE_HOOK} is not executable."

def test_git_push_hook_integration():
    test_repo_dir = tempfile.mkdtemp()
    try:
        # Initialize test repo
        subprocess.run(["git", "init"], cwd=test_repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "remote", "add", "origin", REPO_PATH], cwd=test_repo_dir, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=test_repo_dir, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=test_repo_dir, check=True)

        # 1. Test pushing a good config
        good_conf_path = os.path.join(test_repo_dir, "good.conf")
        with open(good_conf_path, "w") as f:
            f.write("server {\n    listen 443 ssl;\n    ssl_protocols TLSv1.2 TLSv1.3;\n}\n")

        subprocess.run(["git", "add", "good.conf"], cwd=test_repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Add good config"], cwd=test_repo_dir, check=True, capture_output=True)

        push_good = subprocess.run(["git", "push", "origin", "master"], cwd=test_repo_dir, capture_output=True, text=True)
        assert push_good.returncode == 0, f"Pushing good config failed: {push_good.stderr}"

        # 2. Test pushing a bad config
        bad_conf_path = os.path.join(test_repo_dir, "bad.conf")
        with open(bad_conf_path, "w") as f:
            f.write("server {\n    listen 443 ssl;\n    ssl_protocols TLSv1.1 TLSv1.2;\n}\n")

        subprocess.run(["git", "add", "bad.conf"], cwd=test_repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Add bad config"], cwd=test_repo_dir, check=True, capture_output=True)

        push_bad = subprocess.run(["git", "push", "origin", "master"], cwd=test_repo_dir, capture_output=True, text=True)
        assert push_bad.returncode != 0, "Pushing bad config should have been rejected."
        assert "WEAK TLS DETECTED" in push_bad.stderr or "WEAK TLS DETECTED" in push_bad.stdout, "Expected 'WEAK TLS DETECTED' in hook output."

    finally:
        shutil.rmtree(test_repo_dir)