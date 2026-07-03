# test_final_state.py

import pytest
import requests
import time
import threading

def test_api_report_endpoint():
    url = "http://127.0.0.1:8000/api/report"

    # Retry a few times in case the service is slow to start
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=2)
            break
        except requests.exceptions.ConnectionError:
            if i == max_retries - 1:
                pytest.fail(f"Could not connect to service at {url}")
            time.sleep(1)

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert "secret_token" in data, "Missing 'secret_token' in JSON response"
    assert data["secret_token"] == "dev_token_9x2b_lost", f"Incorrect secret_token. Expected 'dev_token_9x2b_lost', got {data['secret_token']}"

    assert "red_frame" in data, "Missing 'red_frame' in JSON response"
    assert data["red_frame"] == 87, f"Incorrect red_frame. Expected 87, got {data['red_frame']}"

    assert "recovered_id" in data, "Missing 'recovered_id' in JSON response"
    assert data["recovered_id"] == 14092, f"Incorrect recovered_id. Expected 14092, got {data['recovered_id']}"

def test_concurrency_metrics_endpoint():
    # If the endpoint exists, hammer it to ensure no 500 errors
    url = "http://127.0.0.1:8000/api/metrics"

    try:
        res = requests.get(url, timeout=2)
        if res.status_code == 404:
            # Endpoint might not be exposed or named differently, skip
            return
    except requests.exceptions.ConnectionError:
        return

    errors = []

    def hammer():
        for _ in range(50):
            try:
                r = requests.get(url, timeout=2)
                if r.status_code == 500:
                    errors.append("Internal Server Error (500) received, possible race condition.")
            except Exception as e:
                errors.append(str(e))

    threads = [threading.Thread(target=hammer) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors, f"Concurrency test failed with errors: {errors[0]}"