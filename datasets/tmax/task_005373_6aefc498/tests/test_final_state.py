# test_final_state.py

import pytest
import requests
import json
import os

URL = "http://127.0.0.1:9090/process"
TOKEN = "pineapple"

def test_source_file_exists():
    assert os.path.isfile("/home/user/etl_server.go"), "Go source file /home/user/etl_server.go is missing."

def test_auth_failure():
    """Test that missing or incorrect token returns 401 Unauthorized."""
    # Missing auth
    try:
        response = requests.post(URL, timeout=2)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the server at 127.0.0.1:9090. Is it running?")

    assert response.status_code == 401, f"Expected 401 for missing auth, got {response.status_code}"

    # Wrong auth
    headers = {"Authorization": "Bearer wrongtoken"}
    response = requests.post(URL, headers=headers, timeout=2)
    assert response.status_code == 401, f"Expected 401 for incorrect auth, got {response.status_code}"

def test_etl_processing():
    """Test the ETL pipeline with a valid token and ISO-8859-1 payload."""
    headers = {"Authorization": f"Bearer {TOKEN}"}

    csv_content = (
        "EmployeeID,FullName,Jan_Sales,Feb_Sales,Mar_Sales\n"
        "101,Renée,,2000,\n"
        "102,José,1500,1600,1700\n"
        "101,Renée,1000,2000,3000\n"
    )

    # Encode as ISO-8859-1
    csv_bytes = csv_content.encode('iso-8859-1')

    files = {
        'dataset': ('data.csv', csv_bytes, 'text/csv')
    }

    try:
        response = requests.post(URL, headers=headers, files=files, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the server at 127.0.0.1:9090.")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    expected_data = [
      {"employee_id": "101", "full_name": "RENÉE", "month": "Feb", "sales": "2000"},
      {"employee_id": "102", "full_name": "JOSÉ", "month": "Jan", "sales": "1500"},
      {"employee_id": "102", "full_name": "JOSÉ", "month": "Feb", "sales": "1600"},
      {"employee_id": "102", "full_name": "JOSÉ", "month": "Mar", "sales": "1700"},
      {"employee_id": "101", "full_name": "RENÉE", "month": "Jan", "sales": "1000"},
      {"employee_id": "101", "full_name": "RENÉE", "month": "Mar", "sales": "3000"}
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} records, got {len(data)}"

    for i, expected_row in enumerate(expected_data):
        assert data[i] == expected_row, f"Mismatch at index {i}. Expected {expected_row}, got {data[i]}"