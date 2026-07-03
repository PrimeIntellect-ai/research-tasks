# test_final_state.py

import os
import subprocess
import time

def test_files_exist_and_permissions():
    """Check if the required files exist and have correct permissions."""
    assert os.path.isfile("/home/user/src/metric_exporter.c"), "metric_exporter.c is missing."
    assert os.path.isfile("/home/user/service_mgr.sh"), "service_mgr.sh is missing."
    assert os.path.isfile("/home/user/deploy.sh"), "deploy.sh is missing."

    assert os.access("/home/user/service_mgr.sh", os.X_OK), "service_mgr.sh is not executable."
    assert os.access("/home/user/deploy.sh", os.X_OK), "deploy.sh is not executable."

def test_deployment_and_metrics():
    """Run deploy.sh and verify deployment success, metrics, and graceful shutdown."""

    # Run deploy.sh
    result = subprocess.run(["/home/user/deploy.sh"], capture_output=True, text=True)
    assert result.returncode == 0, f"deploy.sh failed with return code {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

    # Check if binary exists and is executable
    assert os.path.isfile("/home/user/bin/metric_exporter"), "Binary metric_exporter was not compiled to /home/user/bin/."
    assert os.access("/home/user/bin/metric_exporter", os.X_OK), "Binary metric_exporter is not executable."

    # Check deploy.log
    assert os.path.isfile("/home/user/deploy.log"), "deploy.log is missing."
    with open("/home/user/deploy.log", "r") as f:
        log_content = f.read()
    assert "ROLLING_DEPLOY_SUCCESS" in log_content, "deploy.log does not contain 'ROLLING_DEPLOY_SUCCESS'."

    # Check metrics files
    metrics_files = {
        1: "/home/user/metrics_1.prom",
        2: "/home/user/metrics_2.prom"
    }

    for instance, file_path in metrics_files.items():
        assert os.path.isfile(file_path), f"Metrics file {file_path} is missing."
        with open(file_path, "r") as f:
            content = f.read().strip()
        expected = f'dashboard_metric{{instance="{instance}"}} 100'
        assert content == expected, f"Metrics file {file_path} content mismatch. Expected '{expected}', got '{content}'."

    # Test graceful shutdown (SIGTERM handling)
    for instance in [1, 2]:
        stop_result = subprocess.run(["/home/user/service_mgr.sh", "stop", str(instance)], capture_output=True, text=True)
        assert stop_result.returncode == 0, f"service_mgr.sh stop {instance} failed."

    # Wait a brief moment for processes to exit and cleanup
    time.sleep(1)

    # Verify cleanup
    for instance, file_path in metrics_files.items():
        assert not os.path.exists(file_path), f"Metrics file {file_path} was not deleted after SIGTERM."
        pid_file = f"/home/user/run/metric_exporter_{instance}.pid"
        assert not os.path.exists(pid_file), f"PID file {pid_file} was not deleted after stop."

    # Ensure processes are actually dead
    pgrep_result = subprocess.run(["pgrep", "-f", "metric_exporter"], capture_output=True, text=True)
    assert pgrep_result.returncode != 0, "metric_exporter processes are still running after stop."