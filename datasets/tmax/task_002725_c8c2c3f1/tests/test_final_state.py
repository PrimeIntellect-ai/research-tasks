# test_final_state.py
import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"

def test_target_neighborhood():
    url = f"{BASE_URL}/api/target_neighborhood"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to the API at {url}. Is the server running?")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected = ["N_01", "N_02", "N_42", "N_99"]
    assert isinstance(data, list), "Expected a JSON array"
    assert sorted(data) == expected, f"Expected {expected}, got {sorted(data)}"

def test_aggregate_like():
    url = f"{BASE_URL}/api/aggregate?interaction_type=like"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to the API at {url}. Is the server running?")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert isinstance(data, dict), "Expected a JSON object"
    assert "average_age" in data, "Expected key 'average_age' in response"

    # 25 + 40 = 65 / 2 = 32.5
    assert float(data["average_age"]) == 32.5, f"Expected average_age to be 32.5, got {data['average_age']}"

def test_aggregate_comment():
    url = f"{BASE_URL}/api/aggregate?interaction_type=comment"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Could not connect to the API at {url}. Is the server running?")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert isinstance(data, dict), "Expected a JSON object"
    assert "average_age" in data, "Expected key 'average_age' in response"

    # Source for comment is N_02, age is 30
    assert float(data["average_age"]) == 30.0, f"Expected average_age to be 30.0, got {data['average_age']}"