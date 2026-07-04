# test_final_state.py

import os
import json
import csv
from collections import defaultdict
import pytest

OUTPUT_PATH = "/home/user/output.json"
INPUT_PATH = "/home/user/raw_events.csv"

def compute_expected_top_users():
    """Compute the expected top 5 users directly from the raw events file."""
    sessions = defaultdict(set)

    # Read the CSV and group users by session
    with open(INPUT_PATH, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_id = row.get("user_id", "").strip()
            session_id = row.get("session_id", "").strip()
            if user_id and session_id:
                sessions[session_id].add(user_id)

    # Build the graph (undirected, unweighted, no self-loops)
    graph = defaultdict(set)
    for users in sessions.values():
        for u1 in users:
            for u2 in users:
                if u1 != u2:
                    graph[u1].add(u2)

    # Compute degrees
    degrees = {u: len(neighbors) for u, neighbors in graph.items()}

    # Sort by degree (descending), then by user_id (ascending alphabetical)
    sorted_users = sorted(degrees.items(), key=lambda x: (-x[1], x[0]))

    # Return top 5 in the expected format
    return [{"user_id": u, "degree": d} for u, d in sorted_users[:5]]

def test_output_file_exists():
    """Test that the output JSON file has been created."""
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} does not exist. The pipeline did not write the output."

def test_output_json_structure_and_values():
    """Test that the output JSON strictly follows the required schema and contains correct values."""
    with open(OUTPUT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {OUTPUT_PATH} does not contain valid JSON.")

    assert "schema_version" in data, "JSON output is missing the 'schema_version' key."
    assert data["schema_version"] == "1.0", f"Expected schema_version '1.0', but got {data['schema_version']}."

    assert "top_users" in data, "JSON output is missing the 'top_users' key."
    top_users = data["top_users"]

    assert isinstance(top_users, list), "The 'top_users' field must be a list."

    expected_top_users = compute_expected_top_users()

    assert len(top_users) == len(expected_top_users), f"Expected {len(expected_top_users)} users in 'top_users', but got {len(top_users)}."

    for i, (actual, expected) in enumerate(zip(top_users, expected_top_users)):
        assert isinstance(actual, dict), f"Element at index {i} in 'top_users' is not a dictionary."
        assert "user_id" in actual, f"Element at index {i} is missing 'user_id'."
        assert "degree" in actual, f"Element at index {i} is missing 'degree'."

        assert actual["user_id"] == expected["user_id"], f"Expected user_id '{expected['user_id']}' at rank {i+1}, but got '{actual['user_id']}'."
        assert actual["degree"] == expected["degree"], f"Expected degree {expected['degree']} for user {expected['user_id']}, but got {actual['degree']}."