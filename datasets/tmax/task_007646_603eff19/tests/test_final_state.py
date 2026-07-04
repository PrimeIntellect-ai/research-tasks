# test_final_state.py

import os
import subprocess
import pytest

def test_profile_fixed():
    profile_path = "/home/user/.profile"
    assert os.path.isfile(profile_path), f"{profile_path} is missing."

    with open(profile_path, "r") as f:
        content = f.read()

    assert "export APP_SOCK=" in content, "APP_SOCK environment variable is not exported in .profile."
    assert "export APP_SOC=" not in content, "The typo (APP_SOC) in .profile was not removed."

def test_backend_fixed():
    backend_path = "/home/user/app/backend.py"
    assert os.path.isfile(backend_path), f"{backend_path} is missing."

    with open(backend_path, "r") as f:
        content = f.read()

    # Check if there is some logic to create directories
    has_dir_creation = any(keyword in content for keyword in ["os.makedirs", "os.mkdir", "mkdir", "Path"])
    assert has_dir_creation, "backend.py does not appear to contain directory creation logic."

def test_verify_deploy_script_and_results():
    script_path = "/home/user/verify_deploy.py"
    assert os.path.isfile(script_path), f"{script_path} is missing. Did you create the verification script?"

    # Execute the script as the user
    try:
        subprocess.run(
            ["su", "-", "user", "-c", f"python3 {script_path}"],
            check=True,
            capture_output=True,
            text=True,
            timeout=15
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {script_path} failed.\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution of {script_path} timed out. Are the background processes hanging?")

    # Verify that the directory was created
    run_dir = "/home/user/run"
    assert os.path.isdir(run_dir), f"The directory {run_dir} was not created by the backend script."

    # Verify the log file contents
    log_path = "/home/user/deploy_results.log"
    assert os.path.isfile(log_path), f"The log file {log_path} was not created."

    with open(log_path, "r") as f:
        log_content = f.read().strip()

    expected_content = "STATUS: 200 | BODY: Backend Operational"
    assert log_content == expected_content, f"Log file content is incorrect.\nExpected: '{expected_content}'\nGot: '{log_content}'"