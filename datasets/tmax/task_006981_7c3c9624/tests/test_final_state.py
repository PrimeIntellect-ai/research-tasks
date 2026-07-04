# test_final_state.py

import os
import socket
import subprocess
import pytest

def test_deployment_output_log_exists_and_correct():
    log_path = "/home/user/deployment_output.log"
    assert os.path.isfile(log_path), f"Output log file {log_path} does not exist. The pipeline may not have run or failed."

    with open(log_path, "r") as f:
        content = f.read()
        assert "SECRET_CONFIG_99281" in content, "The output log does not contain the expected secret 'SECRET_CONFIG_99281'."

def test_git_post_commit_hook_configured():
    hook_path = "/home/user/repo/.git/hooks/post-commit"
    assert os.path.isfile(hook_path), f"Git hook {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Git hook {hook_path} is not executable."

    with open(hook_path, "r") as f:
        content = f.read()
        assert "g++" in content, "The post-commit hook does not appear to compile the code using g++."
        assert "/home/user/repo/app_bin" in content, "The post-commit hook does not reference the expected binary path /home/user/repo/app_bin."

def test_git_commit_exists():
    try:
        output = subprocess.check_output(
            ["git", "log", "--oneline"], 
            cwd="/home/user/repo", 
            stderr=subprocess.STDOUT, 
            text=True
        )
        assert "Fix paths and harden deployment" in output, "The required commit 'Fix paths and harden deployment' was not found in the git log."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run git log: {e.output}")

def test_main_cpp_modified():
    main_cpp_path = "/home/user/repo/main.cpp"
    assert os.path.isfile(main_cpp_path), f"File {main_cpp_path} does not exist."

    with open(main_cpp_path, "r") as f:
        content = f.read()
        assert "/home/user/deployment_output.log" in content, "main.cpp does not contain the expected absolute path '/home/user/deployment_output.log'."

def test_ssh_port_forwarding():
    # Check if port 8080 is listening
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 8080))
    sock.close()
    assert result == 0, "Port 8080 is not listening. The SSH tunnel may not be set up correctly."

    # Verify ssh process with port forwarding
    try:
        output = subprocess.check_output(["ps", "aux"], text=True)
        ssh_forwarding_found = any(
            "ssh" in line and "-L" in line and "8080" in line and "9090" in line 
            for line in output.splitlines()
        )
        assert ssh_forwarding_found, "Could not find an ssh process running with local port forwarding for 8080 to 9090."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to run ps aux to check for ssh port forwarding.")