# test_final_state.py

import pytest
import requests

def test_api_endpoint_failed_backups():
    """
    Test that the backup graph server is running on port 9000 and 
    returns the correctly joined results for failed backups.
    """
    url = "http://127.0.0.1:9000/api/failed_backups?date=2023-10-15"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the API at http://127.0.0.1:9000. The service is either not running or not bound to 0.0.0.0.")
    except requests.exceptions.Timeout:
        pytest.fail("The request to the API timed out.")

    assert response.status_code == 200, f"Expected HTTP 200 OK, but got {response.status_code}. Response: {response.text}"

    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, f"Expected Content-Type to be application/json, got {content_type}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Failed to parse response as JSON. Response body: {response.text}")

    assert isinstance(data, list), f"Expected the JSON response to be a list, got {type(data)}"

    # Based on the truth data, only job-102 on db-01 failed on 2023-10-15.
    expected_data = [{"serverName": "db-01", "jobId": "job-102"}]

    # Sort both lists of dicts by serverName and jobId to ensure order-independent comparison
    sorted_data = sorted(data, key=lambda x: (x.get("serverName", ""), x.get("jobId", "")))
    sorted_expected = sorted(expected_data, key=lambda x: (x.get("serverName", ""), x.get("jobId", "")))

    assert sorted_data == sorted_expected, (
        f"API returned incorrect data.\n"
        f"Expected: {sorted_expected}\n"
        f"Actual: {sorted_data}\n"
        f"If you see a Cartesian product (multiple servers for the same job), the SPARQL query join is still incorrect."
    )