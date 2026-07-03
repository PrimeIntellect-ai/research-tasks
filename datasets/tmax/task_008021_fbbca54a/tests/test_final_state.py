# test_final_state.py

import os
import subprocess
import time
import pytest

@pytest.fixture(scope="session", autouse=True)
def run_student_script():
    script_path = "/home/user/setup_edge_pipeline.sh"
    assert os.path.isfile(script_path), f"Student script {script_path} not found."
    assert os.access(script_path, os.X_OK), f"Student script {script_path} is not executable."

    # Run the script as the 'user' user if possible, or just run it directly.
    # Assuming the tests run in the same environment.
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with exit code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    # Give a brief moment for any background processes to finish closing
    time.sleep(1)

def test_deploy_log_exists_and_correct():
    log_path = "/home/user/deploy.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    assert "DEPLOYMENT_SUCCESSFUL" in content, f"Log file {log_path} does not contain 'DEPLOYMENT_SUCCESSFUL'."

def test_deployed_file_exists_and_correct():
    app_path = "/home/user/iot-active/sensor_app.sh"
    assert os.path.isfile(app_path), f"Deployed file {app_path} is missing."

    with open(app_path, "r") as f:
        content = f.read()

    assert "Reading sensor data" in content, f"Deployed file {app_path} content is incorrect."

def test_ssh_tunnel_closed():
    # Check if port 9999 is listening
    try:
        # ss -tln output
        result = subprocess.run(["ss", "-tln"], capture_output=True, text=True, check=True)
        assert ":9999 " not in result.stdout, "SSH tunnel was not closed; port 9999 is still listening."
    except FileNotFoundError:
        # Fallback if ss is not available
        result = subprocess.run(["netstat", "-tln"], capture_output=True, text=True)
        assert ":9999 " not in result.stdout, "SSH tunnel was not closed; port 9999 is still listening."