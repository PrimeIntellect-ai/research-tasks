# test_final_state.py

import os
import json
import tempfile
import subprocess
import shutil
import pytest

REPO_PATH = "/home/user/deploy_repo.git"
HOOK_PATH = os.path.join(REPO_PATH, "hooks", "pre-receive")
LOG_PATH = "/home/user/monitoring_log.json"

def run_cmd(cmd, cwd=None, env=None):
    return subprocess.run(cmd, cwd=cwd, env=env, shell=True, capture_output=True, text=True)

def test_repo_and_hook_exist():
    assert os.path.isdir(REPO_PATH), f"Bare repository directory not found at {REPO_PATH}"

    # Check if it's a bare git repo
    res = run_cmd("git rev-parse --is-bare-repository", cwd=REPO_PATH)
    assert res.returncode == 0 and "true" in res.stdout, f"{REPO_PATH} is not a bare Git repository"

    assert os.path.isfile(HOOK_PATH), f"pre-receive hook not found at {HOOK_PATH}"
    assert os.access(HOOK_PATH, os.X_OK), f"pre-receive hook at {HOOK_PATH} is not executable"

def test_successful_push():
    # Clear log file if it exists
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Setup local repo
        run_cmd("git init", cwd=tmpdir)
        run_cmd("git config user.email 'test@example.com'", cwd=tmpdir)
        run_cmd("git config user.name 'Test User'", cwd=tmpdir)

        # Create deploy_targets.txt with healthy services
        targets_path = os.path.join(tmpdir, "deploy_targets.txt")
        with open(targets_path, "w") as f:
            f.write("web-frontend\ndb-primary\n")

        run_cmd("git add deploy_targets.txt", cwd=tmpdir)
        run_cmd("git commit -m 'Add healthy targets'", cwd=tmpdir)

        # Push to the bare repo
        run_cmd(f"git remote add origin {REPO_PATH}", cwd=tmpdir)
        res = run_cmd("git push origin master", cwd=tmpdir)

        assert res.returncode == 0, f"Expected push to succeed, but it failed. Stderr: {res.stderr}"
        assert "[OK] All services healthy." in res.stdout or "[OK] All services healthy." in res.stderr, "Success message not found in output"

        # Check log file
        assert os.path.isfile(LOG_PATH), f"Log file {LOG_PATH} not created"
        with open(LOG_PATH, "r") as f:
            lines = f.read().strip().split('\n')
            last_line = lines[-1]
            try:
                log_entry = json.loads(last_line)
            except json.JSONDecodeError:
                pytest.fail(f"Last line of log file is not valid JSON: {last_line}")

            assert log_entry.get("status") == "accepted", f"Expected status 'accepted', got {log_entry.get('status')}"
            assert log_entry.get("failed_services") == [], "Expected empty failed_services list"
            assert "refs/heads/master" in log_entry.get("ref", ""), "Ref does not match expected master branch ref"

def test_rejected_push():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Setup local repo
        run_cmd("git init", cwd=tmpdir)
        run_cmd("git config user.email 'test@example.com'", cwd=tmpdir)
        run_cmd("git config user.name 'Test User'", cwd=tmpdir)

        # Create deploy_targets.txt with failing services
        targets_path = os.path.join(tmpdir, "deploy_targets.txt")
        with open(targets_path, "w") as f:
            f.write("auth-service\npayment-gateway\nmissing-service\n")

        run_cmd("git add deploy_targets.txt", cwd=tmpdir)
        run_cmd("git commit -m 'Add failing targets'", cwd=tmpdir)

        # Push to the bare repo
        run_cmd(f"git remote add origin {REPO_PATH}", cwd=tmpdir)
        res = run_cmd("git push origin master", cwd=tmpdir)

        assert res.returncode != 0, "Expected push to fail, but it succeeded."
        assert "[ALERT] Service payment-gateway is down or unknown!" in res.stderr, "Alert for payment-gateway missing in stderr"
        assert "[ALERT] Service missing-service is down or unknown!" in res.stderr, "Alert for missing-service missing in stderr"

        # Check log file
        assert os.path.isfile(LOG_PATH), f"Log file {LOG_PATH} not found"
        with open(LOG_PATH, "r") as f:
            lines = f.read().strip().split('\n')
            last_line = lines[-1]
            try:
                log_entry = json.loads(last_line)
            except json.JSONDecodeError:
                pytest.fail(f"Last line of log file is not valid JSON: {last_line}")

            assert log_entry.get("status") == "rejected", f"Expected status 'rejected', got {log_entry.get('status')}"
            failed_services = log_entry.get("failed_services", [])
            assert "payment-gateway" in failed_services, "payment-gateway missing from failed_services"
            assert "missing-service" in failed_services, "missing-service missing from failed_services"
            assert "refs/heads/master" in log_entry.get("ref", ""), "Ref does not match expected master branch ref"