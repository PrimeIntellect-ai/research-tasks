# test_final_state.py

import os
import subprocess
import pytest

def test_deploy_script_exists_and_executable():
    deploy_script = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_script), f"{deploy_script} does not exist."
    assert os.access(deploy_script, os.X_OK), f"{deploy_script} is not executable."

def test_vm_service_binary_exists_and_executable():
    binary_path = "/home/user/bin/vm_service"
    assert os.path.isfile(binary_path), f"{binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable."

def test_run_deploy_script_and_check_state():
    # Execute the deployment script
    result = subprocess.run(["bash", "/home/user/deploy.sh"], capture_output=True, text=True)
    assert result.returncode == 0, f"deploy.sh failed with return code {result.returncode}. stderr: {result.stderr}"

    # Check if .bashrc was updated
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} does not exist."
    with open(bashrc_path, "r") as f:
        bashrc_content = f.read()
    assert "export VNC_DISPLAY=:5" in bashrc_content, f"The required export statement was not found in {bashrc_path}."

    # Check if service.log.bak has the correct output
    bak_log_path = "/home/user/logs/service.log.bak"
    assert os.path.isfile(bak_log_path), f"{bak_log_path} does not exist."
    with open(bak_log_path, "r") as f:
        bak_content = f.read().strip()
    expected_log = "Starting QEMU on VNC display :5"
    assert bak_content == expected_log, f"Expected '{expected_log}' in {bak_log_path}, got '{bak_content}'."

    # Check if service.log was truncated
    log_path = "/home/user/logs/service.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."
    assert os.path.getsize(log_path) == 0, f"{log_path} is not empty (size > 0 bytes)."

def test_vm_service_default_behavior():
    # Run the binary without VNC_DISPLAY set
    env = os.environ.copy()
    if "VNC_DISPLAY" in env:
        del env["VNC_DISPLAY"]

    binary_path = "/home/user/bin/vm_service"
    result = subprocess.run([binary_path], env=env, capture_output=True, text=True)

    assert result.returncode == 0, f"{binary_path} crashed or returned non-zero when VNC_DISPLAY was unset."

    expected_output = "Starting QEMU on VNC display :1"
    actual_output = result.stdout.strip()
    assert actual_output == expected_output, f"Expected output '{expected_output}', got '{actual_output}'."