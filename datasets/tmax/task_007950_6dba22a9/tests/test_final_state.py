# test_final_state.py
import os
import subprocess
import pytest

def test_bare_repo_exists():
    """Verify the bare Git repository exists."""
    assert os.path.isdir("/home/user/router_repo.git"), "Bare Git repository /home/user/router_repo.git does not exist."
    assert os.path.isfile("/home/user/router_repo.git/HEAD"), "/home/user/router_repo.git is not a valid Git repository."

def test_deploy_directory_exists():
    """Verify the deployment directory exists."""
    assert os.path.isdir("/home/user/router_deploy"), "Deployment directory /home/user/router_deploy does not exist."

def test_compiled_binary_exists_and_executable():
    """Verify the compiled router binary exists and is executable."""
    binary_path = "/home/user/router_deploy/router"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Compiled binary {binary_path} is not executable."

def test_pipeline_log_success():
    """Verify the pipeline log contains the success message."""
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"Pipeline log {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()
    assert "PIPELINE_SUCCESS: 192.168.50.1" in content, "Pipeline log does not contain the expected success message."

def test_mock_routes_conf_exists_and_correct():
    """Verify the mock_routes.conf file exists and contains the correct entries."""
    conf_path = "/home/user/mock_routes.conf"
    assert os.path.isfile(conf_path), f"Mock routes config {conf_path} does not exist."
    with open(conf_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert "10.0.5.0/24 via 192.168.50.1" in lines, "Missing route for 10.0.5.0/24."
    assert "0.0.0.0/0 via 192.168.1.1" in lines, "Missing route for 0.0.0.0/0."
    assert len(lines) == 2, "mock_routes.conf should contain exactly two routing entries."

def test_config_routes_idempotency():
    """Verify that config_routes.sh is idempotent."""
    conf_path = "/home/user/mock_routes.conf"
    script_path = "/home/user/router_deploy/config_routes.sh"

    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(conf_path, "r") as f:
        lines_before = len(f.readlines())

    # Run the script again
    result = subprocess.run(["bash", script_path], capture_output=True)
    assert result.returncode == 0, "config_routes.sh failed to execute."

    with open(conf_path, "r") as f:
        lines_after = len(f.readlines())

    assert lines_before == lines_after, "config_routes.sh is not idempotent; line count changed after re-running."

def test_router_binary_behavior():
    """Verify the behavior of the compiled router C program."""
    binary_path = "/home/user/router_deploy/router"

    # Test existing route
    result1 = subprocess.run([binary_path, "0.0.0.0/0"], capture_output=True, text=True)
    assert result1.returncode == 0, "Router program failed to execute."
    assert result1.stdout.strip() == "192.168.1.1", "Router program did not output the correct NEXT_HOP for 0.0.0.0/0."

    # Test non-existing route
    result2 = subprocess.run([binary_path, "10.99.99.0/24"], capture_output=True, text=True)
    assert result2.returncode == 0, "Router program failed to execute."
    assert result2.stdout.strip() == "DROP", "Router program did not output DROP for an unknown network."