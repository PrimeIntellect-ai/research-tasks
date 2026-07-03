# test_final_state.py

import os
import json

def test_run_test_script_exists_and_executable():
    """Verify that /home/user/run_test.sh exists and is executable."""
    script_path = "/home/user/run_test.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_success_json_exists_and_correct():
    """Verify that /home/user/success.json exists and contains the correct response."""
    json_path = "/home/user/success.json"
    assert os.path.isfile(json_path), f"Output file {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} does not contain valid JSON."

    assert "id" in data, f"Key 'id' missing in {json_path}."
    assert data["id"] == "task-999", f"Expected 'id' to be 'task-999', got '{data['id']}'."

    assert "status" in data, f"Key 'status' missing in {json_path}."
    assert data["status"] == "CREATED_V2", f"Expected 'status' to be 'CREATED_V2', got '{data['status']}'."