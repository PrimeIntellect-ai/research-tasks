# test_final_state.py
import os
import json
import pytest

def test_top_papers_json_exists_and_correct():
    """Test if /home/user/top_papers.json exists and contains the correct aggregation results."""
    file_path = "/home/user/top_papers.json"
    assert os.path.exists(file_path), f"{file_path} does not exist. The Go script may not have run successfully or saved to the wrong location."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} does not contain valid JSON.")

    expected_data = [
        {
            "_id": "P01",
            "network_size": 5
        },
        {
            "_id": "P02",
            "network_size": 4
        },
        {
            "_id": "P03",
            "network_size": 2
        }
    ]

    assert isinstance(data, list), f"Data in {file_path} must be a JSON array."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} results, got {len(data)}."

    for i, expected_doc in enumerate(expected_data):
        assert data[i].get("_id") == expected_doc["_id"], f"Expected _id '{expected_doc['_id']}' at index {i}, got '{data[i].get('_id')}'."
        assert data[i].get("network_size") == expected_doc["network_size"], f"Expected network_size {expected_doc['network_size']} for _id '{expected_doc['_id']}', got {data[i].get('network_size')}."
        # Ensure no extra fields are present (projection requirement)
        assert set(data[i].keys()) == {"_id", "network_size"}, f"Document at index {i} contains extra or missing fields. Expected only '_id' and 'network_size'."

def test_go_script_exists():
    """Test if the Go script was created at the expected location."""
    file_path = "/home/user/analyze.go"
    assert os.path.exists(file_path), f"{file_path} does not exist. The Go script must be saved here."
    assert os.path.isfile(file_path), f"{file_path} is not a file."