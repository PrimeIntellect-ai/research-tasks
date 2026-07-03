# test_final_state.py
import pytest
import requests

def test_analyze_endpoint():
    url = "http://127.0.0.1:8555/analyze"
    payload = {"node": "ProtA"}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "direct_interactions" in data, "Missing 'direct_interactions' in response"
    assert "strongest_path_to_hub" in data, "Missing 'strongest_path_to_hub' in response"
    assert "rolling_avg_strength" in data, "Missing 'rolling_avg_strength' in response"

    # Check direct interactions
    expected_direct = [
        {"target": "ProtD", "strength": 90},
        {"target": "ProtB", "strength": 50},
        {"target": "ProtZ", "strength": 5}
    ]
    assert data["direct_interactions"] == expected_direct, f"Expected direct_interactions {expected_direct}, got {data['direct_interactions']}"

    # Check strongest path
    expected_path = "ProtA -> ProtD -> ProtHub"
    assert data["strongest_path_to_hub"] == expected_path, f"Expected strongest_path_to_hub '{expected_path}', got '{data['strongest_path_to_hub']}'"

    # Check rolling average strength
    expected_avg = 41.25
    assert abs(data["rolling_avg_strength"] - expected_avg) < 1e-5, f"Expected rolling_avg_strength {expected_avg}, got {data['rolling_avg_strength']}"