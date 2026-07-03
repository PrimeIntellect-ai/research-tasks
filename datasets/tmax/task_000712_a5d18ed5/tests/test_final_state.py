# test_final_state.py

import os
import requests
import pytest

def test_health_endpoint():
    url = "http://127.0.0.1:8080/health"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data == {"status": "ok"}, f"Expected {{'status': 'ok'}}, got {data}"

def test_build_endpoint():
    url = "http://127.0.0.1:8080/build"
    try:
        response = requests.post(url, timeout=30)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response body: {response.text}"
    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected = {"status": "success", "target_version": "2.1.0"}
    assert data == expected, f"Expected {expected}, got {data}"

def test_memory_report():
    path = "/home/user/build_artifacts/memory_report.txt"
    assert os.path.isfile(path), f"Memory report file not found at {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    try:
        memory_usage = float(content)
    except ValueError:
        pytest.fail(f"Could not parse memory report content as float: '{content}'")

    assert memory_usage > 0, f"Expected memory usage to be greater than 0, got {memory_usage}"