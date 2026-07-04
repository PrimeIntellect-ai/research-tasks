# test_final_state.py
import requests
import pytest

URL = "http://127.0.0.1:8080/api/v1/reports"
TOKEN = "SuperSecretDragon99"

def test_unauthorized_request():
    try:
        response = requests.get(URL, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {URL}: {e}")

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for missing token, got {response.status_code}"

def test_authorized_request():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        response = requests.get(URL, headers=headers, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service at {URL}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK with valid token, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response body is not valid JSON")

    assert isinstance(data, list), "Expected response JSON to be a list"
    assert len(data) == 3, f"Expected 3 deduplicated vulnerabilities, got {len(data)}"

    # Check Index 0
    assert data[0].get("cve_id") == "CVE-2023-0001", f"Expected first item to be CVE-2023-0001, got {data[0].get('cve_id')}"
    assert data[0].get("severity") == "CRITICAL", f"Expected first item severity to be CRITICAL, got {data[0].get('severity')}"

    # Check Index 1
    assert data[1].get("cve_id") == "CVE-2024-1111", f"Expected second item to be CVE-2024-1111, got {data[1].get('cve_id')}"
    assert data[1].get("severity") == "HIGH", f"Expected second item severity to be HIGH, got {data[1].get('severity')}"

    # Check Index 2
    assert data[2].get("cve_id") == "CVE-2023-0002", f"Expected third item to be CVE-2023-0002, got {data[2].get('cve_id')}"
    assert data[2].get("severity") == "MEDIUM", f"Expected third item severity to be MEDIUM, got {data[2].get('severity')}"

    endpoints = data[2].get("affected_endpoints", [])
    assert isinstance(endpoints, list), "affected_endpoints should be a list"
    assert len(endpoints) == 2, f"Expected 2 affected endpoints for CVE-2023-0002, got {len(endpoints)}"
    assert "/api/users" in endpoints, "Expected '/api/users' in affected_endpoints for CVE-2023-0002"
    assert "/api/profile" in endpoints, "Expected '/api/profile' in affected_endpoints for CVE-2023-0002"