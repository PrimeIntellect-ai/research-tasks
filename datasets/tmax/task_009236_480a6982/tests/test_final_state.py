# test_final_state.py

import os
import gzip
import pytest

def test_binary_and_symlink():
    binary_path = "/home/user/deploy/releases/v2/logdaemon"
    symlink_path = "/home/user/deploy/current"

    assert os.path.exists(binary_path), f"Binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary at {binary_path} is not executable"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink"
    target = os.readlink(symlink_path)
    assert target == "/home/user/deploy/releases/v2", f"Symlink points to {target}, expected /home/user/deploy/releases/v2"

def test_fstab_configuration():
    fstab_path = "/home/user/deploy/config/fstab.conf"
    assert os.path.exists(fstab_path), f"fstab config not found at {fstab_path}"

    with open(fstab_path, 'r') as f:
        content = f.read()

    assert "UUID=APP_LOGS" in content, "UUID=APP_LOGS not found in fstab.conf"
    assert "/home/user/deploy/logs" in content, "Mount point /home/user/deploy/logs not found in fstab.conf"

def test_logrotate_configuration():
    logrotate_path = "/home/user/deploy/config/logrotate.conf"
    assert os.path.exists(logrotate_path), f"logrotate config not found at {logrotate_path}"

    with open(logrotate_path, 'r') as f:
        content = f.read()

    assert "size 10" in content, "'size 10' directive missing in logrotate.conf"
    assert "rotate 3" in content, "'rotate 3' directive missing in logrotate.conf"
    assert "compress" in content, "'compress' directive missing in logrotate.conf"
    assert "missingok" in content, "'missingok' directive missing in logrotate.conf"

def test_log_rotation_and_contents():
    rotated_log_path = "/home/user/deploy/logs/daemon.log.1.gz"
    assert os.path.exists(rotated_log_path), f"Rotated log file not found at {rotated_log_path}. Did logrotate run successfully?"

    with gzip.open(rotated_log_path, 'rt') as f:
        content = f.read()

    assert "DEPLOYMENT_V2_SUCCESS" in content, "The expected string 'DEPLOYMENT_V2_SUCCESS' was not found in the rotated log file."