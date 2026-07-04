# test_final_state.py

import os
import subprocess
import tempfile
import pytest
import requests
import time

def test_routing_to_metrics_server():
    # Verify that 10.0.0.5 is reachable (the student should have added the route/IP)
    try:
        response = requests.get("http://10.0.0.5:8080/", timeout=2)
        # Even if it's a 404, the server is reachable
    except requests.RequestException as e:
        pytest.fail(f"Metrics server at 10.0.0.5:8080 is not reachable. Routing or interface issue: {e}")

def test_sshd_configuration():
    # Verify the SSH daemon configuration for public key auth
    with open("/home/user/sshd_config", "r") as f:
        config = f.read()

    assert "PubkeyAuthentication yes" in config, "PubkeyAuthentication is not enabled in sshd_config"
    assert "AuthorizedKeysFile" in config, "AuthorizedKeysFile is not specified in sshd_config"

def test_git_hook_exists_and_executable():
    hook_path = "/home/user/git-server/repo.git/hooks/post-receive"
    assert os.path.isfile(hook_path), "post-receive hook does not exist"
    assert os.access(hook_path, os.X_OK), "post-receive hook is not executable"

    with open(hook_path, "r") as f:
        hook_content = f.read()

    assert "curl" in hook_content, "post-receive hook does not contain a curl command"
    assert "$METRICS_URL" in hook_content or "${METRICS_URL}" in hook_content, "post-receive hook does not use the METRICS_URL environment variable"

def test_git_push_triggers_hook():
    # Test the end-to-end flow
    with tempfile.TemporaryDirectory() as tmpdir:
        env = os.environ.copy()
        env["GIT_SSH_COMMAND"] = "ssh -i /home/user/.ssh/id_rsa -p 2222 -o StrictHostKeyChecking=no"

        # Clone
        clone_cmd = ["git", "clone", "user@127.0.0.1:/home/user/git-server/repo.git", tmpdir]
        try:
            subprocess.run(clone_cmd, env=env, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Failed to clone repository via SSH: {e.stderr}")

        # Commit
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmpdir, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmpdir, check=True)
        subprocess.run(["git", "commit", "--allow-empty", "-m", "Test commit"], cwd=tmpdir, check=True)

        # Push
        try:
            push_result = subprocess.run(["git", "push", "origin", "master"], cwd=tmpdir, env=env, check=True, capture_output=True, text=True)
            output = push_result.stderr + push_result.stdout
            # If curl fails, it usually outputs to stderr which is relayed back
            assert "Failed to connect" not in output, f"Curl failed to connect during git push: {output}"
            assert "Could not resolve host" not in output, f"Curl could not resolve host during git push: {output}"
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Failed to push to repository: {e.stderr}")