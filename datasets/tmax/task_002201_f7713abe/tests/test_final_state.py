# test_final_state.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"

def test_stats_endpoint():
    """Test the /stats GET endpoint for correct statistical results."""
    try:
        response = requests.get(f"{BASE_URL}/stats", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the /stats endpoint: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /stats is not valid JSON")

    expected_keys = {"t_stat", "p_value", "ci_lower", "ci_upper"}
    assert expected_keys.issubset(data.keys()), f"Missing keys in /stats response. Expected {expected_keys}, got {set(data.keys())}"

    assert isinstance(data["t_stat"], (int, float)), "t_stat must be a number"
    assert isinstance(data["p_value"], (int, float)), "p_value must be a number"
    assert isinstance(data["ci_lower"], (int, float)), "ci_lower must be a number"
    assert isinstance(data["ci_upper"], (int, float)), "ci_upper must be a number"

    # Check that CI does not contain 0 (significant difference)
    ci_lower = data["ci_lower"]
    ci_upper = data["ci_upper"]
    assert (ci_lower > 0 and ci_upper > 0) or (ci_lower < 0 and ci_upper < 0), "Confidence interval should not contain 0"

def test_retrieve_endpoint():
    """Test the /retrieve POST endpoint for correct similarity retrieval."""
    payload = {"chunk_id": 0, "top_k": 3}
    try:
        response = requests.post(f"{BASE_URL}/retrieve", json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the /retrieve endpoint: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /retrieve is not valid JSON")

    assert "similar_chunks" in data, "Missing 'similar_chunks' key in /retrieve response"
    similar_chunks = data["similar_chunks"]

    assert isinstance(similar_chunks, list), "similar_chunks must be a list"
    assert len(similar_chunks) == 3, f"Expected 3 similar chunks, got {len(similar_chunks)}"

    # Chunks 0-4 are identical, so top 3 similar to chunk 0 should be from {1, 2, 3, 4}
    valid_similar_set = {1, 2, 3, 4}
    for chunk in similar_chunks:
        assert chunk in valid_similar_set, f"Chunk {chunk} is not in the expected set of similar chunks {valid_similar_set}"