# test_final_state.py

import os
import subprocess
import pytest

def test_bare_repo_exists():
    repo_path = "/home/user/iot_repo.git"
    assert os.path.isdir(repo_path), f"Bare repository directory {repo_path} does not exist."
    assert os.path.isfile(os.path.join(repo_path, "config")), f"{repo_path} does not appear to be a valid Git repository."

def test_active_repo_symlink():
    symlink_path = "/home/user/active_repo"
    target_path = "/home/user/iot_repo.git"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."
    assert os.readlink(symlink_path) == target_path, f"Symlink {symlink_path} does not point to {target_path}."

def test_deploy_stage_directory():
    deploy_dir = "/home/user/deploy_stage"
    assert os.path.isdir(deploy_dir), f"Deployment directory {deploy_dir} does not exist."

def test_firmware_deployed():
    firmware_path = "/home/user/deploy_stage/firmware.bin"
    assert os.path.isfile(firmware_path), f"Deployed file {firmware_path} does not exist. Did the post-receive hook checkout the files?"
    with open(firmware_path, "r") as f:
        content = f.read().strip()
    assert content == "v1.2.0", f"Expected firmware.bin to contain 'v1.2.0', but got '{content}'."

def test_route_info_logged():
    route_file = "/home/user/deploy_stage/route_info.txt"
    assert os.path.isfile(route_file), f"Route info file {route_file} does not exist. Did the post-receive hook create it?"

    # Recompute expected output
    try:
        expected_output = subprocess.check_output(["ip", "route", "get", "8.8.8.8"], universal_newlines=True)
    except subprocess.CalledProcessError:
        expected_output = ""

    with open(route_file, "r") as f:
        actual_output = f.read()

    assert actual_output.strip() == expected_output.strip(), f"Content of {route_file} does not match the expected output of 'ip route get 8.8.8.8'."

def test_expect_script_exists_and_executable():
    script_path = "/home/user/trigger_sync.exp"
    assert os.path.isfile(script_path), f"Expect script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Expect script {script_path} is not executable."

def test_post_receive_hook_exists_and_executable():
    hook_path = "/home/user/iot_repo.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Git hook {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Git hook {hook_path} is not executable."

def test_device_sync_log():
    log_path = "/home/user/device_sync_log.txt"
    assert os.path.isfile(log_path), f"Device sync log {log_path} does not exist. The simulated IoT device was not notified correctly."
    with open(log_path, "r") as f:
        content = f.read().strip()
    expected_content = "SYNC_SUCCESS: /home/user/deploy_stage"
    assert content == expected_content, f"Expected device sync log to contain '{expected_content}', but got '{content}'."