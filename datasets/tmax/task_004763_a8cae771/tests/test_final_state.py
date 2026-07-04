# test_final_state.py

import os
import subprocess
import tempfile
import time
import urllib.request
import ssl
import json

def test_server_running():
    pid_file = "/home/user/server.pid"
    assert os.path.exists(pid_file), "PID file /home/user/server.pid does not exist."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), "PID file does not contain a valid numeric PID."
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        assert False, f"Process with PID {pid} is not running."

def test_git_repo_and_deployment():
    repo_path = "/home/user/dashboards.git"
    assert os.path.isdir(repo_path), f"Bare git repository {repo_path} does not exist."

    # Check if it's a bare repo
    result = subprocess.run(["git", "-C", repo_path, "rev-parse", "--is-bare-repository"], capture_output=True, text=True)
    assert result.stdout.strip() == "true", f"Repository {repo_path} is not a bare repository."

    with tempfile.TemporaryDirectory() as tmpdir:
        # Clone the repo
        clone_cmd = ["git", "clone", repo_path, tmpdir]
        subprocess.run(clone_cmd, check=True, capture_output=True)

        # Create a test file
        test_file_path = os.path.join(tmpdir, "test_dash.json")
        test_content = {"status": "ok"}
        with open(test_file_path, "w") as f:
            json.dump(test_content, f)

        # Commit and push
        subprocess.run(["git", "-C", tmpdir, "add", "test_dash.json"], check=True, capture_output=True)
        # Set git config for commit
        subprocess.run(["git", "-C", tmpdir, "config", "user.email", "test@example.com"], check=True, capture_output=True)
        subprocess.run(["git", "-C", tmpdir, "config", "user.name", "Test User"], check=True, capture_output=True)
        subprocess.run(["git", "-C", tmpdir, "commit", "-m", "Test dashboard"], check=True, capture_output=True)

        # Push to master
        push_result = subprocess.run(["git", "-C", tmpdir, "push", "origin", "master"], capture_output=True, text=True)
        assert push_result.returncode == 0, f"Failed to push to bare repository: {push_result.stderr}"

        # Wait a moment for the post-receive hook to process
        time.sleep(2)

        # Verify via HTTPS
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        url = "https://localhost:8443/dashboards/test_dash.json"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
                body = response.read().decode('utf-8')
                data = json.loads(body)
                assert data.get("status") == "ok", f"Expected {{'status': 'ok'}}, got {data}"
        except Exception as e:
            assert False, f"Failed to retrieve the pushed dashboard via HTTPS at {url}: {e}"