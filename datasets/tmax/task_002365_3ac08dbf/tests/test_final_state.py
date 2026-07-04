# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_deploy_prod_app_py_exists_and_content():
    app_py_path = "/home/user/deploy/prod/app.py"
    assert os.path.isfile(app_py_path), f"File {app_py_path} does not exist. Deployment may have failed."

    with open(app_py_path, 'r') as f:
        content = f.read().strip()

    assert 'print("Hello World")' in content, f"File {app_py_path} does not contain the expected content."

def test_logs_rotated_correctly():
    log_1_path = "/home/user/deploy/prod/logs/app.log.1"
    log_2_path = "/home/user/deploy/prod/logs/app.log.2"
    log_base_path = "/home/user/deploy/prod/logs/app.log"

    assert os.path.isfile(log_base_path), f"File {log_base_path} does not exist."
    assert os.path.isfile(log_1_path), f"File {log_1_path} does not exist. Log rotation may have failed."
    assert os.path.isfile(log_2_path), f"File {log_2_path} does not exist. Log rotation may have failed."

    with open(log_1_path, 'r') as f:
        content_1 = f.read().strip()
    assert content_1 == "Log entry 2", f"Expected 'Log entry 2' in {log_1_path}, but got '{content_1}'."

    with open(log_2_path, 'r') as f:
        content_2 = f.read().strip()
    assert content_2 == "Log entry 1", f"Expected 'Log entry 1' in {log_2_path}, but got '{content_2}'."

def test_rotate_script_exists():
    rotate_script = "/home/user/rotate.py"
    assert os.path.isfile(rotate_script), f"File {rotate_script} does not exist."

def test_git_push_succeeded():
    repo_path = "/home/user/restore.git"
    try:
        log_output = subprocess.check_output(
            ["git", "log", "-1", "--format=%B"],
            cwd=repo_path,
            stderr=subprocess.STDOUT,
            text=True
        ).strip()
        assert "RESTORE_TEST" in log_output, "The latest commit in the bare repo does not contain 'RESTORE_TEST'. The push might not have succeeded."
    except subprocess.CalledProcessError:
        pytest.fail(f"Failed to get git log from {repo_path}. The push might have failed.")

def test_post_receive_hook_exists_and_executable():
    hook_path = "/home/user/restore.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"File {hook_path} does not exist. Post-receive hook is missing."

    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {hook_path} is not executable."

def test_pre_receive_hook_exists_and_executable():
    hook_path = "/home/user/restore.git/hooks/pre-receive"
    assert os.path.isfile(hook_path), f"File {hook_path} does not exist. Pre-receive hook is missing."

    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {hook_path} is not executable."