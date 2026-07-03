# test_final_state.py

import os
import stat
import subprocess
import urllib.request
import ssl
import tempfile
import shutil

def test_git_repo_and_hook_exist():
    repo_dir = "/home/user/finops_repo.git"
    assert os.path.isdir(repo_dir), f"Bare git repo not found at {repo_dir}"
    assert os.path.isfile(os.path.join(repo_dir, "HEAD")), f"{repo_dir} does not appear to be a git repository"

    hook_path = os.path.join(repo_dir, "hooks", "pre-receive")
    assert os.path.isfile(hook_path), f"pre-receive hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"pre-receive hook at {hook_path} is not executable"

def test_web_server_files_and_pids():
    www_dir = "/home/user/www"
    assert os.path.isdir(www_dir), f"Directory {www_dir} not found"

    for f in ["cert.pem", "key.pem", "cost_report.html"]:
        file_path = os.path.join(www_dir, f)
        assert os.path.isfile(file_path), f"Required file {f} not found in {www_dir}"

    with open(os.path.join(www_dir, "cost_report.html"), "r") as f:
        content = f.read()
        assert "<ul>" in content, "cost_report.html must contain <ul>"

    assert os.path.isfile("/home/user/https.pid"), "https.pid not found"
    assert os.path.isfile("/home/user/socat.pid"), "socat.pid not found"

def test_processes_running():
    def is_pid_running(pid_file):
        try:
            with open(pid_file, "r") as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)
            return True
        except Exception:
            return False

    assert is_pid_running("/home/user/https.pid"), "HTTPS server process is not running"
    assert is_pid_running("/home/user/socat.pid"), "socat process is not running"

def test_git_hook_logic():
    repo_url = "/home/user/finops_repo.git"
    report_file = "/home/user/www/cost_report.html"

    temp_dir = tempfile.mkdtemp()
    try:
        # Clone repo
        subprocess.run(["git", "clone", repo_url, "test_repo"], cwd=temp_dir, check=True, capture_output=True)
        repo_dir = os.path.join(temp_dir, "test_repo")

        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_dir, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_dir, check=True)

        # Test 1: Valid push
        valid_file = os.path.join(repo_dir, "main.tf")
        with open(valid_file, "w") as f:
            f.write('instance_type = "t3.micro"\n')

        subprocess.run(["git", "add", "main.tf"], cwd=repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Valid commit"], cwd=repo_dir, check=True)

        # Get commit hash
        commit_hash = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_dir, check=True, capture_output=True, text=True).stdout.strip()

        push_res = subprocess.run(["git", "push", "origin", "master"], cwd=repo_dir, capture_output=True, text=True)
        assert push_res.returncode == 0, f"Valid push failed. Stderr: {push_res.stderr}"

        with open(report_file, "r") as f:
            report_content = f.read()
            expected_accepted = f'<li><span class="commit">{commit_hash}</span> - <span class="status">ACCEPTED</span></li>'
            assert expected_accepted in report_content, "ACCEPTED log entry not found in cost_report.html"

        # Test 2: Invalid push
        invalid_file = os.path.join(repo_dir, "bad.tf")
        with open(invalid_file, "w") as f:
            f.write('  instance_type = "p4d.24xlarge"\n')

        subprocess.run(["git", "add", "bad.tf"], cwd=repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", "Invalid commit"], cwd=repo_dir, check=True)

        invalid_commit_hash = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_dir, check=True, capture_output=True, text=True).stdout.strip()

        push_res = subprocess.run(["git", "push", "origin", "master"], cwd=repo_dir, capture_output=True, text=True)
        assert push_res.returncode != 0, "Invalid push should have been rejected."
        assert "Cost limit exceeded!" in push_res.stderr, "Error message 'Cost limit exceeded!' not found in stderr."

        with open(report_file, "r") as f:
            report_content = f.read()
            expected_rejected = f'<li><span class="commit">{invalid_commit_hash}</span> - <span class="status">REJECTED</span></li>'
            assert expected_rejected in report_content, "REJECTED log entry not found in cost_report.html"

    finally:
        shutil.rmtree(temp_dir)

def test_port_forwarding_and_https():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request("https://127.0.0.1:8080/cost_report.html")
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, "Failed to fetch cost_report.html via port 8080"
            content = response.read().decode('utf-8')
            assert "<ul>" in content, "cost_report.html fetched via HTTPS does not contain expected content"
    except Exception as e:
        assert False, f"Failed to connect to HTTPS server via socat on port 8080: {e}"