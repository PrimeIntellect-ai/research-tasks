# test_final_state.py
import os
import json

def test_fstab_conf_exists_and_content():
    fstab_path = "/home/user/fstab.conf"
    assert os.path.exists(fstab_path), f"{fstab_path} is missing"
    with open(fstab_path, "r") as f:
        content = f.read()
    assert "/dev/mapper/data_vol /home/user/mnt/data ext4 defaults 0 0" in content, f"{fstab_path} content is invalid"

def test_mount_directory_created():
    dir_path = "/home/user/mnt/data"
    assert os.path.isdir(dir_path), f"Directory {dir_path} was not created"

def test_monitor_json_valid():
    json_path = "/home/user/project/monitor.json"
    assert os.path.exists(json_path), f"{json_path} is missing"
    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} does not contain valid JSON"

    assert data.get("mount_target") == "/home/user/mnt/data", "Incorrect mount_target in JSON"
    assert data.get("network_ok") is True, "network_ok should be true in JSON"

def test_dockerfile_content():
    dockerfile_path = "/home/user/project/Dockerfile"
    assert os.path.exists(dockerfile_path), f"{dockerfile_path} is missing"
    with open(dockerfile_path, "r") as f:
        content = f.read()

    assert "ubuntu:22.04" in content, "Dockerfile missing base image ubuntu:22.04"
    assert "g++" in content, "Dockerfile missing g++ installation"
    assert "nas_monitor" in content, "Dockerfile missing compilation instructions for nas_monitor"

def test_ci_sh_executable_and_content():
    ci_path = "/home/user/project/ci.sh"
    assert os.path.exists(ci_path), f"{ci_path} is missing"
    assert os.access(ci_path, os.X_OK), f"{ci_path} must be executable"

    with open(ci_path, "r") as f:
        content = f.read()

    assert "8080" in content, "ci.sh missing port 8080 for python server"
    assert "g++" in content, "ci.sh missing g++ compilation command"
    assert "nas_monitor" in content, "ci.sh missing execution of nas_monitor"