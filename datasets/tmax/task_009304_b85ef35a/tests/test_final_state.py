# test_final_state.py

import os
import stat

def test_post_receive_executable():
    hook_path = "/home/user/repo.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"The post-receive hook {hook_path} does not exist."

    st = os.stat(hook_path)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, f"The post-receive hook {hook_path} is not executable. You need to fix its permissions."

def test_deploy_log_success():
    log_path = "/home/user/app/deploy.log"
    assert os.path.isfile(log_path), f"The deploy log {log_path} does not exist. Did the pipeline run successfully?"

    with open(log_path, 'r') as f:
        content = f.read()

    assert "DEPLOY_SUCCESS" in content, f"The deploy log does not contain 'DEPLOY_SUCCESS'. Found instead: {content.strip()}"

def test_post_receive_socket_path_fixed():
    hook_path = "/home/user/repo.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"The post-receive hook {hook_path} does not exist."

    with open(hook_path, 'r') as f:
        content = f.read()

    assert "/home/user/upstream.sock" in content, "The post-receive hook does not contain the correct upstream socket path."
    assert "/home/user/app/upstream.sock" not in content, "The post-receive hook still contains the misconfigured socket path."