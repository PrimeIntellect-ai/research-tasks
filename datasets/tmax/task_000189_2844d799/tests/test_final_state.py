# test_final_state.py

import os
import pytest
import requests
import concurrent.futures
import time

API_KEY = "secr3t_m@th_88"
TENANT_ID = "8472"
BASE_URL = "http://127.0.0.1:9090"

def test_service_running_and_correct():
    # Wait for service to be up if not already
    max_retries = 5
    for i in range(max_retries):
        try:
            # Just a simple GET to see if port is open, or we can just proceed
            requests.get(f"{BASE_URL}/", timeout=1)
            break
        except requests.exceptions.RequestException:
            time.sleep(1)

    headers = {"X-API-Key": API_KEY}

    # Send 50 concurrent POST requests
    num_requests = 50
    value = 100
    payload = {"uptime_ms": value}

    def send_ping():
        response = requests.post(
            f"{BASE_URL}/record_ping/{TENANT_ID}",
            json=payload,
            headers=headers,
            timeout=5
        )
        return response.status_code

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(send_ping) for _ in range(num_requests)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    for res in results:
        assert res == 200, f"Expected status code 200, got {res}"

    # Get the final EMA
    response = requests.get(f"{BASE_URL}/uptime/{TENANT_ID}", headers=headers, timeout=5)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    data = response.json()
    assert "ema" in data, "Response JSON missing 'ema' field"

    actual_ema = data["ema"]

    # Calculate expected EMA
    # Assuming initial EMA is 0 and alpha is 0.1 as per typical EMA implementations in this context
    # EMA_n = alpha * V + (1 - alpha) * EMA_{n-1}
    # Since all V are 100, EMA_n = 100 * (1 - (1 - alpha)^n)
    alpha = 0.1
    expected_ema = value * (1 - (1 - alpha)**num_requests)

    # If race condition is present, actual_ema will be less because some updates were lost.
    # If math bug is present, actual_ema will be completely wrong.
    assert abs(actual_ema - expected_ema) < 1e-4, f"Expected EMA to be ~{expected_ema}, but got {actual_ema}. This indicates either the math bug or the concurrency bug is not fully fixed."