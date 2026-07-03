# test_final_state.py

import os
import subprocess
import socket
import time
import shutil
import pytest

def test_auto_approve_script():
    exp_path = "/home/user/auto-approve.exp"
    assert os.path.isfile(exp_path), f"Expect script {exp_path} is missing."
    assert os.access(exp_path, os.X_OK), f"Expect script {exp_path} is not executable."

    # Run the expect script and check exit code
    result = subprocess.run([exp_path], capture_output=True)
    assert result.returncode == 0, f"Expect script failed to run successfully. Output: {result.stderr.decode()} {result.stdout.decode()}"

def test_port_forwarding():
    # Check if port 10025 is listening
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex(('127.0.0.1', 10025))
    sock.close()
    assert result == 0, "Port 10025 is not open or forwarded. The socat port forwarding might not be running."

def test_git_hook_exists():
    hook_path = "/home/user/manifests.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Git hook {hook_path} is missing."
    assert os.access(hook_path, os.X_OK), f"Git hook {hook_path} is not executable."

def test_end_to_end_git_push():
    # Setup a temporary repo to push from
    temp_repo = "/tmp/test-repo"
    if os.path.exists(temp_repo):
        shutil.rmtree(temp_repo)

    os.makedirs(temp_repo)

    # Initialize and push
    subprocess.run(["git", "init"], cwd=temp_repo, check=True, capture_output=True)
    subprocess.run(["git", "remote", "add", "origin", "/home/user/manifests.git"], cwd=temp_repo, check=True, capture_output=True)

    # Create a dummy file
    with open(os.path.join(temp_repo, "deployment.yaml"), "w") as f:
        f.write("apiVersion: v1\n")

    subprocess.run(["git", "add", "deployment.yaml"], cwd=temp_repo, check=True, capture_output=True)

    # Configure git user if not set
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_repo, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_repo, capture_output=True)

    subprocess.run(["git", "commit", "-m", "Test deployment"], cwd=temp_repo, check=True, capture_output=True)

    # Clean up previous log if it exists
    log_path = "/home/user/deploy-stage/applied.log"
    if os.path.exists(log_path):
        os.remove(log_path)

    # Push to trigger the hook
    push_result = subprocess.run(["git", "push", "origin", "master"], cwd=temp_repo, capture_output=True)
    assert push_result.returncode == 0, f"Git push failed. Output: {push_result.stderr.decode()}"

    # Wait for background processes to settle
    time.sleep(5)

    # Check the applied.log
    assert os.path.isfile(log_path), f"Log file {log_path} was not created. The hook may have failed or not run."

    with open(log_path, "r") as f:
        content = f.read()

    expected_msg = "Successfully applied manifests from /home/user/deploy-stage/"
    assert expected_msg in content, f"Expected success message not found in {log_path}. Content: {content}"