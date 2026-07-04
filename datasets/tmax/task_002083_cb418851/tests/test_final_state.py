# test_final_state.py

import os
import time
import socket
import subprocess
import pytest

def wait_for_port(port, timeout=5.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.1):
                return True
        except OSError:
            time.sleep(0.1)
    return False

def test_audit_go_performance_and_correctness():
    audit_file = "/home/user/audit.go"
    assert os.path.isfile(audit_file), f"File {audit_file} does not exist."

    # Ensure any existing daemon is killed
    subprocess.run(["pkill", "-f", "auth_daemon"])

    # Start a fresh instance of the daemon
    daemon_proc = subprocess.Popen(["/app/auth_daemon"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        assert wait_for_port(8080), "Daemon did not start listening on port 8080."

        # Run the agent's Go program and measure execution time
        start_time = time.time()
        proc = subprocess.run(["go", "run", audit_file], capture_output=True, text=True)
        duration = time.time() - start_time

        output = proc.stdout.strip()
        expected_flag = "FLAG{g0_c0ncurr3ncy_byp4ss_x92}"

        # Check correctness
        assert proc.returncode == 0, f"Go program failed with return code {proc.returncode}. Stderr:\n{proc.stderr}"
        assert output == expected_flag, f"Go program output was incorrect. Expected '{expected_flag}', got '{output}'"

        # Check performance metric
        assert duration <= 1.0, f"Execution time metric failed: took {duration:.3f}s, threshold is <= 1.0s."

    finally:
        daemon_proc.terminate()
        daemon_proc.wait()