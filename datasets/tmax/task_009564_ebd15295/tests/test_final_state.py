# test_final_state.py

import os
import json
import subprocess
import pytest

CONFIG_PATH = "/home/user/monitor_config.json"
BACKUP_PATH = "/home/user/monitor_config.json.bak"
SCRIPT_PATH = "/home/user/update_config.py"

def test_script_exists():
    """Test that the update_config.py script exists."""
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."

def test_backup_exists_and_correct():
    """Test that the backup file exists and contains the original configuration."""
    assert os.path.exists(BACKUP_PATH), f"Backup file {BACKUP_PATH} does not exist."

    with open(BACKUP_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Backup file {BACKUP_PATH} does not contain valid JSON.")

    expected_original = {
        "global_timeout": 30,
        "endpoints": [
            {
                "name": "db_service",
                "url": "http://localhost:5432/ping"
            }
        ]
    }

    assert data == expected_original, f"Backup file {BACKUP_PATH} does not match the original configuration."

def test_config_updated_correctly():
    """Test that the configuration file was updated correctly."""
    assert os.path.exists(CONFIG_PATH), f"Configuration file {CONFIG_PATH} does not exist."

    with open(CONFIG_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Configuration file {CONFIG_PATH} does not contain valid JSON.")

    expected_updated = {
        "global_timeout": 30,
        "endpoints": [
            {
                "name": "db_service",
                "url": "http://localhost:5432/ping"
            },
            {
                "name": "cache_service",
                "url": "http://localhost:8081/health"
            }
        ]
    }

    assert data == expected_updated, f"Configuration file {CONFIG_PATH} does not contain the expected updated state."

def test_idempotency():
    """Test that running the script again does not duplicate the endpoint."""
    # Run the script again
    result = subprocess.run(["python3", SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {SCRIPT_PATH} failed with error: {result.stderr}"

    # Check the config file again
    with open(CONFIG_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Configuration file {CONFIG_PATH} is no longer valid JSON after second run.")

    # Count how many times cache_service appears
    endpoints = data.get("endpoints", [])
    cache_endpoints = [ep for ep in endpoints if ep.get("name") == "cache_service"]

    assert len(cache_endpoints) == 1, "The script is not idempotent: 'cache_service' was added multiple times."