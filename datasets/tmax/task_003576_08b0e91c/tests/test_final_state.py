# test_final_state.py

import os
import stat
import subprocess
import re

def test_critical_dates_extracted():
    log_path = "/home/user/old_crash.log"
    out_path = "/home/user/critical_dates.txt"

    assert os.path.isfile(log_path), f"Source log file {log_path} is missing."
    assert os.path.isfile(out_path), f"Output file {out_path} is missing."

    expected_dates = []
    with open(log_path, "r") as f:
        for line in f:
            if "[CRITICAL FATAL ERROR]" in line:
                # Extract the first token (timestamp)
                parts = line.split()
                if parts:
                    expected_dates.append(parts[0])

    with open(out_path, "r") as f:
        actual_dates = [line.strip() for line in f if line.strip()]

    assert actual_dates == expected_dates, (
        f"Contents of {out_path} do not match expected timestamps. "
        f"Expected {expected_dates}, got {actual_dates}."
    )

def test_deploy_git_is_bare_repo():
    repo_path = "/home/user/deploy.git"
    assert os.path.isdir(repo_path), f"Deploy repository {repo_path} does not exist."

    # Check if it's a bare repository
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "rev-parse", "--is-bare-repository"],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        assert result.stdout.strip() == "true", f"{repo_path} is not a bare git repository."
    except subprocess.CalledProcessError:
        raise AssertionError(f"Failed to verify if {repo_path} is a bare git repository.")

def test_post_receive_hook_executable():
    hook_path = "/home/user/deploy.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Hook file {hook_path} does not exist."

    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Hook file {hook_path} is not executable."

def test_daemon_repo_remote_configured():
    repo_path = "/home/user/daemon_repo"
    try:
        result = subprocess.run(
            ["git", "-C", repo_path, "remote", "-v"],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        remotes = result.stdout
        assert "deploy" in remotes and "/home/user/deploy.git" in remotes, (
            "The 'deploy' remote is not correctly configured in /home/user/daemon_repo."
        )
    except subprocess.CalledProcessError:
        raise AssertionError(f"Failed to check git remotes in {repo_path}.")

def test_daemon_build_directory_and_executable():
    build_dir = "/home/user/daemon_build"
    daemon_exec = os.path.join(build_dir, "daemon")

    assert os.path.isdir(build_dir), f"Build directory {build_dir} does not exist."
    assert os.path.isfile(daemon_exec), f"Compiled daemon executable {daemon_exec} does not exist."

    st = os.stat(daemon_exec)
    assert bool(st.st_mode & stat.S_IXUSR), f"Daemon file {daemon_exec} is not executable."

def test_daemon_pid_file():
    pid_file = "/home/user/daemon.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist. The daemon may not have started successfully."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid numeric PID (found: {pid_str})."

    pid = int(pid_str)
    assert pid > 0, f"PID {pid} is invalid."

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        raise AssertionError(f"Process with PID {pid} from {pid_file} is not running.")

def test_daemon_log_file():
    log_file = "/home/user/daemon.log"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist. The daemon may not have started successfully."

    with open(log_file, "r") as f:
        content = f.read().strip()
    assert len(content) > 0, f"Log file {log_file} is empty."