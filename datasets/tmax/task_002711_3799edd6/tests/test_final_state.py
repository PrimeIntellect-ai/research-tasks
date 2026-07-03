# test_final_state.py

import os
import json
import sqlite3
import pytest

def test_output_page2_json():
    output_path = "/home/user/output_page2.json"
    assert os.path.exists(output_path), f"Output file not found at {output_path}"

    db_path = "/home/user/data.db"
    assert os.path.exists(db_path), f"Database not found at {db_path}"

    interactions_path = "/home/user/interactions.json"
    assert os.path.exists(interactions_path), f"Interactions file not found at {interactions_path}"

    # 1. Load users from SQLite
    users = {}
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM users")
        for row in cursor.fetchall():
            users[row[0]] = {"name": row[1], "centrality": 0}
        conn.close()
    except sqlite3.Error as e:
        pytest.fail(f"Failed to query SQLite database: {e}")

    # 2. Load interactions and compute centrality
    try:
        with open(interactions_path, 'r') as f:
            interactions = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse interactions JSON file: {e}")

    for interaction in interactions:
        src = interaction.get("src")
        dst = interaction.get("dst")
        weight = interaction.get("weight", 0)
        if src in users:
            users[src]["centrality"] += weight
        if dst in users:
            users[dst]["centrality"] += weight

    # 3. Filter >= 10
    filtered_users = []
    for uid, data in users.items():
        if data["centrality"] >= 10:
            filtered_users.append({
                "id": uid,
                "name": data["name"],
                "centrality": data["centrality"]
            })

    # 4. Sort by centrality DESC, name ASC
    filtered_users.sort(key=lambda x: (-x["centrality"], x["name"]))

    # 5. Pagination (Page size 3, Page 2)
    # Page 1: 0, 1, 2
    # Page 2: 3, 4, 5
    expected_page2 = filtered_users[3:6]

    # 6. Read and verify output file
    try:
        with open(output_path, 'r') as f:
            actual_output = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse output JSON file: {e}")

    assert isinstance(actual_output, list), f"Output JSON must be a list, got {type(actual_output).__name__}"
    assert len(actual_output) == len(expected_page2), f"Expected {len(expected_page2)} items in page 2, found {len(actual_output)}"

    for i, (actual, expected) in enumerate(zip(actual_output, expected_page2)):
        assert actual.get("id") == expected["id"], f"Item at index {i} has incorrect id. Expected {expected['id']}, got {actual.get('id')}"
        assert actual.get("name") == expected["name"], f"Item at index {i} has incorrect name. Expected {expected['name']}, got {actual.get('name')}"
        assert actual.get("centrality") == expected["centrality"], f"Item at index {i} has incorrect centrality. Expected {expected['centrality']}, got {actual.get('centrality')}"