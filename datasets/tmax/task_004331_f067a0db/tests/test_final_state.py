# test_final_state.py

import os
import time
import subprocess
import pytest

def test_metrics_threshold():
    """Verify that the Rust monitor optimized parsing time is under the 150ms threshold."""
    metrics_file = "/home/user/app/metrics.txt"
    assert os.path.exists(metrics_file), f"Metrics file {metrics_file} not found. Did the Rust monitor run and output its benchmark?"

    with open(metrics_file, "r") as f:
        content = f.read().strip()

    try:
        time_ms = int(content)
    except ValueError:
        pytest.fail(f"Metrics file does not contain a valid integer: '{content}'")

    assert time_ms <= 150, f"FAIL: Parsing took {time_ms}ms, threshold is 150ms."

def test_logrotate_config():
    """Verify the logrotate configuration meets the specified requirements."""
    config_file = "/home/user/app/logrotate.conf"
    assert os.path.exists(config_file), f"logrotate configuration {config_file} not found."

    with open(config_file, "r") as f:
        content = f.read()

    assert "daily" in content, "logrotate config missing 'daily' rotation."
    assert "rotate 7" in content, "logrotate config missing 'rotate 7'."
    assert "compress" in content, "logrotate config missing 'compress'."
    assert "create 0644" in content or "create 644" in content, "logrotate config missing 'create 0644'."

def test_supervisord_config():
    """Verify supervisord configuration exists."""
    config_file = "/home/user/app/supervisord.conf"
    assert os.path.exists(config_file), f"supervisord configuration {config_file} not found."

def test_end_to_end_alerting():
    """Verify the end-to-end flow: appending an error log triggers an alert commit to the Git repository."""
    # Ensure supervisord is running with the user's config
    subprocess.run(["supervisord", "-c", "/home/user/app/supervisord.conf"], capture_output=True)

    # Give services a moment to start and initialize
    time.sleep(3)

    log_file = "/home/user/app/logs/access.log"
    test_message = "ERROR: Verifier test failure"

    # Append the test error line
    with open(log_file, "a") as f:
        f.write(f"{test_message}\n")

    # Wait for the Rust monitor to tail the log, send the alert, and Git auditor to commit
    time.sleep(3)

    git_dir = "/home/user/git/alerts.git"
    try:
        out = subprocess.check_output(["git", "log", "-1", "--pretty=%B"], cwd=git_dir, stderr=subprocess.STDOUT)
        commit_msg = out.decode('utf-8')
        assert test_message in commit_msg, f"Expected '{test_message}' in latest commit message, got: {commit_msg}"
    except subprocess.CalledProcessError as e:
        output = e.output.decode('utf-8') if e.output else str(e)
        pytest.fail(f"Git auditor did not commit the alert. Failed to retrieve git log or no commits exist. Git output: {output}")