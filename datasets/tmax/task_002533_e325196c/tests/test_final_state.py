# test_final_state.py

import os
import re
import stat
import subprocess
import socket
import time
import pytest

def test_profile_file():
    profile_path = "/home/user/.microservice_profile"
    assert os.path.isfile(profile_path), f"Profile file missing at {profile_path}"
    with open(profile_path, "r") as f:
        content = f.read()
    assert "export DEPLOY_ENV=staging" in content, "DEPLOY_ENV export missing or incorrect"
    assert "export TARGET_PORT=8080" in content, "TARGET_PORT export missing or incorrect"
    assert "export LOG_DIR=/home/user/logs" in content, "LOG_DIR export missing or incorrect"

def test_deployer_binary():
    bin_path = "/home/user/bin/deployer"
    assert os.path.isfile(bin_path), f"Deployer binary missing at {bin_path}"
    assert os.access(bin_path, os.X_OK), "Deployer binary is not executable"

def test_git_repo_and_hook():
    repo_path = "/home/user/microservice.git"
    assert os.path.isdir(repo_path), f"Git repo directory missing at {repo_path}"
    assert os.path.isfile(os.path.join(repo_path, "config")), "Not a valid git repository"

    # Check if bare
    with open(os.path.join(repo_path, "config"), "r") as f:
        assert "bare = true" in f.read().lower(), "Git repository is not bare"

    hook_path = os.path.join(repo_path, "hooks/post-receive")
    assert os.path.isfile(hook_path), f"post-receive hook missing at {hook_path}"
    assert os.access(hook_path, os.X_OK), "post-receive hook is not executable"

    with open(hook_path, "r") as f:
        content = f.read()
    assert ".microservice_profile" in content, "Hook does not source the profile"
    assert "/home/user/bin/deployer" in content, "Hook does not execute the deployer"

def test_logrotate_conf():
    conf_path = "/home/user/logrotate.conf"
    assert os.path.isfile(conf_path), f"logrotate.conf missing at {conf_path}"
    with open(conf_path, "r") as f:
        content = f.read()
    assert "/home/user/logs/deploy.log" in content, "logrotate.conf does not target deploy.log"
    assert "daily" in content, "logrotate.conf missing 'daily' directive"
    assert "rotate 3" in content, "logrotate.conf missing 'rotate 3' directive"
    assert "compress" in content, "logrotate.conf missing 'compress' directive"
    assert "missingok" in content, "logrotate.conf missing 'missingok' directive"

def test_deploy_log_success():
    log_path = "/home/user/logs/deploy.log"
    assert os.path.isfile(log_path), f"Deploy log missing at {log_path}. Did you push a dummy commit?"
    with open(log_path, "r") as f:
        content = f.read()

    # regex for RFC3339 timestamp and success message
    pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2}) DEPLOYMENT SUCCESSFUL: Env=staging, Port=8080$"
    match = re.search(pattern, content, re.MULTILINE)
    assert match is not None, "Deploy log does not contain the correctly formatted success message"

def test_deploy_failure_and_logrotate():
    # Kill the mock service on 9090
    subprocess.run(["fuser", "-k", "9090/tcp"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1) # wait for it to die

    # Run the deployer directly with the profile
    subprocess.run(
        "source /home/user/.microservice_profile && /home/user/bin/deployer",
        shell=True,
        executable="/bin/bash",
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    log_path = "/home/user/logs/deploy.log"
    assert os.path.isfile(log_path), "Deploy log missing after failure test"
    with open(log_path, "r") as f:
        content = f.read()

    assert "DEPLOYMENT FAILED: Dependency unreachable" in content, "Deploy log does not contain the failure message after 9090 is killed"

    # Run logrotate
    subprocess.run(
        ["logrotate", "-s", "/home/user/logrotate.status", "/home/user/logrotate.conf", "--force"],
        check=True
    )

    rotated_log = "/home/user/logs/deploy.log.1.gz"
    assert os.path.isfile(rotated_log), f"Rotated log file missing at {rotated_log}"