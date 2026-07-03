# test_final_state.py

import os
import json
import pytest
import requests

def test_api_prioritize_backups():
    metadata_path = "/home/user/data/backup_metadata.json"
    dependencies_path = "/home/user/data/db_dependencies.json"

    assert os.path.exists(metadata_path), f"Missing {metadata_path}"
    assert os.path.exists(dependencies_path), f"Missing {dependencies_path}"

    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    with open(dependencies_path, "r") as f:
        dependencies = json.load(f)

    # Filter out tier 3
    valid_dbs = {db["db_name"]: db for db in metadata if db.get("tier") != 3}

    # Calculate In-Degree for remaining databases
    in_degrees = {db_name: 0 for db_name in valid_dbs}
    for edge in dependencies:
        target = edge.get("target")
        if target in in_degrees:
            in_degrees[target] += 1

    # Calculate Score
    scores = {}
    for db_name, db_info in valid_dbs.items():
        size_gb = db_info.get("size_gb", 1)
        score = (in_degrees[db_name] + 1) * (1000 / size_gb)
        scores[db_name] = score

    # Sort descending by score
    sorted_dbs = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)
    expected_top_5 = sorted_dbs[:5]

    # Test the API
    url = "http://127.0.0.1:8080/prioritize-backups"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}. Is the service running? Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response body: {response.text}")

    assert "priority_backups" in data, f"Key 'priority_backups' missing from response. Actual response: {data}"

    actual_top_5 = data["priority_backups"]
    assert actual_top_5 == expected_top_5, f"Expected priority_backups to be {expected_top_5}, but got {actual_top_5}"