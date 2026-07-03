# test_final_state.py

import os
import json
import time
import pytest

SCRIPT_PATH = "/home/user/sync_projects.sh"
MASTER_INDEX = "/home/user/master_index.json"
DROPZONE = "/home/user/dropzone"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_uses_atomic_mv():
    with open(SCRIPT_PATH, 'r') as f:
        content = f.read()
    assert "mv " in content and "master_index.json" in content, "Script does not appear to use atomic 'mv' to update master_index.json."

def test_initial_master_index():
    assert os.path.isfile(MASTER_INDEX), f"{MASTER_INDEX} does not exist. The script might not have run the initial scan."
    with open(MASTER_INDEX, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{MASTER_INDEX} is not valid JSON.")

    assert data.get("Apollo") == "active", "Initial scan missing or incorrect 'Apollo' project from JSON file."
    assert data.get("Gemini") == "archived", "Initial scan missing or incorrect 'Gemini' project from CSV file."

def test_dropzone_update():
    # Verify initial state before dropping
    assert os.path.isdir(DROPZONE), f"Dropzone directory {DROPZONE} missing."

    # Drop a new file
    new_file_path = os.path.join(DROPZONE, "new_proj.json")
    new_data = {"id": 103, "project_name": "Orion", "status": "planning"}
    with open(new_file_path, 'w') as f:
        json.dump(new_data, f)

    # Wait for the background script and inotifywait to trigger and process
    time.sleep(3)

    assert os.path.isfile(MASTER_INDEX), f"{MASTER_INDEX} does not exist after dropping new file."
    with open(MASTER_INDEX, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{MASTER_INDEX} is not valid JSON after update.")

    assert data.get("Orion") == "planning", "Dropzone file was not processed or master index not updated with 'Orion'."
    assert data.get("Apollo") == "active", "'Apollo' project was lost after dropzone update."
    assert data.get("Gemini") == "archived", "'Gemini' project was lost after dropzone update."