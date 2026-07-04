# test_final_state.py

import os
import stat
import pytest

def test_failed_servers_txt():
    path = '/home/user/failed_servers.txt'
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "server-cache-01,10.0.0.8",
        "server-db-02,10.0.0.12"
    ]

    assert lines == expected_lines, f"Contents of {path} do not match the expected output. Got: {lines}"

def test_supervisor_log():
    path = '/home/user/supervisor.log'
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "[WARN] Agent crashed, restarting",
        "[WARN] Agent crashed, restarting",
        "[INFO] Agent succeeded"
    ]

    assert lines == expected_lines, f"Contents of {path} do not match the expected output. Got: {lines}"

def test_pipeline_result():
    path = '/home/user/pipeline_result.txt'
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == "PIPELINE SUCCESS", f"Contents of {path} should be exactly 'PIPELINE SUCCESS'. Got: '{content}'"

def test_tunnel_cleanup():
    pid_file = '/home/user/tunnel.pid'
    assert os.path.isfile(pid_file), f"File {pid_file} is missing. The tunnel.sh script should have created it."

    with open(pid_file, 'r') as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"Contents of {pid_file} must be a valid PID. Got: '{pid_str}'"

    pid = int(pid_str)

    # Check if process is still running
    # On Linux, we can check if /proc/<pid> exists
    proc_dir = f"/proc/{pid}"

    # If the process is still running, we should check if it's socat to be sure
    if os.path.isdir(proc_dir):
        try:
            with open(os.path.join(proc_dir, "comm"), "r") as f:
                comm = f.read().strip()
            assert comm != "socat", f"The socat process (PID {pid}) is still running. The pipeline should have terminated it."
        except FileNotFoundError:
            # Process died between isdir check and opening comm file
            pass

def test_scripts_exist_and_executable():
    scripts = [
        '/home/user/analyze.sh',
        '/home/user/supervisor.sh',
        '/home/user/tunnel.sh',
        '/home/user/pipeline.sh'
    ]

    for script in scripts:
        assert os.path.isfile(script), f"Script {script} is missing."
        st = os.stat(script)
        assert bool(st.st_mode & stat.S_IXUSR), f"Script {script} is not executable."