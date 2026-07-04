# test_final_state.py
import os
import json
import math
import pytest

OUTPUT_PATH = "/home/user/restore_priority.json"

EXPECTED_DATA = [
    {
        "server_name": "DB-01",
        "in_degree_centrality": 0.5,
        "total_backup_size": 500
    },
    {
        "server_name": "CACHE-01",
        "in_degree_centrality": 0.5,
        "total_backup_size": 20
    },
    {
        "server_name": "APP-01",
        "in_degree_centrality": 0.25,
        "total_backup_size": 570
    },
    {
        "server_name": "APP-02",
        "in_degree_centrality": 0.25,
        "total_backup_size": 570
    },
    {
        "server_name": "WEB-01",
        "in_degree_centrality": 0.0,
        "total_backup_size": 110
    }
]

def test_output_file_exists():
    assert os.path.exists(OUTPUT_PATH), f"Output file {OUTPUT_PATH} is missing."
    assert os.path.isfile(OUTPUT_PATH), f"{OUTPUT_PATH} should be a regular file."

def test_output_content_and_order():
    with open(OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{OUTPUT_PATH} does not contain valid JSON.")

    assert isinstance(data, list), f"Expected the JSON output to be a list, got {type(data).__name__}."
    assert len(data) == len(EXPECTED_DATA), f"Expected {len(EXPECTED_DATA)} items, found {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, EXPECTED_DATA)):
        assert isinstance(actual, dict), f"Item at index {i} is not a dictionary."

        # Check keys
        expected_keys = {"server_name", "in_degree_centrality", "total_backup_size"}
        assert set(actual.keys()) == expected_keys, f"Item at index {i} has incorrect keys. Expected {expected_keys}, got {set(actual.keys())}."

        # Check server_name
        assert actual["server_name"] == expected["server_name"], f"Item at index {i} has incorrect server_name. Expected {expected['server_name']}, got {actual['server_name']}."

        # Check in_degree_centrality with a tolerance for floating point differences
        assert math.isclose(actual["in_degree_centrality"], expected["in_degree_centrality"], abs_tol=0.001), \
            f"Item at index {i} has incorrect in_degree_centrality. Expected {expected['in_degree_centrality']}, got {actual['in_degree_centrality']}."

        # Check total_backup_size
        assert actual["total_backup_size"] == expected["total_backup_size"], \
            f"Item at index {i} has incorrect total_backup_size. Expected {expected['total_backup_size']}, got {actual['total_backup_size']}."