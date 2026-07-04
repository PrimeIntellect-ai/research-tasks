# test_final_state.py

import os
import subprocess
import time
import pytest

def test_server_cpp_fixed():
    file_path = "/home/user/app/server.cpp"
    assert os.path.isfile(file_path), f"File {file_path} is missing"

    with open(file_path, "r") as f:
        content = f.read()

    assert "/home/user/run/upstream.sock" in content, "The socket path in server.cpp was not updated to /home/user/run/upstream.sock"

def test_deploy_script_exists_and_executable():
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"Deploy script {script_path} is missing"
    assert os.access(script_path, os.X_OK), f"Deploy script {script_path} is not executable"

def test_deploy_script_execution_and_cleanup():
    script_path = "/home/user/deploy.sh"

    # Run the deployment script
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Deploy script failed with exit code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    # Verify the test_result.log content
    log_path = "/home/user/test_result.log"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created by the deploy script"

    with open(log_path, "r") as f:
        log_content = f.read().strip()

    assert log_content == "Hello from C++!", f"Expected log content 'Hello from C++!', but got '{log_content}'"

    # Allow a small delay for processes to fully terminate
    time.sleep(1)

    # Verify that no nginx or server_bin processes are still running
    ps_result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    processes = ps_result.stdout.splitlines()

    nginx_running = any("nginx" in p and "worker" in p or "nginx" in p and "master" in p for p in processes)
    server_bin_running = any("server_bin" in p and "grep" not in p for p in processes)

    assert not nginx_running, "Nginx process was not cleaned up by the trap in deploy.sh"
    assert not server_bin_running, "server_bin process was not cleaned up by the trap in deploy.sh"