# test_final_state.py

import os
import stat
import socket
import subprocess
import time
import tempfile
import pytest

def test_dashboard_directory_exists():
    """Verify /home/user/dashboard/ exists."""
    assert os.path.isdir("/home/user/dashboard/"), "/home/user/dashboard/ directory does not exist."

def test_git_hook_functionality():
    """Verify the post-receive git hook works as expected."""
    repo_path = "/home/user/metrics-config.git"
    hook_path = os.path.join(repo_path, "hooks", "post-receive")

    assert os.path.isdir(repo_path), f"Bare git repository not found at {repo_path}"
    assert os.path.isfile(hook_path), f"Git hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"Git hook at {hook_path} is not executable"

    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize a temporary git repo, commit, and push
        subprocess.run(["git", "init"], cwd=tmpdir, check=True, capture_output=True)
        subprocess.run(["git", "remote", "add", "origin", repo_path], cwd=tmpdir, check=True, capture_output=True)

        test_file = os.path.join(tmpdir, "testfile.txt")
        with open(test_file, "w") as f:
            f.write("test commit")

        subprocess.run(["git", "add", "testfile.txt"], cwd=tmpdir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=tmpdir, check=True, capture_output=True)

        # We push to a unique branch to avoid conflicts if tests run multiple times
        branch_name = "test-branch-123"
        subprocess.run(["git", "checkout", "-b", branch_name], cwd=tmpdir, check=True, capture_output=True)
        push_result = subprocess.run(["git", "push", "origin", branch_name], cwd=tmpdir, capture_output=True)
        assert push_result.returncode == 0, f"Git push failed: {push_result.stderr.decode()}"

    events_log = "/home/user/dashboard/events.log"
    assert os.path.isfile(events_log), f"{events_log} was not created."

    with open(events_log, "r") as f:
        log_contents = f.read()

    expected_log = f'{{"type": "push", "ref": "refs/heads/{branch_name}"}}'
    assert expected_log in log_contents, f"Expected JSON log '{expected_log}' not found in {events_log}."

def test_smtp_daemon_functionality():
    """Verify the SMTP daemon listens on 8025 and extracts Subject lines."""
    # Send test message
    test_subject = "Critical System Alert Pytest"
    message = f"HELO localhost\r\nSubject: {test_subject}\r\nData\r\nQUIT\r\n"

    try:
        with socket.create_connection(("127.0.0.1", 8025), timeout=5) as s:
            s.sendall(message.encode('utf-8'))
    except ConnectionRefusedError:
        pytest.fail("Connection refused on 127.0.0.1:8025. Is smtp-alerter running?")

    time.sleep(1) # Allow daemon time to write

    alerts_log = "/home/user/dashboard/alerts.log"
    assert os.path.isfile(alerts_log), f"{alerts_log} was not created."

    with open(alerts_log, "r") as f:
        log_contents = f.read()

    assert test_subject in log_contents, f"Expected subject '{test_subject}' not found in {alerts_log}."

def test_monitor_script_and_cron():
    """Verify monitor.sh script and crontab configuration."""
    monitor_script = "/home/user/monitor.sh"
    assert os.path.isfile(monitor_script), f"{monitor_script} does not exist."
    assert os.access(monitor_script, os.X_OK), f"{monitor_script} is not executable."

    # Check crontab
    crontab_result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert crontab_result.returncode == 0, "Failed to read crontab."
    assert monitor_script in crontab_result.stdout, f"{monitor_script} not found in crontab."

    # Check if crontab is set to run every minute
    cron_lines = [line for line in crontab_result.stdout.splitlines() if monitor_script in line and not line.strip().startswith("#")]
    assert len(cron_lines) > 0, f"No active cron job found for {monitor_script}."

    cron_parts = cron_lines[0].split()
    assert cron_parts[:5] == ["*", "*", "*", "*", "*"], "Cron job is not configured to run every minute (* * * * *)."

def test_monitor_script_restarts_daemon():
    """Verify monitor.sh actually restarts the smtp-alerter daemon."""
    # Kill daemon if running
    subprocess.run(["pkill", "-f", "smtp-alerter"])
    time.sleep(1)

    # Ensure it's dead
    pgrep_result = subprocess.run(["pgrep", "-f", "smtp-alerter"], capture_output=True)
    assert pgrep_result.returncode != 0, "Failed to kill smtp-alerter for testing."

    # Run monitor script
    subprocess.run(["/home/user/monitor.sh"], check=True)
    time.sleep(2)

    # Ensure it's back
    pgrep_result = subprocess.run(["pgrep", "-f", "smtp-alerter"], capture_output=True)
    assert pgrep_result.returncode == 0, "monitor.sh failed to restart smtp-alerter."