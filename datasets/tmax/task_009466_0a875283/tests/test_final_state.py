# test_final_state.py
import os
import stat
import re

def test_extraction_and_permissions():
    restored_dir = "/home/user/restored_app"
    assert os.path.isdir(restored_dir), f"Directory {restored_dir} does not exist."

    expected_files = [".env", "restore_data.log", "server.py"]
    for f in expected_files:
        file_path = os.path.join(restored_dir, f)
        assert os.path.isfile(file_path), f"File {file_path} is missing."

    env_path = os.path.join(restored_dir, ".env")
    mode = os.stat(env_path).st_mode
    permissions = stat.S_IMODE(mode)
    assert permissions == 0o600, f"Permissions for {env_path} are {oct(permissions)}, expected 0o600."

def test_corrupt_count():
    count_file = "/home/user/corrupt_count.txt"
    assert os.path.isfile(count_file), f"File {count_file} does not exist."

    with open(count_file, "r") as f:
        content = f.read().strip()

    assert content == "3", f"Expected count to be '3', but got '{content}'."

def test_supervise_script():
    script_file = "/home/user/supervise.sh"
    assert os.path.isfile(script_file), f"Script {script_file} does not exist."

    with open(script_file, "r") as f:
        content = f.read()

    assert "while" in content or "until" in content, f"Script {script_file} does not appear to contain a loop."
    assert "server.py" in content, f"Script {script_file} does not reference server.py."

def test_supervisor_running():
    pid_file = "/home/user/supervisor.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid integer."
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        assert False, f"Process with PID {pid} is not running."

    # Check process command line if possible
    cmdline_file = f"/proc/{pid}/cmdline"
    if os.path.isfile(cmdline_file):
        with open(cmdline_file, "r") as f:
            cmdline = f.read().replace('\x00', ' ')
        assert "supervise.sh" in cmdline or "bash" in cmdline or "sh" in cmdline, \
            f"Process {pid} does not seem to be running the supervise script. Cmdline: {cmdline}"