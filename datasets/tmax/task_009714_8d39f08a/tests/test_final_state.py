# test_final_state.py

import os
import subprocess
import pytest

def test_monitor_fstab_content():
    """Check if monitor.fstab exists and has correct content."""
    fstab_path = "/home/user/monitor.fstab"
    assert os.path.exists(fstab_path), f"{fstab_path} does not exist."
    with open(fstab_path, "r") as f:
        content = f.read().strip()

    expected_line = "/home/user/logs_pool /home/user/mnt/logs none bind 0 0"
    assert expected_line in content, f"Expected line '{expected_line}' not found in {fstab_path}."

def test_git_hook_exists_and_executable():
    """Check if the post-receive git hook exists and is executable."""
    hook_path = "/home/user/sre-monitor.git/hooks/post-receive"
    assert os.path.exists(hook_path), f"Git hook {hook_path} does not exist."
    assert os.access(hook_path, os.X_OK), f"Git hook {hook_path} is not executable."

def test_rust_binary_deployed():
    """Check if the Rust binary was successfully built and deployed."""
    binary_path = "/home/user/bin/sre-monitor"
    assert os.path.exists(binary_path), f"Binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Binary {binary_path} is not executable."

def test_uptime_log_content():
    """Check if the run_monitor.sh script executed correctly and left the expected log."""
    log_path = "/home/user/logs_pool/uptime.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()

    assert "STATUS: UP" in content, f"'STATUS: UP' not found in {log_path}."

def test_mountpoint_unmounted():
    """Ensure the mount point is currently unmounted."""
    mount_path = "/home/user/mnt/logs"
    assert os.path.exists(mount_path), f"Mount directory {mount_path} does not exist."

    # Check if it's a mountpoint using the mountpoint command
    result = subprocess.run(["mountpoint", "-q", mount_path])
    assert result.returncode != 0, f"{mount_path} is still mounted. Cleanup was not successful."