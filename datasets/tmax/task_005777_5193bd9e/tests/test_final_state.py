# test_final_state.py

import os
import stat
import subprocess

def test_app_config_permissions():
    config_file = "/home/user/app_config.json"
    assert os.path.isfile(config_file), f"File {config_file} is missing."

    st = os.stat(config_file)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"Permissions of {config_file} are not 0600, got {oct(perms)}."

def test_hook_exists_and_executable():
    hook_path = "/home/user/deploy.git/hooks/pre-receive"
    assert os.path.isfile(hook_path), f"Hook executable {hook_path} is missing."
    assert os.access(hook_path, os.X_OK), f"Hook {hook_path} is not executable."

def test_hook_rejection_logic():
    hook_path = "/home/user/deploy.git/hooks/pre-receive"
    config_file = "/home/user/app_config.json"

    # Temporarily change permissions to 644
    original_perms = stat.S_IMODE(os.stat(config_file).st_mode)
    os.chmod(config_file, 0o644)

    try:
        process = subprocess.run(
            [hook_path],
            input=b"0000 1111 refs/heads/master\n",
            capture_output=True
        )
        assert process.returncode == 1, f"Hook should exit with 1 when permissions are open. Got {process.returncode}."

        expected_stderr = b"Hardening check failed: app_config.json permissions are too open\n"
        assert expected_stderr in process.stderr, f"Hook did not print the expected error message. Got: {process.stderr}"
    finally:
        # Restore permissions
        os.chmod(config_file, original_perms)

def test_hook_acceptance_logic():
    hook_path = "/home/user/deploy.git/hooks/pre-receive"
    config_file = "/home/user/app_config.json"

    # Temporarily ensure permissions are 600
    original_perms = stat.S_IMODE(os.stat(config_file).st_mode)
    os.chmod(config_file, 0o600)

    try:
        process = subprocess.run(
            [hook_path],
            input=b"0000 1111 refs/heads/master\n",
            capture_output=True
        )
        assert process.returncode == 0, f"Hook should exit with 0 when permissions are 0600. Got {process.returncode}."
    finally:
        # Restore permissions
        os.chmod(config_file, original_perms)

def test_push_log():
    log_file = "/home/user/push_result.log"
    assert os.path.isfile(log_file), f"Push log file {log_file} is missing."

    with open(log_file, "r") as f:
        content = f.read()

    assert "master -> master" in content or "master -> master" in content.replace("\r", ""), "Push log does not indicate a successful push to master."

def test_push_success():
    repo_path = "/home/user/deploy.git"
    process = subprocess.run(
        ["git", f"--git-dir={repo_path}", "ls-tree", "HEAD", "deploy.txt"],
        capture_output=True,
        text=True
    )
    assert process.returncode == 0, "Failed to run git ls-tree on the bare repository."
    assert "deploy.txt" in process.stdout, "deploy.txt was not found in the bare repository's HEAD tree."