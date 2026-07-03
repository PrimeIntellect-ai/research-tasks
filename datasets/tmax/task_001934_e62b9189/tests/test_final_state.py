# test_final_state.py

import pytest
import requests
import math

BASE_URL = "http://127.0.0.1:8000/api/v1/record"
AUTH_HEADER = {"Authorization": "Bearer ds_secret_2024"}

def check_record(record_id, expected_tokens, expected_a, expected_b):
    url = f"{BASE_URL}/{record_id}"
    try:
        response = requests.get(url, headers=AUTH_HEADER, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API or request timed out: {e}")

    assert response.status_code == 200, f"Expected status code 200 for record {record_id}, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response for record {record_id} is not valid JSON. Response text: {response.text}")

    assert "id" in data, f"Missing 'id' in response for record {record_id}"
    assert data["id"] == record_id, f"Expected id {record_id}, got {data['id']}"

    assert "tokens" in data, f"Missing 'tokens' in response for record {record_id}"
    assert data["tokens"] == expected_tokens, f"Expected tokens {expected_tokens}, got {data['tokens']}"

    assert "imputed_a" in data, f"Missing 'imputed_a' in response for record {record_id}"
    assert math.isclose(data["imputed_a"], expected_a, rel_tol=1e-5), f"Expected imputed_a {expected_a}, got {data['imputed_a']}"

    assert "scaled_b" in data, f"Missing 'scaled_b' in response for record {record_id}"
    assert math.isclose(data["scaled_b"], expected_b, rel_tol=1e-5), f"Expected scaled_b {expected_b}, got {data['scaled_b']}"

def test_record_1():
    check_record(1, ["café", "ñandú", "hola"], 10.0, 6.28)

def test_record_2():
    check_record(2, ["the", "quick", "brown", "fox"], 20.0, 15.7)

def test_record_3():
    check_record(3, ["こんにちは世界", "123"], 30.0, 31.4)

def test_record_4():
    check_record(4, ["ænima", "songtest"], 40.0, 4.71)

def test_record_99_not_found():
    url = f"{BASE_URL}/99"
    try:
        response = requests.get(url, headers=AUTH_HEADER, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API or request timed out: {e}")

    assert response.status_code == 404, f"Expected status code 404 for missing record 99, got {response.status_code}"

def test_unauthorized():
    url = f"{BASE_URL}/1"
    try:
        response = requests.get(url, headers={"Authorization": "Bearer wrong_token"}, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API or request timed out: {e}")

    assert response.status_code == 401, f"Expected status code 401 for wrong token, got {response.status_code}"

def test_missing_auth():
    url = f"{BASE_URL}/1"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API or request timed out: {e}")

    assert response.status_code == 401, f"Expected status code 401 for missing auth header, got {response.status_code}"