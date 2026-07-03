# test_final_state.py

import os
import time
import signal
import subprocess
import pytest

def test_organizer_throughput():
    script_path = "/home/user/organizer.py"
    master_log_path = "/home/user/master_log.txt"
    dropzone_path = "/home/user/dropzone"

    assert os.path.exists(script_path), f"Agent script not found at {script_path}"

    # Cleanup before test
    subprocess.run(["rm", "-rf", dropzone_path], check=False)
    subprocess.run(["rm", "-f", master_log_path], check=False)

    # Run the agent's script
    proc = subprocess.Popen(["python3", script_path])

    # Allow it to run for exactly 15 seconds
    time.sleep(15.0)

    # Gracefully terminate
    proc.send_signal(signal.SIGINT)
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=1)

    # Check the output
    count = 0
    if os.path.exists(master_log_path):
        with open(master_log_path, "r") as f:
            count = sum(1 for line in f if line.strip())

    assert count >= 200, f"Throughput too low: extracted {count} lines, expected >= 200"

    # Also verify that the log emitter process was terminated by the script
    # (or at least isn't running as a zombie if we can help it, but checking throughput is the main metric)

    # Cleanup after test
    subprocess.run(["pkill", "-f", "log_emitter"], check=False)