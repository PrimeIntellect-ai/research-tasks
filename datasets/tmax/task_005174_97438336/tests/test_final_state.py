# test_final_state.py

import os
import subprocess
import time
import signal
import re

PIPELINE_DIR = "/home/user/pipeline"
RESULT_FILE = os.path.join(PIPELINE_DIR, "result.txt")
SCRIPT_FILE = os.path.join(PIPELINE_DIR, "aggregate_metrics.sh")

def test_result_file_correct():
    """Verify that the result file contains the correct average with exactly 4 decimal places."""
    assert os.path.isfile(RESULT_FILE), f"Result file {RESULT_FILE} is missing. Did you run the script?"
    with open(RESULT_FILE, 'r') as f:
        content = f.read().strip()

    assert content == "30.5454", f"Expected average '30.5454', but got '{content}'. Check your precision and loop logic."

def test_script_fixes_shared_library():
    """Verify that the script fixes the shared library issue."""
    with open(SCRIPT_FILE, 'r') as f:
        script_content = f.read()

    # Check if LD_LIBRARY_PATH or similar is used
    has_ld_path = "LD_LIBRARY_PATH" in script_content
    has_ldconfig = "ldconfig" in script_content
    has_patchelf = "patchelf" in script_content
    has_cd = "cd " in script_content and "./metric_parser" in script_content

    assert has_ld_path or has_ldconfig or has_patchelf, "Could not find LD_LIBRARY_PATH or similar fix for the shared library in the script."

def test_script_trap_and_cleanup():
    """Verify that the script properly traps signals and cleans up background processes."""
    with open(SCRIPT_FILE, 'r') as f:
        script_content = f.read()

    assert "trap" in script_content, "No 'trap' command found in the script."
    assert "kill" in script_content, "No 'kill' command found in the script to terminate background processes."

    # Actually test the behavior
    # Start the script in a new session so we can send signals
    process = subprocess.Popen(
        ["bash", SCRIPT_FILE],
        cwd=PIPELINE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Give it a moment to spawn background processes
    time.sleep(1)

    # Get the process group ID
    pgid = os.getpgid(process.pid)

    # Send SIGTERM to the script
    os.kill(process.pid, signal.SIGTERM)

    # Wait for the script to exit
    process.wait(timeout=5)

    # Check if any sleep processes are left from this script
    # We can use ps to find any sleep 100 processes
    ps_output = subprocess.check_output(["ps", "-eo", "pid,ppid,cmd"]).decode('utf-8')
    leaked_sleeps = []
    for line in ps_output.splitlines():
        if "sleep 100" in line and not "grep" in line:
            parts = line.split()
            if len(parts) >= 3:
                leaked_sleeps.append(line)

    # We can't strictly assert no sleep 100 globally, but we can assume in this container environment
    # it's isolated. Alternatively, we check if the specific child processes were killed.
    # If the trap worked, there should be no sleep 100 processes running.
    assert len(leaked_sleeps) == 0, "Found leaked 'sleep 100' processes after sending SIGTERM to the script."