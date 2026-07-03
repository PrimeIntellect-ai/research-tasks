# test_final_state.py

import pytest
import requests

def test_api_employees_endpoint():
    url = "http://127.0.0.1:8080/api/employees"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}. Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert isinstance(data, list), f"Expected response to be a JSON array, got {type(data)}"

    expected_data = [
        {
            "employee_id": 1,
            "name": "Alice",
            "department_name": "Engineering",
            "salary_rank": 2,
            "login_count": 2
        },
        {
            "employee_id": 2,
            "name": "Bob",
            "department_name": "Engineering",
            "salary_rank": 1,
            "login_count": 0
        },
        {
            "employee_id": 3,
            "name": "Charlie",
            "department_name": "Sales",
            "salary_rank": 1,
            "login_count": 1
        },
        {
            "employee_id": 4,
            "name": "Diana",
            "department_name": "Operations",
            "salary_rank": 1,
            "login_count": 0
        }
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} employees, got {len(data)}"

    # Check each employee matches
    for i, expected_emp in enumerate(expected_data):
        actual_emp = data[i]
        assert actual_emp.get("employee_id") == expected_emp["employee_id"], f"Mismatch at index {i}: expected employee_id {expected_emp['employee_id']}, got {actual_emp.get('employee_id')}"
        assert actual_emp.get("name") == expected_emp["name"], f"Mismatch at index {i}: expected name {expected_emp['name']}, got {actual_emp.get('name')}"
        assert actual_emp.get("department_name") == expected_emp["department_name"], f"Mismatch at index {i}: expected department_name {expected_emp['department_name']}, got {actual_emp.get('department_name')}"
        assert actual_emp.get("salary_rank") == expected_emp["salary_rank"], f"Mismatch at index {i}: expected salary_rank {expected_emp['salary_rank']}, got {actual_emp.get('salary_rank')}"

        # Handle cases where login_count might be missing if 0, but spec says it should be present
        actual_login_count = actual_emp.get("login_count", 0)
        assert actual_login_count == expected_emp["login_count"], f"Mismatch at index {i}: expected login_count {expected_emp['login_count']}, got {actual_login_count}"