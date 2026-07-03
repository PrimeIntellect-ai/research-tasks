# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_deploy_and_logs_directories_exist():
    deploy_dir = "/home/user/deploy"
    logs_dir = "/home/user/logs"

    assert os.path.isdir(deploy_dir), f"Deployment directory {deploy_dir} does not exist."
    assert os.path.isdir(logs_dir), f"Logs directory {logs_dir} does not exist."

def test_post_receive_hook_exists_and_executable():
    hook_path = "/home/user/repo/netmon.git/hooks/post-receive"

    assert os.path.isfile(hook_path), f"Git hook {hook_path} does not exist."

    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Git hook {hook_path} is not executable."

def test_monitor_compiled_and_executable():
    monitor_bin = "/home/user/deploy/monitor"

    assert os.path.isfile(monitor_bin), f"Compiled binary {monitor_bin} does not exist."

    st = os.stat(monitor_bin)
    assert bool(st.st_mode & stat.S_IXUSR), f"Compiled binary {monitor_bin} is not executable."

def test_net_log_exists_and_contains_jst():
    log_path = "/home/user/logs/net.log"

    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    assert "JST" in content, f"Log file {log_path} does not contain the JST timezone identifier."
    assert "Port 8080" in content, f"Log file {log_path} does not contain 'Port 8080'."

def test_monitor_c_fixed_and_pushed():
    workspace_monitor = "/home/user/workspace/monitor.c"

    assert os.path.isfile(workspace_monitor), f"Source file {workspace_monitor} does not exist."

    with open(workspace_monitor, "r") as f:
        content = f.read()

    assert "<sys/socket.h>" in content or "<arpa/inet.h>" in content or "<netinet/in.h>" in content, \
        "The required network headers were not added to monitor.c."

    # Check if the repo is clean (changes pushed)
    result = subprocess.run(["git", "-C", "/home/user/workspace", "status", "--porcelain"], capture_output=True, text=True)
    assert result.stdout.strip() == "", "There are uncommitted or unpushed changes in the workspace."