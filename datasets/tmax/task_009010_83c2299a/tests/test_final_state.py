# test_final_state.py

import os
import stat
import urllib.request
import urllib.error
import pytest

def test_backend_permissions_fixed():
    """Verify that the permissions on /home/user/backend are no longer 000."""
    path = "/home/user/backend"
    assert os.path.exists(path), f"Directory {path} does not exist."
    st = os.stat(path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms != 0, f"Permissions on {path} are still 000. They must be fixed to allow access."

def test_symlink_logs_created():
    """Verify that /home/user/logs is a symlink to /home/user/backend/logs."""
    link_path = "/home/user/logs"
    target_path = "/home/user/backend/logs"

    assert os.path.islink(link_path), f"{link_path} is not a symbolic link."
    actual_target = os.readlink(link_path)
    assert actual_target == target_path, f"Symlink {link_path} points to {actual_target}, expected {target_path}."

def test_startup_log_exists():
    """Verify that the Rust application wrote startup.log into the logs directory."""
    log_file = "/home/user/logs/startup.log"
    assert os.path.isfile(log_file), f"Startup log file {log_file} does not exist."

def test_final_output_content():
    """Verify that final_output.txt contains the correct backend response."""
    output_file = "/home/user/final_output.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    with open(output_file, "r") as f:
        content = f.read().strip()

    expected_content = "BACKEND_SUCCESS_77812"
    assert content == expected_content, f"Content of {output_file} was '{content}', expected '{expected_content}'."

def test_nginx_and_forwarder_active():
    """Verify that Nginx is running and proxying through the Rust forwarder successfully."""
    # We can do a live test to 127.0.0.1:8080/api to ensure the chain is actually working
    url = "http://127.0.0.1:8080/api"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            body = response.read().decode('utf-8').strip()
            assert body == "BACKEND_SUCCESS_77812", f"Live request to {url} returned '{body}', expected 'BACKEND_SUCCESS_77812'."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to {url} or received an error. Is Nginx and the Rust forwarder running? Error: {e}")