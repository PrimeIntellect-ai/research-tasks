# test_final_state.py

import os
import subprocess
import pytest

def test_client_c_behavior():
    client_c_path = "/home/user/app/client.c"
    assert os.path.isfile(client_c_path), f"{client_c_path} is missing"

    # Compile the client to a temporary location to verify its behavior
    test_bin = "/tmp/test_client_bin"
    compile_proc = subprocess.run(
        ["gcc", client_c_path, "-o", test_bin],
        capture_output=True,
        text=True
    )
    assert compile_proc.returncode == 0, f"Compilation of client.c failed: {compile_proc.stderr}"

    # Run the compiled binary. Assuming port 9090 is closed, it should fail to connect.
    run_proc = subprocess.run(
        [test_bin],
        capture_output=True,
        text=True
    )

    # Check exit code
    assert run_proc.returncode == 5, f"Expected exit code 5, got {run_proc.returncode}"

    # Check stderr
    assert run_proc.stderr.strip() == "Error: Connection refused", f"Expected 'Error: Connection refused' on stderr, got '{run_proc.stderr}'"

def test_systemd_configuration():
    # Check the deployed service file
    deployed_service_path = "/home/user/.config/systemd/user/netclient.service"
    assert os.path.isfile(deployed_service_path), f"{deployed_service_path} is missing"

    with open(deployed_service_path, "r") as f:
        content = f.read()

    assert "After=netserver.service" in content, "Missing 'After=netserver.service' in deployed systemd unit"
    assert "Requires=netserver.service" in content, "Missing 'Requires=netserver.service' in deployed systemd unit"

    # Also check the template file
    template_service_path = "/home/user/app/netclient.service"
    assert os.path.isfile(template_service_path), f"{template_service_path} is missing"

    with open(template_service_path, "r") as f:
        template_content = f.read()

    assert "After=netserver.service" in template_content, "Missing 'After=netserver.service' in template systemd unit"
    assert "Requires=netserver.service" in template_content, "Missing 'Requires=netserver.service' in template systemd unit"

def test_deployment_script_exists_and_executable():
    deploy_script_path = "/home/user/app/deploy.sh"
    assert os.path.isfile(deploy_script_path), f"{deploy_script_path} is missing"
    assert os.access(deploy_script_path, os.X_OK), f"{deploy_script_path} is not executable"

def test_deployment_log_contents():
    log_path = "/home/user/app/deploy.log"
    assert os.path.isfile(log_path), f"{log_path} is missing"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "Deployment script executed successfully", f"deploy.log contents are incorrect: {content}"

def test_client_executable_deployed():
    client_bin_path = "/home/user/app/client"
    assert os.path.isfile(client_bin_path), f"{client_bin_path} is missing"
    assert os.access(client_bin_path, os.X_OK), f"{client_bin_path} is not executable"