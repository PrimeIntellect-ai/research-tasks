# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_git_repo_initialized():
    """Verify that /home/user/infra-repo is a valid Git repository."""
    repo_path = "/home/user/infra-repo"
    assert os.path.isdir(repo_path), f"{repo_path} directory does not exist."
    assert os.path.isdir(os.path.join(repo_path, ".git")), f"{repo_path} is not a git repository."

def test_provisioner_script_exists():
    """Verify that the provisioner script exists."""
    script_path = "/home/user/provisioner.py"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

def test_requests_file_exists():
    """Verify that the requests.txt file exists."""
    req_path = "/home/user/requests.txt"
    assert os.path.isfile(req_path), f"{req_path} does not exist."

def test_post_commit_hook():
    """Verify the post-commit hook exists and is executable."""
    hook_path = "/home/user/infra-repo/.git/hooks/post-commit"
    assert os.path.isfile(hook_path), f"Post-commit hook at {hook_path} does not exist."

    # Check if executable
    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Post-commit hook {hook_path} is not executable."

def test_provisioning_workflow():
    """Simulate the provisioning workflow to ensure the script and hook work correctly."""
    req_path = "/home/user/requests.txt"
    repo_path = "/home/user/infra-repo"
    services_path = "/home/user/services"

    # 1. Provide first batch of requests
    with open(req_path, "w") as f:
        f.write("START web_frontend\n")
        f.write("START db_backend\n")
        f.write("STOP cache_layer\n")

    # 2. Trigger the hook via git commit
    try:
        subprocess.run(
            ["git", "commit", "--allow-empty", "-m", "Trigger provisioning 1"],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Git commit failed: {e.stderr}")

    # 3. Verify outputs
    def check_status(service, expected):
        status_file = os.path.join(services_path, service, "status")
        assert os.path.isfile(status_file), f"Status file for {service} not found at {status_file}."
        with open(status_file, "r") as f:
            content = f.read().strip()
        assert content == expected, f"Expected {service} status to be '{expected}', but got '{content}'."

    check_status("web_frontend", "active")
    check_status("db_backend", "active")
    check_status("cache_layer", "inactive")

    # 4. Provide second batch of requests
    with open(req_path, "a") as f:
        f.write("RESTART web_frontend\n")
        f.write("START message_queue\n")

    # 5. Trigger again
    try:
        subprocess.run(
            ["git", "commit", "--allow-empty", "-m", "Trigger provisioning 2"],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Second Git commit failed: {e.stderr}")

    # 6. Verify second batch
    check_status("web_frontend", "restarted")
    check_status("message_queue", "active")