# test_final_state.py

import os
import json
import pytest

OUTPUT_PATH = "/home/user/incremental_patch.json"

def test_incremental_patch_exists():
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} does not exist. Did you run the program and redirect output?"

def test_incremental_patch_valid_json():
    assert os.path.isfile(OUTPUT_PATH), "Output file missing."
    try:
        with open(OUTPUT_PATH, "r") as f:
            json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"Output file {OUTPUT_PATH} does not contain valid JSON.")

def test_incremental_patch_server_json_diff():
    with open(OUTPUT_PATH, "r") as f:
        data = json.load(f)

    assert "server.json" in data, "Missing 'server.json' key in output JSON."
    server_diff = data["server.json"]

    assert server_diff.get("type") == "json", "server.json type should be 'json'"
    assert server_diff.get("added") == {"timeout": 30}, "server.json 'added' diff is incorrect."
    assert server_diff.get("removed") == {"protocol": "http"}, "server.json 'removed' diff is incorrect."
    assert server_diff.get("modified") == {"port": {"old": 8080, "new": 8081}}, "server.json 'modified' diff is incorrect."

def test_incremental_patch_users_csv_diff():
    with open(OUTPUT_PATH, "r") as f:
        data = json.load(f)

    assert "users.csv" in data, "Missing 'users.csv' key in output JSON."
    users_diff = data["users.csv"]

    assert users_diff.get("type") == "csv", "users.csv type should be 'csv'"

    added = users_diff.get("added", [])
    removed = users_diff.get("removed", [])

    assert isinstance(added, list), "users.csv 'added' should be a list"
    assert isinstance(removed, list), "users.csv 'removed' should be a list"

    expected_added = {"id": "3", "name": "alice", "role": "user"}
    expected_removed = {"id": "2", "name": "john", "role": "user"}

    assert expected_added in added, f"Expected {expected_added} in users.csv 'added' list."
    assert expected_removed in removed, f"Expected {expected_removed} in users.csv 'removed' list."

    # Also check exact lengths to ensure no extra rows are reported
    assert len(added) == 1, "users.csv 'added' list should contain exactly 1 item."
    assert len(removed) == 1, "users.csv 'removed' list should contain exactly 1 item."