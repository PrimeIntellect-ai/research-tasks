# test_final_state.py

import os
import subprocess
import pytest

def test_expect_script_exists():
    """Check that the Expect script exists."""
    script_path = '/home/user/auto_deploy.exp'
    assert os.path.exists(script_path), f"Expect script '{script_path}' was not found."
    assert os.path.isfile(script_path), f"'{script_path}' is not a file."

def test_deployment_status_file():
    """Check that the deployment status file exists and contains 'READY'."""
    status_path = '/home/user/deploy_dir/status.txt'
    assert os.path.exists(status_path), f"Status file '{status_path}' was not created. Did the Expect script run successfully?"
    with open(status_path, 'r') as f:
        content = f.read().strip()
    assert "READY" in content, f"Status file '{status_path}' does not contain 'READY'."

def test_health_check_cpp_and_binary():
    """Check that the C++ source and compiled binary exist."""
    cpp_path = '/home/user/health_check.cpp'
    bin_path = '/home/user/health_check'
    assert os.path.exists(cpp_path), f"C++ source file '{cpp_path}' was not found."
    assert os.path.exists(bin_path), f"Compiled binary '{bin_path}' was not found."
    assert os.access(bin_path, os.X_OK), f"Compiled binary '{bin_path}' is not executable."

def test_health_log_file():
    """Check that the health log file exists and contains exactly 'HEALTHY\\n'."""
    log_path = '/home/user/deploy_dir/health_log.txt'
    assert os.path.exists(log_path), f"Health log file '{log_path}' was not created. Did you run the health_check binary?"
    with open(log_path, 'r') as f:
        content = f.read()
    assert content == "HEALTHY\n", f"Health log file '{log_path}' content is incorrect. Expected 'HEALTHY\\n', got {repr(content)}"

def test_acl_permissions():
    """Check that the ACL grants read permission to the daemon user on the health log file."""
    log_path = '/home/user/deploy_dir/health_log.txt'
    assert os.path.exists(log_path), f"Health log file '{log_path}' missing, cannot check ACLs."

    result = subprocess.run(['getfacl', log_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to run getfacl on '{log_path}'."

    acl_output = result.stdout
    expected_acl = "user:daemon:r--"

    assert expected_acl in acl_output, f"ACL for daemon user is incorrect or missing. Expected '{expected_acl}' in getfacl output, got:\n{acl_output}"