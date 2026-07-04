# test_final_state.py
import requests
import time
import pytest

def test_recommend_endpoint():
    url = "http://127.0.0.1:8000/recommend"
    payload = {"features": [0.1] * 10}

    max_retries = 5
    response = None
    for i in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=5)
            break
        except requests.exceptions.RequestException:
            if i == max_retries - 1:
                pytest.fail("Failed to connect to the API server at 127.0.0.1:8000. Ensure the server is running and bound to the correct host and port.")
            time.sleep(1)

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "recommended_class" in data, "Response JSON missing 'recommended_class' key"
    assert "similar_ids" in data, "Response JSON missing 'similar_ids' key"

    assert isinstance(data["recommended_class"], int), f"'recommended_class' should be an integer, got {type(data['recommended_class'])}"
    assert isinstance(data["similar_ids"], list), f"'similar_ids' should be a list, got {type(data['similar_ids'])}"

    assert len(data["similar_ids"]) in [3, 5], f"Expected 'similar_ids' length to be 3 or 5 (from K_NEIGHBORS grid), got {len(data['similar_ids'])}"

    for item in data["similar_ids"]:
        assert isinstance(item, int), f"All items in 'similar_ids' should be integers, found {type(item)}"