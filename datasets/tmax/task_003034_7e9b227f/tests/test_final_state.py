# test_final_state.py
import os
import requests
import pytest

def test_incident_report_exists():
    report_path = "/home/user/incident_report.log"
    assert os.path.exists(report_path), f"Incident report not found at {report_path}"
    assert os.path.getsize(report_path) > 0, "Incident report is empty"

def test_recommendation_api_all_users():
    base_url = "http://127.0.0.1:8000/recommend/"
    headers = {"X-Auth-Token": "emergency-bypass"}

    # Test user IDs 1 through 100, which includes multiples of 7 (the bug trigger)
    for user_id in range(1, 101):
        url = f"{base_url}{user_id}"
        try:
            response = requests.get(url, headers=headers, timeout=5)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request to API Gateway failed for user_id {user_id}: {e}")

        assert response.status_code == 200, f"Expected status 200 for user_id {user_id}, got {response.status_code}. Response: {response.text}"

        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Response for user_id {user_id} is not valid JSON. Response: {response.text}")

        assert "user_id" in data, f"Missing 'user_id' in response for user_id {user_id}"
        assert data["user_id"] == user_id, f"Expected user_id {user_id} in response, got {data.get('user_id')}"
        assert "recommendations" in data, f"Missing 'recommendations' in response for user_id {user_id}"
        assert isinstance(data["recommendations"], list), f"'recommendations' should be a list for user_id {user_id}"