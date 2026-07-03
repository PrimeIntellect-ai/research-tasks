# test_final_state.py

import os
import socket
import urllib.request
import urllib.error
import subprocess
import pytest

def test_rust_project_exists():
    assert os.path.isdir("/home/user/src/network_monitor"), "Rust project directory does not exist at /home/user/src/network_monitor"
    assert os.path.isfile("/home/user/src/network_monitor/Cargo.toml"), "Cargo.toml not found in the Rust project"

def test_registry_repo_exists():
    assert os.path.isdir("/home/user/registry.git"), "Bare git repository does not exist at /home/user/registry.git"
    assert os.path.isfile("/home/user/registry.git/config"), "Git config not found in bare repository"

def test_post_receive_hook_exists_and_executable():
    hook_path = "/home/user/registry.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"post-receive hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), "post-receive hook is not executable"

def test_post_receive_hook_contents():
    hook_path = "/home/user/registry.git/hooks/post-receive"
    with open(hook_path, "r") as f:
        content = f.read()

    assert "df -k" in content, "Hook does not contain 'df -k'"
    assert "50000" in content, "Hook does not check for 50000 KB disk space"
    assert "cargo build" in content and "--release" in content, "Hook does not contain 'cargo build --release'"
    assert "netmon" in content, "Hook does not contain references to netmon"
    assert "/home/user/netmon.log" in content, "Hook does not redirect output to /home/user/netmon.log"

def test_deploy_directory_exists():
    assert os.path.isdir("/home/user/deploy"), "Deploy directory does not exist at /home/user/deploy"
    assert os.path.isfile("/home/user/deploy/Cargo.toml"), "Checked out code missing in deploy directory"

def test_final_status_file():
    status_path = "/home/user/final_status.txt"
    assert os.path.isfile(status_path), f"{status_path} does not exist"
    with open(status_path, "r") as f:
        content = f.read().strip()
    assert content == "UP", f"final_status.txt contains '{content}', expected 'UP'"

def test_netmon_process_running():
    try:
        output = subprocess.check_output(["pgrep", "-f", "netmon"]).decode("utf-8")
        assert output.strip() != "", "netmon process is not running"
    except subprocess.CalledProcessError:
        pytest.fail("netmon process is not running (pgrep returned no results)")

def test_port_9090_listening():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', 9090))
        assert result == 0, "No process is listening on 127.0.0.1:9090"

def test_port_8181_listening_and_behavior():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', 8181))
        assert result == 0, "netmon is not listening on 127.0.0.1:8181"

    # Since 9090 is listening, 8181 should return 200 OK and UP
    req = urllib.request.Request("http://127.0.0.1:8181/")
    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read().decode("utf-8").strip()
            assert body == "UP", f"Expected body 'UP', got '{body}'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect or received error from netmon: {e}")