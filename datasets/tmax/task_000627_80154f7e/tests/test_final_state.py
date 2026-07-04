# test_final_state.py

import os
import requests
import pytest

def test_engine_binary_exists():
    binary_path = "/home/user/engine"
    assert os.path.isfile(binary_path), f"C++ engine binary not found at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"File at {binary_path} is not executable"

def test_http_service_response():
    url = "http://127.0.0.1:8080/user_stats"
    params = {"user_id": "101"}

    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP service at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP status code 200, got {response.status_code}"

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type 'application/json', got '{content_type}'"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON: {response.text}")

    expected_email = "alice@example.com"
    expected_total_spent = 26.0

    assert "email" in data, "Response JSON missing 'email' field"
    assert "total_spent" in data, "Response JSON missing 'total_spent' field"

    assert data["email"] == expected_email, f"Expected email '{expected_email}', got '{data['email']}'"
    assert float(data["total_spent"]) == expected_total_spent, f"Expected total_spent {expected_total_spent}, got {data['total_spent']}"