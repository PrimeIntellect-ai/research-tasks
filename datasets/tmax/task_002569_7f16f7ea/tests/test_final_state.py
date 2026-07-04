# test_final_state.py

import os
import time
import requests
import pytest

def test_mock_fixture_exists():
    path = "/app/rust-processor/tests/fixtures/mock_ast.json"
    assert os.path.isfile(path), f"Missing mock fixture file: {path}"

def test_rust_processor_evaluates_correctly():
    url = "http://127.0.0.1:8080/evaluate"

    # Wait for the service to be up
    max_retries = 10
    for i in range(max_retries):
        try:
            # We just want to see if the port is open and accepting HTTP connections
            requests.get("http://127.0.0.1:8080/", timeout=1)
            break
        except requests.ConnectionError:
            time.sleep(1)
    else:
        pytest.fail("Rust processor is not listening on 127.0.0.1:8080")

    # Test payload 1
    payload1 = {"version": "2.1.0", "rule_id": "rule-prod"}
    try:
        response1 = requests.post(url, json=payload1, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to send request to {url}: {e}")

    assert response1.status_code == 200, f"Expected status code 200, got {response1.status_code}. Response: {response1.text}"
    try:
        data1 = response1.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response1.text}")
    assert data1.get("allowed") is True, f"Expected allowed: true for {payload1}, got {data1}"

    # Test payload 2
    payload2 = {"version": "0.9.0", "rule_id": "rule-prod"}
    try:
        response2 = requests.post(url, json=payload2, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to send request to {url}: {e}")

    assert response2.status_code == 200, f"Expected status code 200, got {response2.status_code}. Response: {response2.text}"
    try:
        data2 = response2.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response2.text}")
    assert data2.get("allowed") is False, f"Expected allowed: false for {payload2}, got {data2}"