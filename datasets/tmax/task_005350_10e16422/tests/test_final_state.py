# test_final_state.py

import os
import re
import socket
import subprocess
import pytest

def test_bare_repo_exists():
    """Verify that the bare repository exists and is properly initialized."""
    bare_repo_path = "/home/user/bare_repo.git"
    assert os.path.isdir(bare_repo_path), f"Bare repository directory {bare_repo_path} does not exist."
    assert os.path.isfile(os.path.join(bare_repo_path, "HEAD")), "Bare repository is missing HEAD file."
    assert os.path.isdir(os.path.join(bare_repo_path, "objects")), "Bare repository is missing objects directory."

def test_symlink_correct():
    """Verify that the symlink for the restore environment is correct."""
    symlink_path = "/home/user/restore_env/current_repo"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."
    target = os.readlink(symlink_path)
    assert target == "/home/user/bare_repo.git", f"Symlink points to {target} instead of /home/user/bare_repo.git"

def check_port_open(port):
    """Helper to check if a local port is listening."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def test_services_running():
    """Verify that git daemon and proxy PIDs exist and ports are listening."""
    daemon_pid_file = "/home/user/git_daemon.pid"
    proxy_pid_file = "/home/user/proxy.pid"

    assert os.path.isfile(daemon_pid_file), f"{daemon_pid_file} does not exist."
    assert os.path.isfile(proxy_pid_file), f"{proxy_pid_file} does not exist."

    assert check_port_open(9418), "Git daemon port 9418 is not listening on 127.0.0.1"
    assert check_port_open(8080), "Proxy port 8080 is not listening on 127.0.0.1"

def test_test_clone_and_file():
    """Verify that the test clone was successful and contains the correct file."""
    clone_path = "/home/user/test_clone"
    file_path = os.path.join(clone_path, "restore_verified.txt")

    assert os.path.isdir(os.path.join(clone_path, ".git")), f"{clone_path} is not a valid git repository."
    assert os.path.isfile(file_path), f"{file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()
    assert content == "RESTORE OK", f"File content is '{content}', expected 'RESTORE OK'."

def test_restore_log_format_and_content():
    """Verify that the restore log exists, has the correct format, and contains the correct commit hash."""
    log_file = "/home/user/restore_log.txt"
    assert os.path.isfile(log_file), f"{log_file} does not exist."

    with open(log_file, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) > 0, f"{log_file} is empty."
    last_line = lines[-1]

    # Check regex format
    match = re.match(r"^RESTORE_PUSH: ([0-9a-f]{40}) at \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$", last_line)
    assert match, f"Log line '{last_line}' does not match the required format."

    logged_hash = match.group(1)

    # Get the latest commit hash from the bare repo
    try:
        bare_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], 
            cwd="/home/user/bare_repo.git", 
            text=True
        ).strip()
    except subprocess.CalledProcessError:
        pytest.fail("Failed to get HEAD commit hash from the bare repository.")

    assert logged_hash == bare_hash, f"Logged commit hash {logged_hash} does not match bare repo HEAD {bare_hash}."