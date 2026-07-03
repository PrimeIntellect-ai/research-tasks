# test_final_state.py

import pytest
import requests

def test_top_affiliations_endpoint():
    url = "http://127.0.0.1:8080/top-affiliations"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the web service at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response body: {response.text}")

    expected = [["r2", 3], ["r3", 3], ["r1", 2]]
    assert data == expected, f"Expected JSON {expected}, got {data}"