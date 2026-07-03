# test_final_state.py

import os
import stat

def test_start_sh_modified():
    path = "/home/user/start.sh"
    assert os.path.isfile(path), f"Expected file {path} to exist."

    with open(path, "r") as f:
        content = f.read()

    state_idx = content.find("state_svc.py")
    deploy_idx = content.find("deploy_svc.py")
    sleep_idx = content.find("sleep")

    assert state_idx != -1, "start.sh is missing state_svc.py"
    assert deploy_idx != -1, "start.sh is missing deploy_svc.py"
    assert sleep_idx != -1, "start.sh is missing a sleep command"

    assert state_idx < deploy_idx, "state_svc.py must be started before deploy_svc.py in start.sh"
    assert state_idx < sleep_idx < deploy_idx, "The sleep command must be placed between starting state_svc.py and deploy_svc.py"

def test_post_receive_executable():
    path = "/home/user/registry.git/hooks/post-receive"
    assert os.path.isfile(path), f"Expected file {path} to exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR) or bool(st.st_mode & stat.S_IXGRP) or bool(st.st_mode & stat.S_IXOTH), \
        f"Expected {path} to have executable permissions."

def test_workspace_and_trigger():
    path = "/home/user/workspace/trigger.txt"
    assert os.path.isfile(path), f"Expected file {path} to exist. Did you clone the repo and create trigger.txt?"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "deploy", f"Expected trigger.txt to contain 'deploy', but got '{content}'"

def test_deploy_log_exists_and_content():
    path = "/home/user/deploy.log"
    assert os.path.isfile(path), f"Expected file {path} to exist. The deployment hook likely did not trigger successfully."

    with open(path, "r") as f:
        content = f.read()

    assert content == "Deployment successful!\n", f"Expected deploy.log to contain exactly 'Deployment successful!\\n', but got {repr(content)}"