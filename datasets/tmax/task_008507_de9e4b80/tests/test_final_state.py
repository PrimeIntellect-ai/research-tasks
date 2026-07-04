# test_final_state.py

import os
import subprocess
import tempfile
import json
import urllib.request
import ssl
import time

def test_git_repo_bare():
    """Check if /home/user/obs-gitops.git is a bare git repository."""
    repo_path = "/home/user/obs-gitops.git"
    assert os.path.isdir(repo_path), f"{repo_path} does not exist or is not a directory."

    res = subprocess.run(
        ["git", "rev-parse", "--is-bare-repository"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    assert res.returncode == 0, "Failed to run git rev-parse."
    assert res.stdout.strip() == "true", f"{repo_path} is not a bare git repository."

def test_hook_exists_and_executable():
    """Check if the post-receive hook exists and is executable."""
    hook_path = "/home/user/obs-gitops.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Hook script {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Hook script {hook_path} is not executable."

def test_git_push_and_hook():
    """Simulate a push to the bare git repository and verify the hook functionality."""
    repo_path = "/home/user/obs-gitops.git"

    with tempfile.TemporaryDirectory() as tmpdir:
        # Clone the repository
        res = subprocess.run(["git", "clone", repo_path, tmpdir], capture_output=True, text=True)
        assert res.returncode == 0, f"Failed to clone repo: {res.stderr}"

        # Create test files
        with open(os.path.join(tmpdir, "valid.json"), "w") as f:
            f.write('{"dashboard_id": "123", "name": "CPU"}')
        with open(os.path.join(tmpdir, "invalid.json"), "w") as f:
            f.write('{"name": "Memory"}')
        with open(os.path.join(tmpdir, "broken.json"), "w") as f:
            f.write('{not json}')

        # Configure git and commit
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmpdir, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmpdir, check=True)
        subprocess.run(["git", "add", "."], cwd=tmpdir, check=True)
        subprocess.run(["git", "commit", "-m", "test commit"], cwd=tmpdir, check=True)

        # Push to main branch
        res = subprocess.run(["git", "push", "origin", "main"], cwd=tmpdir, capture_output=True, text=True)
        assert res.returncode == 0, f"Git push failed: {res.stderr}"

    # Verify the hook processed the files correctly
    dashboards_dir = "/home/user/public_html/dashboards/"
    assert os.path.isdir(dashboards_dir), f"Directory {dashboards_dir} was not created."

    valid_path = os.path.join(dashboards_dir, "valid.json")
    invalid_path = os.path.join(dashboards_dir, "invalid.json")
    broken_path = os.path.join(dashboards_dir, "broken.json")

    assert os.path.isfile(valid_path), "valid.json was not copied to the dashboards directory."
    assert not os.path.isfile(invalid_path), "invalid.json should not have been copied."
    assert not os.path.isfile(broken_path), "broken.json should not have been copied."

def test_certs_exist():
    """Check if the SSL certificates exist."""
    cert_path = "/home/user/certs/cert.pem"
    key_path = "/home/user/certs/key.pem"
    assert os.path.isfile(cert_path), f"Certificate {cert_path} does not exist."
    assert os.path.isfile(key_path), f"Private key {key_path} does not exist."

def test_webserver_running():
    """Check if the web server is running on port 8443 with TLS."""
    pid_file = "/home/user/webserver.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist."

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.urlopen("https://localhost:8443/", context=ctx, timeout=5)
        assert req.getcode() == 200, "Web server did not return 200 OK."
    except Exception as e:
        assert False, f"Failed to connect to web server: {e}"

def test_health_check_script():
    """Run the health check script and verify its output."""
    script_path = "/home/user/health_check.py"
    assert os.path.isfile(script_path), f"Health check script {script_path} does not exist."

    # Run the script
    res = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert res.returncode == 0, f"Health check script failed: {res.stderr}"

    health_file = "/home/user/public_html/health.json"
    assert os.path.isfile(health_file), f"Health file {health_file} was not created."

    with open(health_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{health_file} does not contain valid JSON."

    assert data.get("status") == "up", "Health check status is not 'up'."
    assert isinstance(data.get("dashboard_count"), int), "dashboard_count is missing or not an integer."
    assert data.get("dashboard_count") >= 1, "dashboard_count should be at least 1 after the git push test."

def test_cron_job():
    """Check if the cron job is configured for the user."""
    res = subprocess.run(["crontab", "-l", "-u", "user"], capture_output=True, text=True)

    # It's possible crontab returns 1 if no crontab for user, but we expect one.
    assert res.returncode == 0, "Failed to read crontab for user 'user'."

    cron_content = res.stdout.strip()
    assert "* * * * *" in cron_content, "Cron job does not have the correct schedule (* * * * *)."
    assert "/home/user/health_check.py" in cron_content, "Cron job does not execute /home/user/health_check.py."