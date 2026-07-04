# test_final_state.py

import os
import subprocess
import pytest

def test_device_fstab_conf():
    path = "/home/user/device_fstab.conf"
    assert os.path.isfile(path), f"{path} does not exist."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "DATA_MOUNT=/home/user/sensor_data", f"Incorrect content in {path}."

def test_c_service_files():
    assert os.path.isfile("/home/user/src/edge_server.c"), "C source file edge_server.c is missing."
    assert os.path.isfile("/home/user/src/edge_server"), "Compiled edge_server executable is missing."
    assert os.access("/home/user/src/edge_server", os.X_OK), "edge_server is not executable."

def test_staged_deployment_symlink():
    symlink_path = "/home/user/deploy/active"
    target_dir = "/home/user/deploy/v1"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."
    target = os.readlink(symlink_path)

    # Target could be absolute or relative
    if not os.path.isabs(target):
        target = os.path.normpath(os.path.join(os.path.dirname(symlink_path), target))

    assert target == target_dir, f"Symlink {symlink_path} does not point to {target_dir}."
    assert os.path.isfile(os.path.join(symlink_path, "edge_server")), "edge_server not found in the active deployment."

def test_processes_running():
    try:
        output = subprocess.check_output(["ps", "-eo", "command"], text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute ps command.")

    lines = output.splitlines()

    edge_server_running = any("edge_server" in line and "ps " not in line for line in lines)
    assert edge_server_running, "The edge_server process is not running."

    ssh_forwarding_running = False
    for line in lines:
        if line.startswith("ssh ") or line.find("/ssh ") != -1:
            if "-L" in line and "9090" in line and "8080" in line:
                ssh_forwarding_running = True
                break

    assert ssh_forwarding_running, "SSH port forwarding process (9090 to 8080) is not running."

def test_deploy_result_log():
    log_path = "/home/user/deploy_result.log"
    reading_path = "/home/user/sensor_data/reading.txt"

    assert os.path.isfile(log_path), f"{log_path} does not exist."
    assert os.path.isfile(reading_path), f"{reading_path} does not exist."

    with open(log_path, "r") as f:
        log_content = f.read()

    with open(reading_path, "r") as f:
        reading_content = f.read()

    assert log_content == reading_content, "The contents of deploy_result.log do not match reading.txt."