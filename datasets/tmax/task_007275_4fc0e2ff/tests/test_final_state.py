# test_final_state.py

import os
import subprocess
import re

def test_socat_port_forwarding():
    pid_file = "/home/user/port_forward.pid"
    assert os.path.exists(pid_file), f"Fail: {pid_file} does not exist."

    with open(pid_file, "r") as f:
        pid = f.read().strip()

    assert pid.isdigit(), f"Fail: PID in {pid_file} is not a valid integer."

    # Check if process is running
    try:
        # ps -p PID -o args=
        result = subprocess.run(
            ["ps", "-p", pid, "-o", "args="],
            capture_output=True,
            text=True,
            check=True
        )
        cmdline = result.stdout.strip()
    except subprocess.CalledProcessError:
        assert False, f"Fail: Process {pid} is not running."

    assert "socat" in cmdline, f"Fail: Process {pid} is not socat. Command line: {cmdline}"
    assert "8080" in cmdline and "9090" in cmdline, f"Fail: socat is not configured with the correct ports (8080 -> 9090). Command line: {cmdline}"

def test_git_commit_and_push():
    source_dir = "/home/user/source"

    # Check latest commit message
    result = subprocess.run(
        ["git", "log", "-1", "--pretty=%B"],
        cwd=source_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Fail: Could not get git log."
    latest_msg = result.stdout.strip()
    assert latest_msg == "Trigger rollout", f"Fail: The latest commit message is not 'Trigger rollout'. Found: '{latest_msg}'"

    # Check if pushed to origin
    # We can check if the local HEAD matches the origin/main or just check the bare repo
    bare_repo = "/home/user/app.git"
    result_bare = subprocess.run(
        ["git", "rev-parse", "main"],
        cwd=bare_repo,
        capture_output=True,
        text=True
    )
    assert result_bare.returncode == 0, "Fail: 'main' branch not found in bare repository. Push may have failed."
    bare_hash = result_bare.stdout.strip()

    result_local = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=source_dir,
        capture_output=True,
        text=True
    )
    local_hash = result_local.stdout.strip()

    assert bare_hash == local_hash, "Fail: The latest commit in source was not pushed to app.git."

def test_email_notification_file():
    source_dir = "/home/user/source"
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=source_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Fail: Could not get git HEAD hash."
    latest_hash = result.stdout.strip()

    eml_file = f"/home/user/mail/deployed_{latest_hash}.eml"
    assert os.path.exists(eml_file), f"Fail: Expected notification file {eml_file} does not exist. Hook or Go script may have failed."

    expected_content = f"To: dev@local\nSubject: Update rolled out\n\nCommit: {latest_hash}"

    with open(eml_file, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, f"Fail: File content does not match expected output.\nExpected:\n{expected_content}\nActual:\n{actual_content}"