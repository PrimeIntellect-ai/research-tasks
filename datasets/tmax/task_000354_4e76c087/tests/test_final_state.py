# test_final_state.py
import pytest
import requests

def test_api_schema_response():
    url = "http://127.0.0.1:8080/api/schema"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to or retrieve data from {url}. Error: {e}")

    assert response.status_code == 200, f"Expected HTTP status code 200, but got {response.status_code}. Response text: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON. Response text: {response.text}")

    expected_data = {
        "departments": ["dept_id", "dept_name", "location"],
        "employees": ["dept_id", "emp_id", "first_name", "last_name"],
        "projects": ["lead_id", "project_id", "project_name"]
    }

    assert data == expected_data, f"The returned JSON schema does not match the expected schema. Expected: {expected_data}, Got: {data}"