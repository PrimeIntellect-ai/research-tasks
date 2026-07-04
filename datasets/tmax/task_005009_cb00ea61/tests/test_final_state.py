# test_final_state.py

import os
import pytest

def test_vm_launcher_service_dependencies():
    path = "/home/user/.config/systemd/user/vm-launcher.service"
    assert os.path.isfile(path), f"Service file {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "Requires=prepare-disk.service" in content, "vm-launcher.service is missing 'Requires=prepare-disk.service'."
    assert "After=prepare-disk.service" in content, "vm-launcher.service is missing 'After=prepare-disk.service'."

def test_active_disk_symlink_created():
    symlink_path = "/home/user/active-disk.qcow2"
    target_path = "/home/user/storage/base-image.qcow2"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink. Did prepare-disk.service run?"
    assert os.readlink(symlink_path) == target_path, f"{symlink_path} does not point to {target_path}."

def test_vm_run_log_success():
    log_path = "/home/user/vm_run.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did vm-launcher.service run successfully?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "SUCCESS" in content, f"Log file {log_path} does not contain 'SUCCESS'. The script may have failed."