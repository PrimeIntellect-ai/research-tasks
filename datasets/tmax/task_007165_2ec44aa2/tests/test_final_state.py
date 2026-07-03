# test_final_state.py

import os
import json
import pytest

OUTPUT_PATH = "/home/user/backup_routing_plan.json"

def test_output_file_exists():
    """Test that the output JSON file was created."""
    assert os.path.exists(OUTPUT_PATH), f"Output file {OUTPUT_PATH} does not exist. Did the script run successfully?"

def test_output_format_and_sorting():
    """Test that the output is a JSON array and sorted by database_id."""
    with open(OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_PATH} is not valid JSON.")

    assert isinstance(data, list), "Output must be a JSON array."
    assert len(data) == 2, f"Output should contain exactly 2 databases (DB1 and DB3) that need backup, but found {len(data)}."

    db_ids = [item.get("database_id") for item in data]
    assert db_ids == sorted(db_ids), "Output array must be sorted in ascending alphabetical order by database_id."

def test_output_routing_logic():
    """Test the correctness of the routing logic for each database."""
    with open(OUTPUT_PATH, 'r') as f:
        data = json.load(f)

    db_map = {item.get("database_id"): item for item in data}

    db1_id = "http://example.org/infra#DB1"
    db3_id = "http://example.org/infra#DB3"

    assert db1_id in db_map, f"Missing routing result for {db1_id}. Is the SPARQL query finding all databases needing backup?"
    assert db3_id in db_map, f"Missing routing result for {db3_id}. Is the SPARQL query finding all databases needing backup?"

    db1_res = db_map[db1_id]
    assert db1_res.get("target_storage_id") == "http://example.org/infra#Storage1", "DB1 should be routed to Storage1 (lowest latency)."
    assert db1_res.get("total_latency") == 25, f"DB1 total latency should be 25, got {db1_res.get('total_latency')}."
    assert db1_res.get("path") == [
        "http://example.org/infra#DB1",
        "http://example.org/infra#Switch1",
        "http://example.org/infra#Storage1"
    ], "DB1 path is incorrect. Check bidirectional link traversal."

    db3_res = db_map[db3_id]
    assert db3_res.get("target_storage_id") == "http://example.org/infra#Storage2", "DB3 should be routed to Storage2. Storage1 does not have enough capacity."
    assert db3_res.get("total_latency") == 42, f"DB3 total latency should be 42, got {db3_res.get('total_latency')}."
    assert db3_res.get("path") == [
        "http://example.org/infra#DB3",
        "http://example.org/infra#Switch2",
        "http://example.org/infra#Storage2"
    ], "DB3 path is incorrect. Check capacity constraints and bidirectional link traversal."