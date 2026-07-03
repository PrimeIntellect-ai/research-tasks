# test_final_state.py
import requests
import pytest

def test_metric_endpoint():
    url = "http://127.0.0.1:8080/metric"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}. Is the server running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP status code 200, got {response.status_code}. Response body: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response body: {response.text}")

    expected_scores = {
        "A": 0.2644,
        "B": 0.1472,
        "C": 0.3797,
        "D": 0.2087
    }

    for node, expected_score in expected_scores.items():
        assert node in data, f"Missing node '{node}' in the JSON response."
        actual_score = data[node]
        assert isinstance(actual_score, (int, float)), f"Score for node '{node}' is not a number: {actual_score}"
        assert abs(actual_score - expected_score) <= 0.001, (
            f"Score for node '{node}' is incorrect. "
            f"Expected ~{expected_score}, got {actual_score}. "
            "Did you use the correct metric (pagerank) and parameter (alpha=0.85)?"
        )