# test_final_state.py

import os
import subprocess
import time
import tempfile
import requests
import shutil

GIT_PORT = 9418
HTTP_PORT = 8080
TUNNEL_PORT = 8081

def test_logrotate_config():
    config_path = "/home/user/logrotate.conf"
    assert os.path.exists(config_path), "logrotate.conf is missing"
    with open(config_path, "r") as f:
        content = f.read()
    assert "/home/user/http.log" in content, "logrotate config missing target file"
    assert "daily" in content, "logrotate config missing 'daily'"
    assert "rotate 3" in content, "logrotate config missing 'rotate 3'"
    assert "compress" in content, "logrotate config missing 'compress'"

def test_ssh_config():
    ssh_config_path = "/home/user/.ssh/config"
    if not os.path.exists(ssh_config_path):
        # Could be root depending on user
        ssh_config_path = os.path.expanduser("~/.ssh/config")
    assert os.path.exists(ssh_config_path), "SSH config is missing"
    with open(ssh_config_path, "r") as f:
        content = f.read()
    assert "k8s-cluster.local" in content, "SSH config missing Host k8s-cluster.local"
    assert "PubkeyAuthentication no" in content or "PasswordAuthentication yes" in content or "IdentitiesOnly" in content, "SSH config missing key rejection for k8s-cluster.local"

def test_supervisor_script():
    script_path = "/home/user/supervisor.sh"
    assert os.path.exists(script_path), "supervisor.sh is missing"
    assert os.access(script_path, os.X_OK), "supervisor.sh is not executable"

def test_git_hook():
    hook_path = "/home/user/manifests.git/hooks/post-receive"
    assert os.path.exists(hook_path), "post-receive hook is missing"
    assert os.access(hook_path, os.X_OK), "post-receive hook is not executable"

def test_pipeline_and_ports():
    # Test Git push
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run(["git", "init"], cwd=tmpdir, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmpdir, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmpdir, check=True)

        test_file = os.path.join(tmpdir, "deployment.yaml")
        test_content = "apiVersion: apps/v1\nkind: Deployment\n"
        with open(test_file, "w") as f:
            f.write(test_content)

        subprocess.run(["git", "add", "deployment.yaml"], cwd=tmpdir, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=tmpdir, check=True)

        # Add remote and push
        subprocess.run(["git", "remote", "add", "origin", f"git://localhost:{GIT_PORT}/"], cwd=tmpdir, check=True)

        push_res = subprocess.run(["git", "push", "origin", "master:main"], cwd=tmpdir, capture_output=True)
        if push_res.returncode != 0:
            push_res = subprocess.run(["git", "push", "origin", "main:main"], cwd=tmpdir, capture_output=True)

        assert push_res.returncode == 0, f"Git push failed: {push_res.stderr.decode()}"

    # Wait a moment for hook to process
    time.sleep(1)

    # Test HTTP server
    try:
        resp = requests.get(f"http://localhost:{HTTP_PORT}/deployment.yaml", timeout=2)
        assert resp.status_code == 200, f"HTTP server returned {resp.status_code}"
        assert test_content in resp.text, "HTTP server returned incorrect content"
    except requests.RequestException as e:
        assert False, f"HTTP server check failed: {e}"

    # Test SSH Tunnel
    try:
        resp = requests.get(f"http://localhost:{TUNNEL_PORT}/deployment.yaml", timeout=2)
        assert resp.status_code == 200, f"Tunnel HTTP server returned {resp.status_code}"
        assert test_content in resp.text, "Tunnel HTTP server returned incorrect content"
    except requests.RequestException as e:
        assert False, f"Tunnel HTTP server check failed: {e}"