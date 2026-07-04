# test_final_state.py
import os
import socket
import subprocess
import time
import pytest

@pytest.fixture(scope="session", autouse=True)
def run_deploy_script():
    """
    Kills any existing workers, cleans up files, runs the student's deploy.py,
    and waits for it to complete before running the assertions.
    """
    # Clean up any existing worker processes
    subprocess.run(["pkill", "-f", "worker.py"], stderr=subprocess.DEVNULL)

    # Clean up state files
    files_to_remove = [
        "/home/user/deploy/w1.ready",
        "/home/user/deploy/w2.ready",
        "/home/user/deploy/w3.ready",
        "/home/user/deploy/status.log"
    ]
    for f in files_to_remove:
        if os.path.exists(f):
            os.remove(f)

    # Run the deploy script
    deploy_script = "/home/user/deploy/deploy.py"
    assert os.path.exists(deploy_script), f"{deploy_script} does not exist."

    try:
        subprocess.run(
            ["python3", deploy_script],
            timeout=20,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except subprocess.TimeoutExpired:
        pytest.fail("deploy.py timed out after 20 seconds. It may be hanging or failing to detect readiness.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"deploy.py exited with an error: {e.stderr.decode()}")

    yield

    # Teardown: kill workers after tests
    subprocess.run(["pkill", "-f", "worker.py"], stderr=subprocess.DEVNULL)

def test_status_log():
    """Verify that status.log contains the correct success message."""
    log_path = "/home/user/deploy/status.log"
    assert os.path.isfile(log_path), f"{log_path} was not created."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "DEPLOYMENT SUCCESSFUL", f"Expected 'DEPLOYMENT SUCCESSFUL' in status.log, got '{content}'"

def test_readiness_files():
    """Verify that all worker readiness files exist."""
    for i in range(1, 4):
        ready_file = f"/home/user/deploy/w{i}.ready"
        assert os.path.isfile(ready_file), f"Readiness file {ready_file} is missing. Worker {i} may have crashed or not started."

def test_worker_ports_listening():
    """Verify that all workers are listening on their respective ports."""
    ports = [8081, 8082, 8083]
    for i, port in enumerate(ports, start=1):
        is_listening = False
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                is_listening = True
        except OSError:
            pass

        assert is_listening, f"Worker {i} is not listening on port {port}. It may have crashed due to unmet dependencies."