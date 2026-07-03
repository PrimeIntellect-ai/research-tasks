# test_final_state.py

import os
import subprocess
import time
import pytest

@pytest.fixture(scope="session", autouse=True)
def run_verification():
    """
    Executes the setup script and performs git operations to trigger hooks and monitor.
    """
    setup_script = "/home/user/setup_env.sh"
    assert os.path.exists(setup_script), f"{setup_script} does not exist."

    # 1. Execute the agent's setup script
    subprocess.run(["bash", setup_script], check=True)

    # Wait a brief moment for any background processes to start
    time.sleep(1)

    # 2. Setup a dummy clone to push from
    clone_dir = "/home/user/dummy_clone"
    subprocess.run(["git", "clone", "/home/user/project.git", clone_dir], check=True)

    subprocess.run(["git", "config", "user.name", "Tester"], cwd=clone_dir, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=clone_dir, check=True)

    # Create initial branch to ensure we can push
    subprocess.run(["git", "checkout", "-b", "main"], cwd=clone_dir, check=False)

    # 3. Push commit 1 (should create deploy.log and trigger monitor)
    test_file = os.path.join(clone_dir, "test.txt")
    with open(test_file, "w") as f:
        f.write("test1\n")
    subprocess.run(["git", "add", "test.txt"], cwd=clone_dir, check=True)
    subprocess.run(["git", "commit", "-m", "commit 1"], cwd=clone_dir, check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=clone_dir, check=True)

    # Wait for monitor to process
    time.sleep(2)

    # 4. Push commit 2 -> 60 bytes total in deploy.log
    with open(test_file, "w") as f:
        f.write("test2\n")
    subprocess.run(["git", "commit", "-am", "commit 2"], cwd=clone_dir, check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=clone_dir, check=True)

    time.sleep(1)

    # 5. Push commit 3 -> Should trigger rotation
    with open(test_file, "w") as f:
        f.write("test3\n")
    subprocess.run(["git", "commit", "-am", "commit 3"], cwd=clone_dir, check=True)
    subprocess.run(["git", "push", "origin", "main"], cwd=clone_dir, check=True)

    # Wait for hook to finish
    time.sleep(1)

def test_git_server_initialization():
    """Verify that the bare Git repository was initialized correctly."""
    repo_dir = "/home/user/project.git"
    assert os.path.isdir(repo_dir), f"Bare repository directory {repo_dir} not found."
    assert os.path.isfile(os.path.join(repo_dir, "config")), "Git config not found in bare repo."

    # Check if it's a bare repo
    result = subprocess.run(["git", "config", "--get", "core.bare"], cwd=repo_dir, capture_output=True, text=True)
    assert result.stdout.strip() == "true", "Repository is not configured as bare."

def test_post_receive_hook_exists_and_executable():
    """Verify the post-receive hook exists and is executable."""
    hook_path = "/home/user/project.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Hook script {hook_path} not found."
    assert os.access(hook_path, os.X_OK), f"Hook script {hook_path} is not executable."

def test_monitor_status_output():
    """Verify that the monitor process detected the log and wrote the correct status."""
    status_file = "/home/user/monitor_status.txt"
    assert os.path.isfile(status_file), f"Monitor status file {status_file} not found. Monitor may not have run or failed."

    with open(status_file, "r") as f:
        content = f.read().strip()

    assert content == "STATUS: OK", f"Expected 'STATUS: OK' in {status_file}, got '{content}'"

def test_log_rotation_and_size():
    """Verify that the log file was rotated properly after exceeding 50 bytes."""
    log_file = "/home/user/deploy.log"
    rotated_log = "/home/user/deploy.log.1"

    assert os.path.isfile(rotated_log), f"Rotated log file {rotated_log} not found. Rotation did not occur."
    assert os.path.isfile(log_file), f"Current log file {log_file} not found."

    # Each log entry should be exactly 30 bytes: "DEPLOYED: YYYY-MM-DD HH:MM:SS\n"
    # The rotated log should contain the first two commits (60 bytes)
    rotated_size = os.path.getsize(rotated_log)
    assert rotated_size >= 60, f"Rotated log file size is {rotated_size} bytes, expected at least 60 bytes."

    # The current log should contain only the third commit (30 bytes)
    current_size = os.path.getsize(log_file)
    assert current_size == 30, f"Current log file size is {current_size} bytes, expected exactly 30 bytes."