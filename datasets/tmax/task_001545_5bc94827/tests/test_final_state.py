# test_final_state.py
import os
import subprocess
import tempfile

def test_repo_and_symlink():
    repo_path = "/home/user/alert_repo.git"
    hooks_path = os.path.join(repo_path, "hooks")
    global_hooks_path = "/home/user/global_git_hooks"

    assert os.path.isdir(repo_path), f"Bare repository directory {repo_path} does not exist"
    assert os.path.isdir(global_hooks_path), f"Global hooks directory {global_hooks_path} does not exist"

    assert os.path.islink(hooks_path), f"{hooks_path} is not a symbolic link"

    target = os.readlink(hooks_path)
    assert target == global_hooks_path, f"Symlink target is {target}, expected {global_hooks_path}"

def test_git_config():
    repo_path = "/home/user/alert_repo.git"
    result = subprocess.run(
        ["git", "-C", repo_path, "config", "--local", "receive.denyDeletes"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, "Failed to read git config receive.denyDeletes"
    assert result.stdout.strip() == "true", "receive.denyDeletes is not set to true"

def test_hook_files():
    global_hooks_path = "/home/user/global_git_hooks"
    pre_receive_path = os.path.join(global_hooks_path, "pre-receive")
    secret_scanner_path = os.path.join(global_hooks_path, "secret_scanner.py")

    assert os.path.isfile(pre_receive_path), f"{pre_receive_path} does not exist"
    assert os.path.isfile(secret_scanner_path), f"{secret_scanner_path} does not exist"
    assert os.access(pre_receive_path, os.X_OK), f"{pre_receive_path} is not executable"

def test_git_push_behavior():
    repo_path = "/home/user/alert_repo.git"
    log_file = "/home/user/rejected_pushes.log"

    # Remove log file if it exists from manual testing
    if os.path.exists(log_file):
        os.remove(log_file)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Clone the repository
        subprocess.run(["git", "clone", repo_path, tmpdir], check=True, capture_output=True)

        # Configure git for the clone
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmpdir, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=tmpdir, check=True)
        subprocess.run(["git", "config", "init.defaultBranch", "master"], cwd=tmpdir, check=True)

        # 1. Safe commit
        safe_file = os.path.join(tmpdir, "safe_file.txt")
        with open(safe_file, "w") as f:
            f.write("safe data\n")
        subprocess.run(["git", "add", "safe_file.txt"], cwd=tmpdir, check=True)
        subprocess.run(["git", "commit", "-m", "Safe commit"], cwd=tmpdir, check=True, capture_output=True)

        # Push safe commit
        res_safe = subprocess.run(["git", "push", "origin", "master"], cwd=tmpdir, capture_output=True, text=True)
        assert res_safe.returncode == 0, f"Safe push was incorrectly rejected. Stderr: {res_safe.stderr}"

        # 2. Secret commit
        secret_file = os.path.join(tmpdir, "secret_file.txt")
        with open(secret_file, "w") as f:
            f.write("here is a CRITICAL_PRIVATE_KEY_123 in the code\n")
        subprocess.run(["git", "add", "secret_file.txt"], cwd=tmpdir, check=True)
        subprocess.run(["git", "commit", "-m", "Secret commit"], cwd=tmpdir, check=True, capture_output=True)

        # Push secret commit
        res_secret = subprocess.run(["git", "push", "origin", "master"], cwd=tmpdir, capture_output=True, text=True)
        assert res_secret.returncode != 0, "Push with secret key was incorrectly accepted"

        # 3. Verify log
        assert os.path.isfile(log_file), f"Log file {log_file} was not created after rejected push"

        with open(log_file, "r") as f:
            lines = f.read().splitlines()

        assert len(lines) > 0, "Log file is empty"
        expected_log = "ALERT: Push rejected due to secret key in ref refs/heads/master"
        assert lines[-1] == expected_log, f"Incorrect log format. Expected '{expected_log}', got '{lines[-1]}'"