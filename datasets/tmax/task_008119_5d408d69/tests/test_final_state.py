# test_final_state.py
import os
import time
import subprocess
import pytest

def test_directories_exist():
    """Verify that the required directories have been created."""
    assert os.path.isdir("/home/user/wal_incoming"), "/home/user/wal_incoming directory is missing"
    assert os.path.isdir("/home/user/wal_processed"), "/home/user/wal_processed directory is missing"
    assert os.path.isdir("/home/user/config_active"), "/home/user/config_active directory is missing"

def test_script_exists_and_executable():
    """Verify that the watcher script exists and is executable."""
    script_path = "/home/user/config_watcher.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

def test_watcher_running():
    """Verify that the watcher script is running in the background."""
    output = subprocess.check_output(["ps", "-ef"]).decode()
    assert "config_watcher.sh" in output, "config_watcher.sh is not running in the background"

def test_processing_wal_file():
    """Simulate dropping a WAL file and verify correct processing."""
    wal_content = """# BEGIN TEST FILE
TXN:1001|SYS:network|CMD:set ip 192.168.1.50
TXN:1002|SYS:auth|CMD:add_user admin
# This is a comment
TXN:1003|SYS:network|CMD:restart_interface eth0
TXN:1004|SYS:storage|CMD:mount /dev/sdb1 /mnt/data
# END TEST FILE
"""
    incoming_path = "/home/user/wal_incoming/verify.wal"
    processed_path = "/home/user/wal_processed/verify.wal"

    # Drop the test file
    with open(incoming_path, "w") as f:
        f.write(wal_content)

    # Wait up to 5 seconds for the daemon to process it
    for _ in range(50):
        if os.path.exists(processed_path):
            break
        time.sleep(0.1)

    assert os.path.exists(processed_path), "verify.wal was not moved to wal_processed within 5 seconds. Is the polling loop working?"
    assert not os.path.exists(incoming_path), "verify.wal was not removed from wal_incoming."

    # Verify the generated configuration files
    network_conf = "/home/user/config_active/network.conf"
    auth_conf = "/home/user/config_active/auth.conf"
    storage_conf = "/home/user/config_active/storage.conf"

    assert os.path.exists(network_conf), "network.conf was not created in config_active"
    with open(network_conf, "r") as f:
        content = f.read().strip()
        expected = "set ip 192.168.1.50\nrestart_interface eth0"
        assert content == expected, f"network.conf contents incorrect.\nExpected:\n{expected}\nGot:\n{content}"

    assert os.path.exists(auth_conf), "auth.conf was not created in config_active"
    with open(auth_conf, "r") as f:
        content = f.read().strip()
        expected = "add_user admin"
        assert content == expected, f"auth.conf contents incorrect.\nExpected:\n{expected}\nGot:\n{content}"

    assert os.path.exists(storage_conf), "storage.conf was not created in config_active"
    with open(storage_conf, "r") as f:
        content = f.read().strip()
        expected = "mount /dev/sdb1 /mnt/data"
        assert content == expected, f"storage.conf contents incorrect.\nExpected:\n{expected}\nGot:\n{content}"