# test_final_state.py

import os
import pytest

def test_deploy_log_contents():
    log_path = "/home/user/workspace/deploy.log"
    assert os.path.isfile(log_path), f"Deployment log {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    assert "node_1: SUCCESS" in content, "Expected 'node_1: SUCCESS' in deploy.log"
    assert "node_2: ROLLBACK" in content, "Expected 'node_2: ROLLBACK' in deploy.log"
    assert "node_3: SUCCESS" in content, "Expected 'node_3: SUCCESS' in deploy.log"

def test_symlink_states():
    # node_1 and node_3 should point to v2, node_2 should point to v1
    expected_targets = {
        1: "versions/v2",
        2: "versions/v1",
        3: "versions/v2"
    }

    for i in range(1, 4):
        symlink_path = f"/home/user/edge_fleet/node_{i}/current"
        assert os.path.islink(symlink_path), f"{symlink_path} is missing or not a symlink"

        target = os.readlink(symlink_path)
        # Handle both absolute and relative symlinks
        if not os.path.isabs(target):
            # If relative, it should end with the expected target
            assert target.endswith(expected_targets[i]), f"Symlink {symlink_path} points to {target}, expected it to point to {expected_targets[i]}"
        else:
            expected_abs = f"/home/user/edge_fleet/node_{i}/{expected_targets[i]}"
            assert target == expected_abs, f"Symlink {symlink_path} points to {target}, expected {expected_abs}"

def test_status_logs():
    expected_status = {
        1: "STATUS: UP",
        2: "STATUS: DOWN",
        3: "STATUS: UP"
    }

    for i in range(1, 4):
        log_path = f"/home/user/edge_fleet/node_{i}/status.log"
        assert os.path.isfile(log_path), f"Status log {log_path} is missing."

        with open(log_path, "r") as f:
            content = f.read().strip()

        assert content == expected_status[i], f"Expected '{expected_status[i]}' in {log_path}, got '{content}'"

def test_v2_directories_exist():
    for i in range(1, 4):
        v2_dir = f"/home/user/edge_fleet/node_{i}/versions/v2"
        assert os.path.isdir(v2_dir), f"Directory {v2_dir} was not created."

        monitor_binary = os.path.join(v2_dir, "monitor")
        assert os.path.isfile(monitor_binary), f"Monitor binary {monitor_binary} is missing."
        assert os.access(monitor_binary, os.X_OK), f"Monitor binary {monitor_binary} is not executable."