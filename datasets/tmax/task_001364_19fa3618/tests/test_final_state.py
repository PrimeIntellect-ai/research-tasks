# test_final_state.py
import os
import subprocess
import pytest

def test_ci_pipeline_exists_and_executable():
    path = '/home/user/ci_pipeline.sh'
    assert os.path.exists(path), f"CI pipeline script missing at {path}"
    assert os.access(path, os.X_OK), f"CI pipeline script at {path} is not executable"

def test_supervisor_contains_fixes():
    path = '/home/user/supervisor.sh'
    assert os.path.exists(path), f"Supervisor script missing at {path}"
    with open(path, 'r') as f:
        content = f.read()

    # Check for some form of loop or wait for the port
    has_port_wait = '9090' in content and ('nc' in content or '/dev/tcp' in content or 'sleep' in content)
    assert has_port_wait, "Supervisor script does not seem to wait for port 9090."

    # Check for restart logic (e.g., loop, retry, etc.)
    has_restart_logic = 'while' in content or 'for' in content or 'until' in content
    assert has_restart_logic, "Supervisor script does not seem to contain restart logic for the C++ binary."

def test_pipeline_execution_and_output():
    # Run the pipeline
    try:
        proc = subprocess.run(
            ['/home/user/ci_pipeline.sh'], 
            capture_output=True, 
            text=True, 
            timeout=20
        )
    except subprocess.TimeoutExpired:
        pytest.fail("CI pipeline script timed out after 20 seconds.")

    assert proc.returncode == 0, f"Pipeline failed with exit code {proc.returncode}. Output: {proc.stdout}\nError: {proc.stderr}"
    assert "PIPELINE SUCCESS" in proc.stdout, "Pipeline script did not output 'PIPELINE SUCCESS'."

def test_server_log_contains_correct_capacity():
    log_path = '/home/user/server.log'
    assert os.path.exists(log_path), f"{log_path} was not created."

    with open(log_path, 'r') as f:
        log_content = f.read().strip()

    # Calculate the ground truth size
    expected_size = 0
    data_dir = '/home/user/data'
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            expected_size += os.path.getsize(os.path.join(root, file))

    expected_log = f"CAPACITY:{expected_size}"
    assert log_content.startswith(expected_log), f"Expected log to start with '{expected_log}', found '{log_content}'"