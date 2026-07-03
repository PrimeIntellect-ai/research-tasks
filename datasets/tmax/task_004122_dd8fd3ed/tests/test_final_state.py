# test_final_state.py

import os
import re
import pytest

BASE_DIR = "/home/user/app_deployment"

def test_directories_exist():
    """Verify all required directories are created."""
    dirs = [
        "config", "src", "bin", "scripts", "logs", "mail", "storage", "container_data"
    ]
    for d in dirs:
        path = os.path.join(BASE_DIR, d)
        assert os.path.isdir(path), f"Directory missing: {path}"

def test_fstab_mock():
    """Verify fstab.mock format and contents."""
    fstab_path = os.path.join(BASE_DIR, "config", "fstab.mock")
    assert os.path.isfile(fstab_path), f"File missing: {fstab_path}"

    with open(fstab_path, "r") as f:
        content = f.read().strip()

    # Allow multiple spaces or tabs
    fields = re.split(r'\s+', content)
    assert len(fields) == 6, f"fstab.mock must have exactly 6 fields, found {len(fields)}"
    assert fields[0] == "/home/user/app_deployment/storage", "Incorrect file system field"
    assert fields[1] == "/home/user/app_deployment/container_data", "Incorrect mount point field"
    assert fields[2] == "none", "Incorrect type field"
    assert fields[3] == "bind", "Incorrect options field"
    assert fields[4] == "0", "Incorrect dump field"
    assert fields[5] == "0", "Incorrect pass field"

def test_storage_index_html():
    """Verify index.html in storage directory."""
    index_path = os.path.join(BASE_DIR, "storage", "index.html")
    assert os.path.isfile(index_path), f"File missing: {index_path}"
    with open(index_path, "r") as f:
        assert f.read().strip() == "DEPLOYMENT_SUCCESS", "index.html does not contain the expected text."

def test_proxy_c_exists():
    """Verify proxy.c exists."""
    proxy_c_path = os.path.join(BASE_DIR, "src", "proxy.c")
    assert os.path.isfile(proxy_c_path), f"File missing: {proxy_c_path}"

def test_proxy_server_executable():
    """Verify proxy_server is compiled and executable."""
    proxy_bin_path = os.path.join(BASE_DIR, "bin", "proxy_server")
    assert os.path.isfile(proxy_bin_path), f"Executable missing: {proxy_bin_path}"
    assert os.access(proxy_bin_path, os.X_OK), f"File is not executable: {proxy_bin_path}"

def test_start_stack_script():
    """Verify start_stack.sh is executable."""
    script_path = os.path.join(BASE_DIR, "scripts", "start_stack.sh")
    assert os.path.isfile(script_path), f"Script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_test_request_log():
    """Verify test_request.log contains the expected output from the proxy."""
    log_path = os.path.join(BASE_DIR, "logs", "test_request.log")
    assert os.path.isfile(log_path), f"Log file missing: {log_path}. Did you run the script?"
    with open(log_path, "r") as f:
        assert "DEPLOYMENT_SUCCESS" in f.read(), "Log file does not contain 'DEPLOYMENT_SUCCESS'."

def test_deployment_alert_email():
    """Verify the exact contents of the deployment alert email."""
    email_path = os.path.join(BASE_DIR, "mail", "deployment_alert.eml")
    assert os.path.isfile(email_path), f"Email file missing: {email_path}"

    expected_content = (
        "From: deploybot@localhost\n"
        "To: sysadmin@localhost\n"
        "Subject: Deployment Status\n"
        "\n"
        "Proxy server is running on port 8080.\n"
        "Backend container is on port 9090.\n"
        "Log output captured.\n"
    )

    with open(email_path, "r") as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), "Email content does not match exactly."