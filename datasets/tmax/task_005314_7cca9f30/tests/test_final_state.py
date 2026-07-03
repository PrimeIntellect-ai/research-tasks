# test_final_state.py
import os
import json
import re
import subprocess

def test_bare_repo_exists():
    repo_path = "/home/user/deploy.git"
    assert os.path.isdir(repo_path), f"Bare repository directory {repo_path} does not exist."
    result = subprocess.run(
        ["git", "rev-parse", "--is-bare-repository"],
        cwd=repo_path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0 and result.stdout.strip() == "true", "The directory /home/user/deploy.git is not a valid bare Git repository."

def test_hook_exists_and_executable():
    hook_path = "/home/user/deploy.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Hook file {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Hook file {hook_path} is not executable."

    with open(hook_path, "r") as f:
        first_line = f.readline().strip()
    assert "python" in first_line, f"Hook file {hook_path} does not appear to be a Python script (shebang: {first_line})."

def test_ports_conf_exists():
    conf_path = "/home/user/ports.conf"
    assert os.path.isfile(conf_path), f"{conf_path} does not exist."
    with open(conf_path, "r") as f:
        content = f.read().strip()
    assert content == "9001,9002,9003", f"{conf_path} content is incorrect. Expected '9001,9002,9003'."

def test_workspace_and_push():
    workspace_path = "/home/user/workspace"
    assert os.path.isdir(workspace_path), f"Workspace directory {workspace_path} does not exist."

    app_path = os.path.join(workspace_path, "app.py")
    assert os.path.isfile(app_path), f"{app_path} does not exist."

    # Check if app.py is committed and pushed to bare repo
    bare_repo_path = "/home/user/deploy.git"
    result = subprocess.run(
        ["git", "ls-tree", "-r", "HEAD", "--name-only"],
        cwd=bare_repo_path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to list files in bare repository."
    assert "app.py" in result.stdout.splitlines(), "app.py was not pushed to the bare repository."

def test_proxy_json_content():
    json_path = "/home/user/proxy.json"
    assert os.path.isfile(json_path), f"{json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} does not contain valid JSON."

    expected_data = {
        "mode": "round-robin",
        "backend_servers": [
            "http://127.0.0.1:9001",
            "http://127.0.0.1:9002",
            "http://127.0.0.1:9003"
        ]
    }
    assert data == expected_data, f"{json_path} content does not match expected structure."

def test_deploy_log_content():
    log_path = "/home/user/deploy.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) >= 1, f"{log_path} is empty."
    last_line = lines[-1]

    # Get the latest commit hash from bare repo
    bare_repo_path = "/home/user/deploy.git"
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=bare_repo_path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to get HEAD commit hash from bare repository."
    commit_hash = result.stdout.strip()

    expected_pattern = rf"^SUCCESS: Commit {commit_hash} deployed across 3 containers\.$"
    assert re.match(expected_pattern, last_line), f"Log entry '{last_line}' does not match expected format or commit hash."