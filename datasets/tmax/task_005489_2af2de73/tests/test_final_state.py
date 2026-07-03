# test_final_state.py

import os
import json
import pytest

def test_deploy_out_status_log():
    """Test that status.log exists and contains DEPLOY_SUCCESS."""
    path = "/home/user/deploy_out/status.log"
    assert os.path.isfile(path), f"File {path} does not exist. The deployment hook may not have executed successfully."

    with open(path, "r") as f:
        content = f.read().strip()

    assert "DEPLOY_SUCCESS" in content, f"File {path} does not contain 'DEPLOY_SUCCESS'. Found: {content}"

def test_deploy_out_app_config():
    """Test that app_config.json exists in deploy_out and has the correct content."""
    path = "/home/user/deploy_out/app_config.json"
    assert os.path.isfile(path), f"File {path} does not exist. The files were not synced correctly."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    assert data.get("version") == "2.0", f"File {path} does not contain the expected version '2.0'."

def test_bare_repo_exists():
    """Test that the bare git repository exists."""
    path = "/home/user/microservices.git"
    assert os.path.isdir(path), f"Directory {path} does not exist."
    assert os.path.isfile(os.path.join(path, "config")), f"{path} does not appear to be a valid git repository."

def test_deploy_workspace_exists():
    """Test that the deploy workspace directory exists."""
    path = "/home/user/deploy_workspace"
    assert os.path.isdir(path), f"Directory {path} does not exist."

def test_local_clone_exists():
    """Test that the local clone exists."""
    path = "/home/user/local_clone"
    assert os.path.isdir(path), f"Directory {path} does not exist."
    assert os.path.isdir(os.path.join(path, ".git")), f"{path} is not a valid git repository clone."