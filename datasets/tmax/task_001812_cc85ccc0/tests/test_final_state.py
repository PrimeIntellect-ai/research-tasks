# test_final_state.py

import os
import json

def test_symlink_structure():
    """Check if the symlink /home/user/app/data exists and points to /home/user/data_mount/active."""
    link_path = '/home/user/app/data'
    target_path = '/home/user/data_mount/active'

    assert os.path.islink(link_path), f"CRITICAL: {link_path} is not a symlink or does not exist."
    assert os.readlink(link_path) == target_path, f"CRITICAL: Symlink {link_path} does not point to {target_path}."
    assert os.path.isdir(target_path), f"CRITICAL: Target directory {target_path} does not exist."

def test_config_file():
    """Check if /home/user/config/containers.json exists and contains the correct JSON structure."""
    config_path = '/home/user/config/containers.json'

    assert os.path.isfile(config_path), f"CRITICAL: Configuration file {config_path} does not exist."

    with open(config_path, 'r') as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            assert False, f"CRITICAL: {config_path} does not contain valid JSON."

    assert "ingest-worker" in config, f"CRITICAL: Key 'ingest-worker' missing in {config_path}."
    assert isinstance(config["ingest-worker"], dict), f"CRITICAL: 'ingest-worker' is not a JSON object."
    assert config["ingest-worker"].get("status") == "running", f"CRITICAL: 'ingest-worker' status is not 'running'."

def test_success_log():
    """Check if /home/user/app/success.log exists and contains the exact string 'SERVICE_STARTED_SUCCESSFULLY'."""
    log_path = '/home/user/app/success.log'

    assert os.path.isfile(log_path), f"CRITICAL: Success log {log_path} does not exist. The service may not have run successfully."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert content == "SERVICE_STARTED_SUCCESSFULLY", f"CRITICAL: {log_path} content is incorrect. Expected 'SERVICE_STARTED_SUCCESSFULLY', got '{content}'."