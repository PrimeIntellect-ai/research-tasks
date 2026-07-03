# test_final_state.py

import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"
AUTH_HEADER = {"Authorization": "Bearer SecureGraphETL2024"}

def test_api_unauthorized():
    """Test that requests without the correct authorization header are rejected with 401."""
    try:
        response = requests.get(f"{BASE_URL}/summary?dept=Sales", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API server at {BASE_URL}: {e}")

    assert response.status_code == 401, (
        f"Expected HTTP 401 Unauthorized when no token is provided, "
        f"but got {response.status_code}. Response: {response.text}"
    )

def test_api_sales_summary():
    """Test the summary endpoint for the Sales department."""
    try:
        response = requests.get(f"{BASE_URL}/summary?dept=Sales", headers=AUTH_HEADER, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API server at {BASE_URL}: {e}")

    assert response.status_code == 200, (
        f"Expected HTTP 200 OK for Sales summary, but got {response.status_code}. "
        f"Response: {response.text}"
    )

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, but failed to parse: {response.text}")

    assert data.get("department") == "Sales", f"Expected department 'Sales', got {data.get('department')}"
    assert data.get("manager") == "Bob", f"Expected manager 'Bob', got {data.get('manager')}"
    assert data.get("employee_count") == 2, f"Expected employee_count 2, got {data.get('employee_count')}"
    assert data.get("total_salary") == 140000, f"Expected total_salary 140000, got {data.get('total_salary')}"

def test_api_engineering_summary():
    """Test the summary endpoint for the Engineering department."""
    try:
        response = requests.get(f"{BASE_URL}/summary?dept=Engineering", headers=AUTH_HEADER, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API server at {BASE_URL}: {e}")

    assert response.status_code == 200, (
        f"Expected HTTP 200 OK for Engineering summary, but got {response.status_code}. "
        f"Response: {response.text}"
    )

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, but failed to parse: {response.text}")

    assert data.get("department") == "Engineering", f"Expected department 'Engineering', got {data.get('department')}"
    assert data.get("manager") == "Alice", f"Expected manager 'Alice', got {data.get('manager')}"
    assert data.get("employee_count") == 3, f"Expected employee_count 3, got {data.get('employee_count')}"
    assert data.get("total_salary") == 280000, f"Expected total_salary 280000, got {data.get('total_salary')}"