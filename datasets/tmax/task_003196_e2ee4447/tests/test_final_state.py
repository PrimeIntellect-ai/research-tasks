# test_final_state.py

import requests
import pytest

def test_audit_report_endpoint():
    """
    Test that the HTTP server is running on 127.0.0.1:8080 and serves the correct
    audit report as JSON at the /audit-report endpoint.
    """
    url = "http://127.0.0.1:8080/audit-report"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}. Is the Bash server running? Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type to contain 'application/json', got '{content_type}'"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON. Body received:\n{response.text}")

    expected_data = [
        {
            "target_node": "EXT-99",
            "department": "Vendor-Cloud",
            "total_scp_bytes": 3000
        },
        {
            "target_node": "EXT-88",
            "department": "Offshore-Contractors",
            "total_scp_bytes": 1700
        }
    ]

    assert isinstance(data, list), f"Expected response JSON to be a list, got {type(data).__name__}"
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items in the list, got {len(data)}"

    assert data == expected_data, f"JSON data does not match expected output.\nExpected: {expected_data}\nGot: {data}"