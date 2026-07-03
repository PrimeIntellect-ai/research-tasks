# test_final_state.py

import os
import subprocess
import pytest

def test_auto_answer_script_exists():
    path = "/home/user/bin/auto_answer.py"
    assert os.path.isfile(path), f"The script {path} does not exist."

def test_post_receive_hook_exists_and_executable():
    path = "/home/user/config_repo.git/hooks/post-receive"
    assert os.path.isfile(path), f"The hook {path} does not exist."
    assert os.access(path, os.X_OK), f"The hook {path} is not executable."

def test_deployment_success_flag():
    path = "/home/user/deployed_services/deploy_success.flag"
    assert os.path.isfile(path), f"The deployment success flag {path} does not exist. The deployment script may not have run correctly or the target directory was incorrect."

def test_hook_metrics_log():
    path = "/home/user/hook_metrics.log"
    assert os.path.isfile(path), f"The metrics log {path} does not exist."

    with open(path, 'r') as f:
        content = f.read().splitlines()

    assert "inventory" in content, f"The metrics log {path} does not contain 'inventory'. Found: {content}"

def test_inventory_yml_in_repo():
    repo_path = "/home/user/config_repo.git"
    result = subprocess.run(
        ["git", "ls-tree", "-r", "HEAD"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to run git ls-tree in the bare repository."
    assert "inventory.yml" in result.stdout, "inventory.yml was not found in the HEAD of the bare repository."