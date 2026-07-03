# test_final_state.py

import os
import pytest

def test_daemon_running():
    """Check that the daemon PID is saved and the process is running."""
    pid_file = "/home/user/watcher.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} does not exist."

    with open(pid_file, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid integer PID."
    pid = int(pid_str)

    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} (from {pid_file}) is not running.")

def test_deployment_network_conf():
    """Check the final deployment config file."""
    conf_file = "/home/user/deployment_network.conf"
    assert os.path.isfile(conf_file), f"Config file {conf_file} does not exist."

    with open(conf_file, "r") as f:
        content = f.read()

    expected_lines = [
        "ACTIVE_DIR=/home/user/active_deployment",
        "LAST_DEPLOYED=build_beta.tar",
        "STATUS=live"
    ]

    for line in expected_lines:
        assert line in content, f"Expected line '{line}' not found in {conf_file}."

def test_active_deployment_content():
    """Check that the active deployment contains the final build."""
    index_file = "/home/user/active_deployment/index.html"
    assert os.path.isfile(index_file), f"Deployed file {index_file} does not exist."

    with open(index_file, "r") as f:
        content = f.read().strip()

    assert content == "Build Version Beta", f"Expected 'Build Version Beta' in {index_file}, found '{content}'."

def test_ci_builds_empty():
    """Check that the ci_builds directory is clean."""
    ci_builds_dir = "/home/user/ci_builds"
    assert os.path.isdir(ci_builds_dir), f"Directory {ci_builds_dir} does not exist."

    contents = os.listdir(ci_builds_dir)
    assert len(contents) == 0, f"Directory {ci_builds_dir} is not empty. Found: {contents}."