# test_final_state.py

import os
import stat
import subprocess
import time
import pytest

def test_investigation_report_contents():
    report_path = "/home/user/investigation_report.txt"
    assert os.path.isfile(report_path), f"Investigation report missing: {report_path}"

    with open(report_path, "r") as f:
        content = f.read()

    assert "LEAKING_VARIABLE: ORPHANED_PAYLOADS" in content, "Incorrect or missing LEAKING_VARIABLE in report."
    assert "FIRST_LEAK_TRACE_ID: TRC-88392" in content, "Incorrect or missing FIRST_LEAK_TRACE_ID in report."

def test_verify_fix_script_exists_and_executable():
    script_path = "/home/user/app/verify_fix.sh"
    assert os.path.isfile(script_path), f"Verification script missing: {script_path}"

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Verification script is not executable: {script_path}"

def test_verify_fix_script_execution():
    script_path = "/home/user/app/verify_fix.sh"

    # Run the user's verify_fix.sh script
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"verify_fix.sh failed with exit code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_sensor_aggregator_no_leak():
    script_path = "/home/user/app/sensor_aggregator.sh"
    pipe_path = "/home/user/app/sensor_pipe"

    if not os.path.exists(pipe_path):
        os.mkfifo(pipe_path)

    proc = subprocess.Popen(["bash", script_path])

    try:
        # Open pipe for writing
        pipe_fd = os.open(pipe_path, os.O_WRONLY)

        # Write 5000 lines of orphan payloads
        for i in range(5000):
            line = f"TYPE:ORPHAN TRACE_ID:TRC-88392 PAYLOAD:DROPPED_PRECISION_DATA_POINT_{i:05d}\n"
            os.write(pipe_fd, line.encode('utf-8'))

        # Give it a moment to process
        time.sleep(1)

        # Check RSS memory
        ps_result = subprocess.run(["ps", "-o", "rss=", "-p", str(proc.pid)], capture_output=True, text=True)
        rss_str = ps_result.stdout.strip()

        if rss_str.isdigit():
            rss_kb = int(rss_str)
            assert rss_kb < 10240, f"Memory leak still present! RSS memory is {rss_kb} KB (>= 10MB) after processing 5000 lines."

        os.close(pipe_fd)
    finally:
        proc.terminate()
        proc.wait(timeout=2)