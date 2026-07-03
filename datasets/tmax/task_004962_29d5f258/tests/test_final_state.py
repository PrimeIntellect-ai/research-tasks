# test_final_state.py

import os
import json
import subprocess
import requests
import pytest
import time

API_URL = "http://127.0.0.1:8080/api/graph"

def test_api_server_is_running():
    """Verify that the C server is listening on port 8080."""
    try:
        response = requests.get(f"{API_URL}?category=tech", timeout=2)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    except requests.exceptions.ConnectionError:
        pytest.fail("Failed to connect to the API server on 127.0.0.1:8080. Is it running?")

def test_api_tech_category_response():
    """Verify the API response structure and logic for the 'tech' category."""
    response = requests.get(f"{API_URL}?category=tech", timeout=2)
    assert response.status_code == 200

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type application/json, got {content_type}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response body is not valid JSON: {response.text}")

    assert data.get("category") == "tech", "Expected category to be 'tech'"
    nodes = data.get("nodes")
    assert isinstance(nodes, list), "Expected 'nodes' to be a list"
    assert len(nodes) == 2, f"Expected 2 nodes for 'tech', got {len(nodes)}"

    # Check sorting by user_id asc
    assert nodes[0].get("user_id") == 1
    assert nodes[1].get("user_id") == 2

    # Check Alice (user 1)
    alice = nodes[0]
    assert alice.get("user_name") == "Alice"
    alice_followers = alice.get("top_followers", [])
    assert len(alice_followers) == 3, "Expected exactly 3 top followers for Alice"

    # Check sorting by score desc
    assert alice_followers[0] == {"follower_id": 4, "score": 99}
    assert alice_followers[1] == {"follower_id": 2, "score": 95}
    assert alice_followers[2] == {"follower_id": 3, "score": 80}

    # Check Bob (user 2)
    bob = nodes[1]
    assert bob.get("user_name") == "Bob"
    bob_followers = bob.get("top_followers", [])
    assert len(bob_followers) == 2, "Expected exactly 2 followers for Bob"
    assert bob_followers[0] == {"follower_id": 3, "score": 60}
    assert bob_followers[1] == {"follower_id": 1, "score": 50}

def test_redis_caching():
    """Verify that the API server caches the response in Redis."""
    # Ensure the API has been called at least once to populate the cache
    requests.get(f"{API_URL}?category=tech", timeout=2)

    # Query Redis directly
    result = subprocess.run(
        ["redis-cli", "GET", "graph:tech"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "Failed to execute redis-cli"

    redis_output = result.stdout.strip()
    assert redis_output != "" and redis_output != "(nil)", "Redis key 'graph:tech' is missing or empty"

    try:
        cached_data = json.loads(redis_output)
    except json.JSONDecodeError:
        pytest.fail(f"Cached data in Redis is not valid JSON: {redis_output}")

    assert cached_data.get("category") == "tech", "Cached JSON does not match expected structure"
    assert "nodes" in cached_data, "Cached JSON missing 'nodes'"