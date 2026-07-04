# test_final_state.py

import os
import re
import time
import socket
import subprocess
import pytest

def wait_for_port(port, timeout=5.0):
    start = time.time()
    while time.time() - start < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) == 0:
                return True
        time.sleep(0.1)
    return False

def kill_existing_server(port):
    # Try to kill any process holding the port
    try:
        output = subprocess.check_output(['lsof', '-t', f'-i:{port}']).decode().strip()
        if output:
            for pid in output.split('\n'):
                os.system(f'kill -9 {pid}')
            time.sleep(0.5)
    except Exception:
        pass

def test_stress_test_script_exists():
    assert os.path.isfile('/home/user/stress_test.py'), "/home/user/stress_test.py script is missing."

def test_performance_and_output():
    script_path = '/home/user/stress_test.py'
    assert os.path.isfile(script_path), f"{script_path} does not exist"

    kill_existing_server(8025)

    # Start the server
    server_proc = subprocess.Popen(
        ['python3', '/app/run_server.py'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    try:
        assert wait_for_port(8025, timeout=5.0), "Server did not start on port 8025"

        # Run the stress test script
        start_time = time.time()
        res = subprocess.run(
            ['python3', script_path],
            capture_output=True,
            text=True
        )
        actual_duration = time.time() - start_time

        assert res.returncode == 0, f"Stress test script failed with return code {res.returncode}. Stderr: {res.stderr}"

        # Parse the output
        match = re.search(r'Total time:\s*([0-9.]+)\s*seconds', res.stdout, re.IGNORECASE)
        assert match is not None, f"Could not find 'Total time: X.XXX seconds' in output. Output was: {res.stdout}"

        reported_time = float(match.group(1))

        # Check metrics
        assert reported_time < 2.0, f"Reported time {reported_time} is not < 2.0 seconds. The bug may not be fixed."
        assert actual_duration < 5.0, f"Actual execution time {actual_duration:.2f}s is too high. The bug may not be fixed."

    finally:
        server_proc.terminate()
        server_proc.wait(timeout=2.0)
        if server_proc.poll() is None:
            server_proc.kill()