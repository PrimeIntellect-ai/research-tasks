# test_final_state.py
import time
import requests
import random
import pytest

def test_api_performance_and_correctness():
    """
    Test that the API serves requests correctly and meets the performance threshold.
    The goal is to serve 100 requests in <= 2.5 seconds.
    """
    base_url = "http://127.0.0.1:5000/events"

    # Warmup
    try:
        for _ in range(5):
            requests.get(f"{base_url}?user_id=1&page=1&limit=10", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API during warmup: {e}")

    errors = 0
    start_time = time.time()

    for _ in range(100):
        uid = random.randint(1, 1000)
        try:
            resp = requests.get(f"{base_url}?user_id={uid}&page=1&limit=50", timeout=5)
            if resp.status_code != 200:
                errors += 1
        except requests.exceptions.RequestException:
            errors += 1

    total_time = time.time() - start_time

    assert errors == 0, f"FAILED: {errors} out of 100 requests failed or returned non-200 status codes."
    assert total_time <= 2.5, f"FAIL: Performance threshold not met. Expected <= 2.5s, got {total_time:.3f}s"