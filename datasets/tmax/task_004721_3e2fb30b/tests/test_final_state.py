# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_agent_running():
    """Verify that the sensor-agent is running and its PID is recorded."""
    pid_file = "/home/user/sensor.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"Content of {pid_file} is not a valid PID: '{pid_str}'"

    try:
        with open(f"/proc/{pid_str}/comm", "r") as f:
            comm = f.read().strip()
        assert comm == "sensor-agent", f"Process {pid_str} is running but named '{comm}', expected 'sensor-agent'."
    except FileNotFoundError:
        pytest.fail(f"Process with PID {pid_str} (from {pid_file}) is not running.")

def test_setup_script():
    """Verify the setup script creates the directory with correct permissions and ACLs."""
    script_path = "/home/user/setup_env.sh"
    assert os.path.isfile(script_path), f"Setup script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Setup script {script_path} is not executable."

    # Execute the script to ensure idempotency and that it sets up the environment correctly
    res = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert res.returncode == 0, f"setup_env.sh failed with return code {res.returncode}.\nStderr: {res.stderr}"

    data_dir = "/home/user/sensor_data"
    assert os.path.isdir(data_dir), f"Data directory {data_dir} was not created."

    # Check base permissions (750)
    st = os.stat(data_dir)
    perms = stat.S_IMODE(st.st_mode) & 0o777
    assert perms == 0o750, f"Permissions of {data_dir} are {oct(perms)}, expected 0o750."

    # Check ACL for user 'nobody'
    acl_res = subprocess.run(["getfacl", data_dir], capture_output=True, text=True)
    assert acl_res.returncode == 0, "Failed to run getfacl."
    assert "user:nobody:r-x" in acl_res.stdout, f"ACL for 'nobody' is not 'r-x'. getfacl output:\n{acl_res.stdout}"

def test_filter_executable_exists():
    """Verify the filter C program was compiled successfully."""
    filter_path = "/home/user/filter"
    assert os.path.isfile(filter_path), f"Compiled filter {filter_path} does not exist."
    assert os.access(filter_path, os.X_OK), f"Filter {filter_path} is not executable."

def test_filter_evil_corpus():
    """Verify the filter rejects all lines containing restricted patterns."""
    filter_path = "/home/user/filter"
    evil_path = "/app/corpus/evil.txt"
    assert os.path.isfile(evil_path), f"Evil corpus {evil_path} is missing."

    with open(evil_path, "r") as f:
        evil_lines = f.readlines()

    bypassed = []
    for i, line in enumerate(evil_lines):
        res = subprocess.run([filter_path], input=line, capture_output=True, text=True)
        if res.stdout != "":
            bypassed.append(f"Line {i+1}: {line.strip()}")

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_lines)} evil lines bypassed the filter. Examples: {bypassed[:5]}")

def test_filter_clean_corpus():
    """Verify the filter preserves all clean lines unchanged."""
    filter_path = "/home/user/filter"
    clean_path = "/app/corpus/clean.txt"
    assert os.path.isfile(clean_path), f"Clean corpus {clean_path} is missing."

    with open(clean_path, "r") as f:
        clean_lines = f.readlines()

    modified = []
    for i, line in enumerate(clean_lines):
        res = subprocess.run([filter_path], input=line, capture_output=True, text=True)
        if res.stdout != line:
            modified.append(f"Line {i+1}: expected {repr(line)}, got {repr(res.stdout)}")

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_lines)} clean lines modified by the filter. Examples: {modified[:5]}")