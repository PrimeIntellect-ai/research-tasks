# test_final_state.py

import os
import time
import subprocess
import signal

def test_deploy_script_exists_and_executable():
    deploy_script = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_script), f"{deploy_script} does not exist."
    assert os.access(deploy_script, os.X_OK), f"{deploy_script} is not executable."

def test_net_monitor_c_exists():
    c_file = "/home/user/net_monitor.c"
    assert os.path.isfile(c_file), f"{c_file} does not exist."

def test_monitor_behavior():
    deploy_script = "/home/user/deploy.sh"
    bashrc_file = "/home/user/.bashrc"
    pid_file = "/home/user/monitor.pid"
    log_file = "/home/user/monitor_alerts.log"
    binary_file = "/home/user/net_monitor"

    # Clean up before test
    if os.path.exists(pid_file):
        os.remove(pid_file)
    if os.path.exists(log_file):
        os.remove(log_file)
    if os.path.exists(binary_file):
        os.remove(binary_file)

    # Start dummy python server
    server_proc = subprocess.Popen(
        ["python3", "-m", "http.server", "8080"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(1) # Wait for server to start

    try:
        # Run deploy.sh
        result = subprocess.run([deploy_script], capture_output=True, text=True)
        assert result.returncode == 0, f"deploy.sh failed with exit code {result.returncode}. Stderr: {result.stderr}"

        # Check .bashrc
        assert os.path.isfile(bashrc_file), f"{bashrc_file} does not exist."
        with open(bashrc_file, "r") as f:
            bashrc_content = f.read()
        assert "export MONITOR_DEPLOYED=true" in bashrc_content, f"export MONITOR_DEPLOYED=true not found in {bashrc_file}."

        # Check binary
        assert os.path.isfile(binary_file), f"{binary_file} was not compiled."
        assert os.access(binary_file, os.X_OK), f"{binary_file} is not executable."

        # Check PID file and process
        assert os.path.isfile(pid_file), f"{pid_file} does not exist."
        with open(pid_file, "r") as f:
            pid_str = f.read().strip()

        assert pid_str.isdigit(), f"{pid_file} does not contain a valid numeric PID."
        monitor_pid = int(pid_str)

        # Check if process is running
        try:
            os.kill(monitor_pid, 0)
        except OSError:
            pytest.fail(f"Process with PID {monitor_pid} from {pid_file} is not running.")

        # Kill server to trigger alert
        server_proc.terminate()
        server_proc.wait(timeout=5)

        # Wait for monitor to detect failures (3 attempts, 1 sec each)
        time.sleep(5)

        # Check log file
        assert os.path.isfile(log_file), f"{log_file} does not exist after failures."
        with open(log_file, "r") as f:
            log_content = f.read()

        expected_log = "[CRITICAL] Port 8080 unresponsive. Executing container restart."
        assert expected_log in log_content, f"Expected alert string not found in {log_file}. Found: {log_content}"

    finally:
        # Cleanup
        if server_proc.poll() is None:
            server_proc.terminate()
            server_proc.wait()

        if 'monitor_pid' in locals():
            try:
                os.kill(monitor_pid, signal.SIGKILL)
            except OSError:
                pass