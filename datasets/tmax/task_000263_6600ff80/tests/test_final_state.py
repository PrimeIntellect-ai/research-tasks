# test_final_state.py

import os
import subprocess
import time
import socket
import stat
import pytest

def test_device_conf():
    """Check that device.conf exists and contains the correct device ID."""
    conf_path = "/home/user/device.conf"
    assert os.path.exists(conf_path), f"{conf_path} does not exist. Expect script may have failed."
    with open(conf_path, "r") as f:
        content = f.read()
    assert "DEVICE=edge-node-99" in content, f"DEVICE=edge-node-99 not found in {conf_path}."
    assert "TOKEN=secure_token_12345" in content, f"TOKEN not found in {conf_path}."

def test_edge_server_running():
    """Check that edge_server is running."""
    try:
        output = subprocess.check_output(["pgrep", "-f", "edge_server"]).decode("utf-8")
        assert output.strip() != "", "edge_server process is not running."
    except subprocess.CalledProcessError:
        pytest.fail("edge_server process is not running.")

def test_socat_running():
    """Check that socat is running."""
    try:
        output = subprocess.check_output(["pgrep", "-f", "socat"]).decode("utf-8")
        assert output.strip() != "", "socat process is not running."
    except subprocess.CalledProcessError:
        pytest.fail("socat process is not running.")

def test_port_forwarding_and_server():
    """Send a test payload to 9090 and verify it appears in payload.log."""
    payload = "VERIFY_PAYLOAD_12345\n"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect(("127.0.0.1", 9090))
        s.sendall(payload.encode("utf-8"))
        s.close()
    except Exception as e:
        pytest.fail(f"Failed to connect and send data to port 9090: {e}")

    # Give it a moment to process
    time.sleep(1)

    log_path = "/home/user/data/payload.log"
    assert os.path.exists(log_path), f"{log_path} does not exist after sending payload."
    with open(log_path, "r") as f:
        content = f.read()
    assert "VERIFY_PAYLOAD_12345" in content, f"Payload not found in {log_path}. Server or port forwarding might be broken."

def test_payload_log_permissions_and_acl():
    """Check base permissions and ACLs for payload.log."""
    log_path = "/home/user/data/payload.log"
    assert os.path.exists(log_path), f"{log_path} does not exist."

    # Check base permissions (should be 600, plus ACL bits which adds group read)
    # The actual mode with ACLs might be 0640 or similar, but the base owner should have rw.
    st = os.stat(log_path)
    # Check owner is rw
    assert bool(st.st_mode & stat.S_IRUSR), "Owner does not have read permission."
    assert bool(st.st_mode & stat.S_IWUSR), "Owner does not have write permission."
    # Check others have no permissions
    assert not bool(st.st_mode & stat.S_IROTH), "Others should not have read permission."
    assert not bool(st.st_mode & stat.S_IWOTH), "Others should not have write permission."
    assert not bool(st.st_mode & stat.S_IXOTH), "Others should not have execute permission."

    # Check ACLs
    try:
        acl_output = subprocess.check_output(["getfacl", "-c", log_path]).decode("utf-8")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run getfacl: {e}")

    assert "user:guest:r--" in acl_output, f"ACL for guest user is incorrect or missing. getfacl output:\n{acl_output}"