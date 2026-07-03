import os
import subprocess
import pytest

def test_final_result_file():
    result_path = "/home/user/final_result.txt"
    assert os.path.exists(result_path), f"File {result_path} does not exist."
    with open(result_path, "r") as f:
        content = f.read().strip()
    assert content == "Hello from Backend!", f"Expected 'Hello from Backend!' in {result_path}, got '{content}'"

def test_post_receive_hook_exists_and_executable():
    hook_path = "/home/user/backend.git/hooks/post-receive"
    assert os.path.exists(hook_path), f"Hook {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Hook {hook_path} is not executable."

def test_git_commit_message():
    repo_path = "/home/user/backend.git"
    try:
        output = subprocess.check_output(
            ["git", "log", "-1", "--pretty=%B"],
            cwd=repo_path,
            stderr=subprocess.STDOUT
        ).decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to get git log from {repo_path}: {e.output.decode('utf-8')}")

    assert "Fix backend port" in output, f"Expected commit message to contain 'Fix backend port', got '{output}'"

def test_auto_deploy_script_exists():
    script_path = "/home/user/auto_deploy.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_app_running_on_correct_port():
    # Nginx proxy_pass is http://127.0.0.1:9000
    try:
        output = subprocess.check_output(
            ["curl", "-s", "http://127.0.0.1:9000"],
            stderr=subprocess.STDOUT
        ).decode("utf-8").strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to curl backend directly on port 9000: {e}")

    assert output == "Hello from Backend!", f"Direct curl to backend port 9000 failed or returned incorrect output: '{output}'"