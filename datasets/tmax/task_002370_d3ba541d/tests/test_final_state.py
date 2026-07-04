# test_final_state.py

import os
import json
import subprocess
import pytest

SCRIPT_PATH = "/home/user/process_citations.sh"
DB_PATH = "/home/user/citations.db"
JSON_PATH = "/home/user/citation_tree.json"

@pytest.fixture(scope="session", autouse=True)
def run_script():
    """Run the student's script before running the tests."""
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

    # Run the script
    result = subprocess.run(
        ["bash", SCRIPT_PATH],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed with return code {result.returncode}\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

def test_database_created():
    """Verify that the SQLite database was created."""
    assert os.path.exists(DB_PATH), f"Database file not found at {DB_PATH}"

def test_json_output_exists():
    """Verify that the output JSON file was created."""
    assert os.path.exists(JSON_PATH), f"JSON output file not found at {JSON_PATH}"

def test_json_output_content():
    """Verify the contents and structure of the JSON output."""
    with open(JSON_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse JSON from {JSON_PATH}: {e}")

    assert isinstance(data, list), "JSON output should be a list of objects"

    expected_data = [
        {"depth": 0, "paper_id": "P001", "title": "Graph Processing Basics"},
        {"depth": 1, "paper_id": "P002", "title": "Advanced SQL"},
        {"depth": 1, "paper_id": "P003", "title": "Data Querying Patterns"},
        {"depth": 2, "paper_id": "P004", "title": "Recursive CTEs in Practice"},
        {"depth": 3, "paper_id": "P006", "title": "Deep Graph Traversals"}
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items in JSON array, got {len(data)}"

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object"

        # Check keys
        expected_keys = {"depth", "paper_id", "title"}
        actual_keys = set(actual.keys())
        assert actual_keys == expected_keys, f"Item at index {i} has incorrect keys. Expected {expected_keys}, got {actual_keys}"

        # Check values
        assert actual["depth"] == expected["depth"], f"Incorrect depth at index {i}. Expected {expected['depth']}, got {actual['depth']}"
        assert actual["paper_id"] == expected["paper_id"], f"Incorrect paper_id at index {i}. Expected {expected['paper_id']}, got {actual['paper_id']}"
        assert actual["title"] == expected["title"], f"Incorrect title at index {i}. Expected {expected['title']}, got {actual['title']}"