# test_final_state.py
import os
import requests
import json
import time

def test_return_distribution_plot_exists():
    assert os.path.isfile('/home/user/return_distribution.png'), "/home/user/return_distribution.png is missing"

def test_api_stats():
    url = "http://127.0.0.0:8080/stats"

    # Retry logic in case the server takes a moment to start or respond
    max_retries = 5
    response = None
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            break
        except requests.exceptions.RequestException:
            time.sleep(1)

    assert response is not None, "Failed to connect to the HTTP server at 0.0.0.0:8080"
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        assert False, "Response is not valid JSON"

    assert "average_return_time" in data, "Key 'average_return_time' missing in JSON response"
    assert "error" in data, "Key 'error' missing in JSON response"

    avg_return_time = float(data["average_return_time"])
    error = float(data["error"])

    assert 4.90 <= avg_return_time <= 5.10, f"average_return_time {avg_return_time} is not between 4.90 and 5.10"
    assert 0.0 <= error <= 0.10, f"error {error} is not between 0.0 and 0.10"