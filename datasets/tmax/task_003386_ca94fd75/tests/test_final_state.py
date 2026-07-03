# test_final_state.py

import pytest
import requests
import math

BASE_URL = "http://127.0.0.1:8123"
ENDPOINT = "/api/v1/posterior"
AUTH_HEADER = {"Authorization": "Bearer bayes_rule_2024"}

def test_api_success_id_1():
    try:
        resp = requests.get(f"{BASE_URL}{ENDPOINT}?id=1", headers=AUTH_HEADER, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert resp.status_code == 200, f"Expected 200 OK for id=1, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert "id" in data, "Response JSON missing 'id' key"
    assert data["id"] == 1, f"Expected id=1, got {data['id']}"
    assert "posterior_mean" in data, "Response JSON missing 'posterior_mean' key"
    assert math.isclose(data["posterior_mean"], 0.2, rel_tol=1e-5), f"Expected posterior_mean ~ 0.2, got {data['posterior_mean']}"

def test_api_success_id_2():
    try:
        resp = requests.get(f"{BASE_URL}{ENDPOINT}?id=2", headers=AUTH_HEADER, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert resp.status_code == 200, f"Expected 200 OK for id=2, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert "id" in data, "Response JSON missing 'id' key"
    assert data["id"] == 2, f"Expected id=2, got {data['id']}"
    assert "posterior_mean" in data, "Response JSON missing 'posterior_mean' key"
    assert math.isclose(data["posterior_mean"], 0.1, rel_tol=1e-5), f"Expected posterior_mean ~ 0.1, got {data['posterior_mean']}"

def test_api_unauthorized():
    try:
        resp1 = requests.get(f"{BASE_URL}{ENDPOINT}?id=1", headers={"Authorization": "Bearer wrong_token"}, timeout=2)
        resp2 = requests.get(f"{BASE_URL}{ENDPOINT}?id=1", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert resp1.status_code == 401, f"Expected 401 Unauthorized for bad token, got {resp1.status_code}"
    assert resp2.status_code == 401, f"Expected 401 Unauthorized for missing token, got {resp2.status_code}"

def test_api_not_found():
    try:
        resp = requests.get(f"{BASE_URL}{ENDPOINT}?id=999", headers=AUTH_HEADER, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to API: {e}")

    assert resp.status_code == 404, f"Expected 404 Not Found for non-existent ID, got {resp.status_code}"