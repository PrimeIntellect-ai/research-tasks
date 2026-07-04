# test_final_state.py

import os
import subprocess
import re
import shutil

def test_git_repo_and_hook():
    repo_path = "/home/user/accounts.git"
    assert os.path.isdir(repo_path), f"Bare repo {repo_path} does not exist"

    hook_path = os.path.join(repo_path, "hooks", "post-receive")
    assert os.path.isfile(hook_path), f"post-receive hook missing at {hook_path}"
    assert os.access(hook_path, os.X_OK), "post-receive hook is not executable"

def test_rust_project_exists():
    cargo_toml = "/home/user/src/network_provisioner/Cargo.toml"
    assert os.path.isfile(cargo_toml), "Rust project Cargo.toml missing"

def test_logrotate_config():
    conf_path = "/home/user/logrotate.conf"
    assert os.path.isfile(conf_path), "logrotate.conf missing"
    with open(conf_path, 'r') as f:
        content = f.read().lower()

    assert "daily" in content, "logrotate.conf missing 'daily'"
    assert "rotate 5" in content, "logrotate.conf missing 'rotate 5'"
    assert "compress" in content, "logrotate.conf missing 'compress'"
    assert "missingok" in content, "logrotate.conf missing 'missingok'"
    assert "create 0644" in content or "create 644" in content, "logrotate.conf missing 'create 0644'"
    assert "/home/user/logs/provision.log" in content, "logrotate.conf does not target the correct log file"

def test_provisioning_workflow():
    clone_dir = "/tmp/test_clone_accounts"
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)

    res = subprocess.run(["git", "clone", "/home/user/accounts.git", clone_dir], capture_output=True, text=True)
    assert res.returncode == 0, f"Failed to clone repository: {res.stderr}"

    users_json = '[{"username": "testuser1", "subnet": "192.168.100.0/24"}, {"username": "testuser2", "subnet": "192.168.101.0/24"}]'
    with open(os.path.join(clone_dir, "users.json"), "w") as f:
        f.write(users_json)

    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=clone_dir, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=clone_dir, check=True)
    subprocess.run(["git", "add", "users.json"], cwd=clone_dir, check=True)
    subprocess.run(["git", "commit", "-m", "Test provisioning"], cwd=clone_dir, check=True)

    # Push to trigger the hook
    res = subprocess.run(["git", "push", "origin", "master"], cwd=clone_dir, capture_output=True, text=True)
    assert res.returncode == 0, f"Git push failed (hook might have failed): {res.stderr}\n{res.stdout}"

    # Check routes.batch
    routes_path = "/home/user/network/routes.batch"
    assert os.path.isfile(routes_path), f"{routes_path} not found after push"
    with open(routes_path, "r") as f:
        routes = f.read()

    assert "route add 192.168.100.0/24 dev dummy0" in routes, "Missing or incorrect route for testuser1 in routes.batch"
    assert "route add 192.168.101.0/24 dev dummy0" in routes, "Missing or incorrect route for testuser2 in routes.batch"

    # Check provision.log
    log_path = "/home/user/logs/provision.log"
    assert os.path.isfile(log_path), f"{log_path} not found after push"
    with open(log_path, "r") as f:
        logs = f.read()

    pattern1 = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Provisioned user testuser1 with subnet 192.168.100.0/24$"
    pattern2 = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] Provisioned user testuser2 with subnet 192.168.101.0/24$"

    found1 = False
    found2 = False
    for line in logs.splitlines():
        if re.match(pattern1, line):
            found1 = True
        if re.match(pattern2, line):
            found2 = True

    assert found1, "Log entry for testuser1 not found or incorrectly formatted in provision.log"
    assert found2, "Log entry for testuser2 not found or incorrectly formatted in provision.log"