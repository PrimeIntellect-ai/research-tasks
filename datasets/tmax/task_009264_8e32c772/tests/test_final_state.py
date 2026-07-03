# test_final_state.py
import os
import stat
import subprocess
import pytest

def test_git_commit_message():
    result = subprocess.run(
        ["git", "-C", "/home/user/repo", "log", "-1", "--pretty=%B"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, "Failed to execute git log."
    assert "Fix PID directory" in result.stdout.strip(), "The latest commit message does not contain 'Fix PID directory'."

def test_run_directory_exists_and_permissions():
    run_dir = "/home/user/run"
    assert os.path.isdir(run_dir), f"Directory {run_dir} does not exist."
    st = os.stat(run_dir)
    # Check if permissions are 0755 (owner rwx, group rx, others rx)
    assert stat.S_IMODE(st.st_mode) == 0o755, f"Permissions of {run_dir} are not 0755."

def test_server_pid_file_exists_and_valid():
    pid_file = "/home/user/run/server.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist."
    with open(pid_file, "r") as f:
        content = f.read().strip()
    assert content.isdigit(), f"PID file {pid_file} does not contain a valid numeric PID."

def test_solution_txt_matches_pid():
    pid_file = "/home/user/run/server.pid"
    solution_file = "/home/user/solution.txt"
    assert os.path.isfile(solution_file), f"Solution file {solution_file} does not exist."

    with open(pid_file, "r") as f:
        expected_pid = f.read().strip()

    with open(solution_file, "r") as f:
        actual_pid = f.read().strip()

    assert actual_pid == expected_pid, f"Solution file contains '{actual_pid}', but expected '{expected_pid}' from {pid_file}."

def test_server_process_running():
    # pgrep -f "/home/user/repo/server"
    result = subprocess.run(
        ["pgrep", "-f", "^/home/user/repo/server$"],
        capture_output=True, text=True
    )
    # Alternatively, just check if the PID from the file is running
    pid_file = "/home/user/run/server.pid"
    if os.path.isfile(pid_file):
        with open(pid_file, "r") as f:
            pid = f.read().strip()
        if pid.isdigit():
            # Check if this specific PID is running and is the server
            assert os.path.isdir(f"/proc/{pid}"), f"Process with PID {pid} is not running."
            with open(f"/proc/{pid}/cmdline", "r") as f:
                cmdline = f.read().replace('\x00', ' ').strip()
            assert "/home/user/repo/server" in cmdline, f"Process {pid} is not the server. Cmdline: {cmdline}"
    else:
        pytest.fail("Cannot verify running process because PID file is missing.")