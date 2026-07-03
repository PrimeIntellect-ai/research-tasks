# test_final_state.py

import pytest
import requests
import time

def test_server_validation_and_rate_limiting():
    """
    Test the Go server's /validate endpoint for correct key validation and rate limiting.
    The server should allow exactly 4 requests before returning 429.
    """
    url = "http://127.0.0.1:8080/validate"

    # Wait for the server to be available (up to 5 seconds)
    server_up = False
    for _ in range(50):
        try:
            # Just a connection check, we don't care about the response yet
            requests.get("http://127.0.0.1:8080/")
            server_up = True
            break
        except requests.exceptions.ConnectionError:
            time.sleep(0.1)

    assert server_up, "Server is not listening on 127.0.0.1:8080"

    # Request 1: Valid keys
    resp1 = requests.post(url, json={"keys": ["omega", "sigma"]})
    assert resp1.status_code == 200, f"Request 1 expected 200 OK, got {resp1.status_code}"

    # Request 2: Valid key
    resp2 = requests.post(url, json={"keys": ["lambda"]})
    assert resp2.status_code == 200, f"Request 2 expected 200 OK, got {resp2.status_code}"

    # Request 3: Invalid key mixed with valid
    resp3 = requests.post(url, json={"keys": ["omega", "invalid_key"]})
    assert resp3.status_code == 400, f"Request 3 expected 400 Bad Request, got {resp3.status_code}"

    # Request 4: Valid key
    resp4 = requests.post(url, json={"keys": ["theta"]})
    assert resp4.status_code == 200, f"Request 4 expected 200 OK, got {resp4.status_code}"

    # Request 5: Valid key, but rate limit exceeded
    resp5 = requests.post(url, json={"keys": ["sigma"]})
    assert resp5.status_code == 429, f"Request 5 expected 429 Too Many Requests, got {resp5.status_code}"

    # Request 6: Invalid key, rate limit exceeded
    resp6 = requests.post(url, json={"keys": ["invalid_key"]})
    assert resp6.status_code == 429, f"Request 6 expected 429 Too Many Requests, got {resp6.status_code}"