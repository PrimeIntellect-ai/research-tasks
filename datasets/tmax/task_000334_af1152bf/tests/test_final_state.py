# test_final_state.py

import os
import json
import subprocess
import pytest

CONFIG_PATH = "/home/user/app_restore/config.ini"
JSON_PATH = "/home/user/restore_status.json"
DATA_DIR = "/home/user/app_restore/data/"

def test_config_ini_updated():
    assert os.path.isfile(CONFIG_PATH), f"File {CONFIG_PATH} does not exist."

    with open(CONFIG_PATH, "r") as f:
        content = f.read()

    assert "AllowAutomatedRestore=true" in content, "config.ini missing 'AllowAutomatedRestore=true'."
    assert "Timezone=UTC" in content, "config.ini missing 'Timezone=UTC'."
    assert "AllowAutomatedRestore=false" not in content, "config.ini still contains 'AllowAutomatedRestore=false'."
    assert "Timezone=America/New_York" not in content, "config.ini still contains 'Timezone=America/New_York'."

def test_restore_status_json_exists_and_valid():
    assert os.path.isfile(JSON_PATH), f"File {JSON_PATH} does not exist."

    with open(JSON_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} is not valid JSON.")

    assert "status" in data, "JSON missing 'status' key."
    assert data["status"] == "ready", f"Expected status 'ready', got '{data['status']}'."

    assert "timezone" in data, "JSON missing 'timezone' key."
    assert data["timezone"] == "UTC", f"Expected timezone 'UTC', got '{data['timezone']}'."

    assert "data_size_bytes" in data, "JSON missing 'data_size_bytes' key."
    assert isinstance(data["data_size_bytes"], int), "'data_size_bytes' must be an integer."

def test_restore_status_data_size():
    assert os.path.isdir(DATA_DIR), f"Directory {DATA_DIR} does not exist."

    # Calculate expected size dynamically
    cmd = f"du -sb {DATA_DIR} | awk '{{print $1}}'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    expected_size = int(result.stdout.strip())

    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    actual_size = data["data_size_bytes"]
    assert actual_size == expected_size, f"Expected data_size_bytes {expected_size}, got {actual_size}."