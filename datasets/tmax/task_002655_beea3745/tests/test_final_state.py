# test_final_state.py

import os
import subprocess
import tempfile
import json
import stat
import pytest

HOOK_PATH = "/home/user/infra.git/hooks/pre-receive"
BARE_REPO = "/home/user/infra.git"
LOG_PATH = "/home/user/finops_alerts.log"

def test_hook_exists_and_executable():
    assert os.path.isfile(HOOK_PATH), f"Hook file {HOOK_PATH} does not exist."
    st = os.stat(HOOK_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Hook file {HOOK_PATH} is not executable."

def test_push_valid_config():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Clone the repo
        subprocess.run(["git", "clone", BARE_REPO, tmpdir], check=True, capture_output=True)

        # Create a valid config
        valid_json_path = os.path.join(tmpdir, "valid_vm.json")
        with open(valid_json_path, "w") as f:
            json.dump({
                "vm_name": "web-01",
                "image_path": "/home/user/storage/small.qcow2"
            }, f)

        # Commit and push
        subprocess.run(["git", "add", "valid_vm.json"], cwd=tmpdir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Add valid VM"], cwd=tmpdir, check=True, capture_output=True)

        result = subprocess.run(["git", "push", "origin", "master"], cwd=tmpdir, capture_output=True, text=True)

        assert result.returncode == 0, f"Pushing a valid config failed. stderr: {result.stderr}"

def test_push_invalid_config_and_logging():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Clone the repo
        subprocess.run(["git", "clone", BARE_REPO, tmpdir], check=True, capture_output=True)

        # Create an invalid config
        invalid_json_path = os.path.join(tmpdir, "invalid_vm.json")
        with open(invalid_json_path, "w") as f:
            json.dump({
                "vm_name": "db-01",
                "image_path": "/home/user/storage/large.qcow2"
            }, f)

        # Commit
        subprocess.run(["git", "add", "invalid_vm.json"], cwd=tmpdir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Add invalid VM"], cwd=tmpdir, check=True, capture_output=True)

        # Get commit hash
        commit_hash_proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmpdir, check=True, capture_output=True, text=True)
        commit_hash = commit_hash_proc.stdout.strip()

        # Push
        result = subprocess.run(["git", "push", "origin", "master"], cwd=tmpdir, capture_output=True, text=True)

        assert result.returncode != 0, "Pushing an invalid config was allowed but should have been rejected."
        assert "FinOps Policy Violation: Image /home/user/storage/large.qcow2 is too large." in result.stderr or "FinOps Policy Violation: Image /home/user/storage/large.qcow2 is too large." in result.stdout, "The expected rejection message was not printed to stdout/stderr."

        # Check log file
        assert os.path.isfile(LOG_PATH), f"Log file {LOG_PATH} does not exist."
        with open(LOG_PATH, "r") as f:
            log_contents = f.read()

        expected_log = f"[REJECTED] {commit_hash} attempted to provision /home/user/storage/large.qcow2"
        assert expected_log in log_contents, f"Expected log entry '{expected_log}' not found in {LOG_PATH}."