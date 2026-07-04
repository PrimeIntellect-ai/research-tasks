# test_final_state.py

import os
import subprocess
import pytest

def test_deployment_log_exists_and_content():
    """Verify that the deployment.log exists and contains the expected success message."""
    log_path = "/home/user/deployment.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist. Did you run deploy.sh successfully?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "VNC_HEALTH_CHECK_PASSED", f"Expected 'VNC_HEALTH_CHECK_PASSED' in {log_path}, got '{content}'"

def test_config_env_fixed():
    """Verify that DOWNSTREAM_TARGET was corrected in config.env."""
    config_path = "/home/user/config.env"
    assert os.path.isfile(config_path), f"{config_path} is missing."

    with open(config_path, "r") as f:
        content = f.read()

    assert 'export DOWNSTREAM_TARGET="/home/user/vm_sockets/vnc.sock"' in content, \
        "DOWNSTREAM_TARGET in config.env was not corrected to match UPSTREAM_SOCKET."

def test_acl_permissions():
    """Verify that the correct ACL permissions were applied to /home/user/vm_sockets."""
    dir_path = "/home/user/vm_sockets"
    assert os.path.isdir(dir_path), f"{dir_path} directory is missing."

    try:
        result = subprocess.run(
            ["getfacl", dir_path],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run getfacl on {dir_path}: {e.stderr}")

    assert "group:users:rwx" in output, \
        f"ACL permissions for group 'users' are missing or incorrect on {dir_path}."