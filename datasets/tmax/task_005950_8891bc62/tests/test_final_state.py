# test_final_state.py

import os
import json
import subprocess
import pytest

def test_output_json_exists_and_correct():
    """Test that output.json exists, is valid JSON, and contains the correct subordinates."""
    filepath = "/home/user/output.json"
    assert os.path.isfile(filepath), f"Output file {filepath} does not exist."

    with open(filepath, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{filepath} is not a valid JSON file.")

    assert isinstance(data, list), f"{filepath} should contain a JSON array."
    assert len(data) == 3, f"Expected exactly 3 documents in {filepath}, got {len(data)}."

    expected_ids = ["E5", "E7", "E8"]
    actual_ids = [doc.get("_id") for doc in data]

    assert actual_ids == expected_ids, f"Expected documents with _ids {expected_ids} in order, but got {actual_ids}."

def test_managerid_index_exists():
    """Test that an index on managerId exists in the company.employees collection."""
    # Find the mongo shell executable
    mongo_bin = None
    possible_paths = [
        "/home/user/mongodb/bin/mongosh",
        "/home/user/mongodb/bin/mongo",
        "mongosh",
        "mongo"
    ]

    for path in possible_paths:
        try:
            res = subprocess.run([path, "--version"], capture_output=True, text=True)
            if res.returncode == 0:
                mongo_bin = path
                break
        except FileNotFoundError:
            continue

    assert mongo_bin is not None, "Could not find 'mongosh' or 'mongo' binary to verify database state."

    # Query the indexes on company.employees
    cmd = [
        mongo_bin,
        "127.0.0.1:27017/company",
        "--quiet",
        "--eval",
        "JSON.stringify(db.employees.getIndexes())"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to query MongoDB indexes. Error: {result.stderr}"

    try:
        indexes = json.loads(result.stdout.strip())
    except json.JSONDecodeError:
        # Fallback if output is not strict JSON but a JS object string
        assert "managerId" in result.stdout, "Could not find index on managerId in the collection."
        return

    # Check if any index has 'managerId' as a key
    has_managerid_index = False
    for idx in indexes:
        keys = idx.get("key", {})
        if "managerId" in keys:
            has_managerid_index = True
            break

    assert has_managerid_index, "No index found on 'managerId' field in 'company.employees' collection."