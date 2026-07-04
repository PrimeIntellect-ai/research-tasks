# test_final_state.py

import os
import subprocess
import time
import tempfile
import pytest

def test_git_repo_and_hook():
    repo_path = "/home/user/iot-hub.git"
    assert os.path.isdir(repo_path), f"Bare repo directory {repo_path} is missing."

    # Check if it is a bare repository
    out = subprocess.run(
        ["git", "-C", repo_path, "rev-parse", "--is-bare-repository"], 
        capture_output=True, text=True
    )
    assert out.stdout.strip() == "true", f"{repo_path} is not a bare Git repository."

    hook_path = os.path.join(repo_path, "hooks", "post-receive")
    assert os.path.isfile(hook_path), f"Hook file {hook_path} is missing."
    assert os.access(hook_path, os.X_OK), f"Hook file {hook_path} is not executable."

def test_push_and_daemon_behavior():
    repo_path = "/home/user/iot-hub.git"
    tz_content = "Pacific/Fiji"

    with tempfile.TemporaryDirectory() as tmpdir:
        clone_path = os.path.join(tmpdir, "test-clone")
        # Clone the bare repo
        res = subprocess.run(["git", "clone", repo_path, clone_path], capture_output=True, text=True)
        assert res.returncode == 0, f"Failed to clone repository: {res.stderr}"

        # Configure git 
        subprocess.run(["git", "-C", clone_path, "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", clone_path, "config", "user.name", "Test User"], check=True)
        subprocess.run(["git", "-C", clone_path, "checkout", "-b", "master"], capture_output=True)

        # Create TIMEZONE file
        tz_file = os.path.join(clone_path, "TIMEZONE")
        with open(tz_file, "w") as f:
            f.write(tz_content)

        subprocess.run(["git", "-C", clone_path, "add", "TIMEZONE"], check=True)
        subprocess.run(["git", "-C", clone_path, "commit", "-m", "Add TIMEZONE"], check=True)

        # Push to master
        res = subprocess.run(
            ["git", "-C", clone_path, "push", "origin", "master"], 
            capture_output=True, text=True
        )
        assert res.returncode == 0, f"Git push failed. Ensure the hook doesn't crash. Error: {res.stderr}"

    # Give the hook and daemon time to process
    time.sleep(3)

    # Check if files were checked out
    active_tz_file = "/home/user/iot-active/TIMEZONE"
    assert os.path.isfile(active_tz_file), f"Checked out file {active_tz_file} is missing."

    with open(active_tz_file, "r") as f:
        assert f.read().strip() == tz_content, f"Content of {active_tz_file} is incorrect."

    # Check if exactly one edge-daemon is running
    try:
        pgrep_out = subprocess.check_output(["pgrep", "-f", "edge-daemon"], text=True)
    except subprocess.CalledProcessError:
        pgrep_out = ""

    pids = [pid for pid in pgrep_out.strip().split() if pid]
    assert len(pids) == 1, f"Expected exactly 1 edge-daemon process running, found {len(pids)}."

    pid = pids[0]

    # Check the environment variables of the running process
    environ_path = f"/proc/{pid}/environ"
    assert os.path.exists(environ_path), f"Process environment file {environ_path} does not exist."

    with open(environ_path, "rb") as f:
        env_data = f.read().split(b'\0')

    tz_env = [e.decode('utf-8') for e in env_data if e.startswith(b"TZ=")]
    assert len(tz_env) == 1, "TZ environment variable not found in the new edge-daemon process."
    assert tz_env[0] == f"TZ={tz_content}", f"Incorrect TZ env var in daemon process: {tz_env[0]}"

    # Check the log file for the correct timezone output
    log_file = "/home/user/daemon-status.log"
    assert os.path.isfile(log_file), f"Log file {log_file} is missing."

    with open(log_file, "r") as f:
        log_content = f.read()

    assert tz_content in log_content, f"Log file {log_file} does not contain the expected timezone {tz_content}."