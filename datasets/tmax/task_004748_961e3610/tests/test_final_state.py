# test_final_state.py

import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"
ENDPOINT = "/dept-top-earners"
CORRECT_TOKEN = "SuperSecret123!"

def test_unauthorized_no_token():
    url = f"{BASE_URL}{ENDPOINT}?dept_id=D1"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("The service is not running on 127.0.0.1:8080")

    assert response.status_code == 401, f"Expected 401 Unauthorized without token, got {response.status_code}"

def test_unauthorized_wrong_token():
    url = f"{BASE_URL}{ENDPOINT}?dept_id=D1"
    headers = {"Authorization": "Bearer WrongToken!"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("The service is not running on 127.0.0.1:8080")

    assert response.status_code == 401, f"Expected 401 Unauthorized with wrong token, got {response.status_code}"

def test_authorized_correct_response():
    url = f"{BASE_URL}{ENDPOINT}?dept_id=D1"
    headers = {"Authorization": f"Bearer {CORRECT_TOKEN}"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("The service is not running on 127.0.0.1:8080")

    assert response.status_code == 200, f"Expected 200 OK with correct token, got {response.status_code}: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "department" in data, "Missing 'department' in response"
    assert data["department"] == "D1", f"Expected department 'D1', got {data['department']}"

    assert "top_earners" in data, "Missing 'top_earners' in response"
    top_earners = data["top_earners"]
    assert isinstance(top_earners, list), "'top_earners' should be a list"
    assert len(top_earners) == 3, f"Expected 3 top earners, got {len(top_earners)}"

    expected_earners = [
        {"emp_id": "E1", "team_volume": 1550.0},
        {"emp_id": "E2", "team_volume": 900.0},
        {"emp_id": "E3", "team_volume": 650.0}
    ]

    for i, expected in enumerate(expected_earners):
        actual = top_earners[i]
        assert actual.get("emp_id") == expected["emp_id"], f"Rank {i+1} expected emp_id {expected['emp_id']}, got {actual.get('emp_id')}"
        assert abs(actual.get("team_volume", 0) - expected["team_volume"]) < 1e-5, f"Rank {i+1} expected team_volume {expected['team_volume']}, got {actual.get('team_volume')}"