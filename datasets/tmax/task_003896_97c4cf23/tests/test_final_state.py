# test_final_state.py

import os
import re
import pytest

def test_env_var_exported():
    """Check if OPERATOR_BACKUP_DIR is exported in .bashrc or .profile."""
    bashrc_path = "/home/user/.bashrc"
    profile_path = "/home/user/.profile"

    found = False
    expected_string = "OPERATOR_BACKUP_DIR=/home/user/backup"

    if os.path.exists(bashrc_path):
        with open(bashrc_path, "r") as f:
            if expected_string in f.read():
                found = True

    if not found and os.path.exists(profile_path):
        with open(profile_path, "r") as f:
            if expected_string in f.read():
                found = True

    assert found, f"Could not find '{expected_string}' in {bashrc_path} or {profile_path}"

def test_backup_exists():
    """Check if the backup archive was created at the expected location."""
    backup_path = "/home/user/backup/manifests_backup.tar.gz"
    assert os.path.isfile(backup_path), f"Backup archive not found at {backup_path}"

def test_proxy_conf_weights():
    """Verify the proxy configuration has correct weights for the services."""
    proxy_conf_path = "/home/user/proxy.conf"
    assert os.path.isfile(proxy_conf_path), f"Proxy configuration not found at {proxy_conf_path}"

    with open(proxy_conf_path, "r") as f:
        content = f.read()

    v1_match = re.search(r'8081.*weight[= ]?(\d+)', content)
    v2_match = re.search(r'8082.*weight[= ]?(\d+)', content)

    assert v1_match is not None, "Could not find weight for port 8081 (service-v1) in proxy.conf"
    assert v2_match is not None, "Could not find weight for port 8082 (service-v2) in proxy.conf"

    w1 = float(v1_match.group(1))
    w2 = float(v2_match.group(1))

    assert (w1 + w2) > 0, "Sum of weights must be greater than 0"

    p1 = w1 / (w1 + w2)
    target_p1 = 0.75

    mse = (p1 - target_p1) ** 2
    threshold = 0.001

    assert mse <= threshold, f"Weight ratio MSE {mse} exceeds threshold {threshold}. Extracted ratio for v1: {p1:.3f}, expected: {target_p1}"