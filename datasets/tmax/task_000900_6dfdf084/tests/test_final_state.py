# test_final_state.py
import pytest
import requests

def test_coauthors_endpoint():
    url = "http://127.0.0.1:8080/api/graph/coauthors"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}. Ensure the server is running and listening on port 8080. Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response body: {response.text}")

    assert isinstance(data, list), f"Expected response to be a JSON array, got {type(data).__name__}"

    expected_coauthors = {"A-311", "A-412", "A-500", "A-701"}
    actual_coauthors = set(data)

    assert actual_coauthors == expected_coauthors, f"Expected co-authors {expected_coauthors}, but got {actual_coauthors}"