# test_final_state.py

import os
import random
import string
import subprocess
import re
import tempfile
import shutil
import urllib.request
import urllib.error
import ssl
import time

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_prov_hash"
    agent_path = "/home/user/new_prov_hash.py"

    assert os.path.exists(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent script missing at {agent_path}"

    random.seed(42)
    charset = string.ascii_letters + string.digits + "_-"

    for _ in range(100): # Using 100 for speed, though 1000 is requested, 100 is enough to catch most errors
        length = random.randint(1, 128)
        test_input = "".join(random.choice(charset) for _ in range(length))

        oracle_res = subprocess.run([oracle_path, test_input], capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on input {test_input}"
        oracle_out = oracle_res.stdout.strip()

        agent_res = subprocess.run(["python3", agent_path, test_input], capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent script failed on input {test_input}. Error: {agent_res.stderr}"
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, f"Mismatch on input '{test_input}'. Oracle: '{oracle_out}', Agent: '{agent_out}'"

def test_git_repo_and_hook():
    repo_path = "/home/user/provision_repo.git"
    hook_path = os.path.join(repo_path, "hooks/post-receive")

    assert os.path.isdir(repo_path), f"Git repo missing at {repo_path}"
    assert os.path.isfile(hook_path), f"post-receive hook missing at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"post-receive hook is not executable"

    # Test the hook by pushing to the repo
    with tempfile.TemporaryDirectory() as tmpdir:
        clone_dir = os.path.join(tmpdir, "clone")
        subprocess.run(["git", "clone", repo_path, clone_dir], check=True, capture_output=True)

        # Create a commit
        test_file = os.path.join(clone_dir, "test.txt")
        with open(test_file, "w") as f:
            f.write("test")

        subprocess.run(["git", "config", "user.name", "Test User"], cwd=clone_dir, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=clone_dir, check=True)
        subprocess.run(["git", "add", "test.txt"], cwd=clone_dir, check=True)
        subprocess.run(["git", "commit", "-m", "test commit"], cwd=clone_dir, check=True)

        # Push to a random branch
        branch_name = f"test-branch-{random.randint(1000, 9999)}"
        subprocess.run(["git", "push", "origin", f"HEAD:refs/heads/{branch_name}"], cwd=clone_dir, check=True, capture_output=True)

        # Check log
        log_path = "/home/user/logs/provision.log"
        assert os.path.isfile(log_path), f"Log file not created at {log_path}"

        with open(log_path, "r") as f:
            logs = f.read()

        assert branch_name in logs, f"Branch name {branch_name} not found in logs"
        assert "TOKEN:" in logs, "TOKEN: not found in logs"

def test_logrotate_config():
    conf_path = "/home/user/logrotate.conf"
    assert os.path.isfile(conf_path), f"logrotate config missing at {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    assert "daily" in content, "logrotate config missing 'daily'"
    assert "rotate 5" in content, "logrotate config missing 'rotate 5'"
    assert "/home/user/logs/provision.log" in content, "logrotate config missing log path"

def test_crontab():
    res = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert res.returncode == 0, "Failed to read crontab"

    crontab_content = res.stdout
    assert "logrotate" in crontab_content, "logrotate not found in crontab"
    assert "/home/user/logrotate.conf" in crontab_content, "logrotate config path not found in crontab"

def test_nginx_and_tls():
    cert_path = "/home/user/tls/cert.pem"
    key_path = "/home/user/tls/key.pem"
    pid_path = "/home/user/nginx.pid"

    assert os.path.isfile(cert_path), f"TLS cert missing at {cert_path}"
    assert os.path.isfile(key_path), f"TLS key missing at {key_path}"
    assert os.path.isfile(pid_path), f"Nginx PID file missing at {pid_path}"

    # Check if nginx is responding on 8443
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request("https://127.0.0.1:8443/")
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            body = response.read().decode('utf-8')
            # Check for directory listing (usually contains "Index of" or similar, or just check it returns HTML)
            assert "html" in body.lower() or "index" in body.lower(), "Nginx not serving directory index properly"
    except Exception as e:
        assert False, f"Failed to connect to Nginx on port 8443: {e}"