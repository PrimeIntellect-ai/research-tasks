# test_final_state.py
import pytest
import requests

BASE_URL = "http://127.0.0.1:8080"

def test_api_summary():
    try:
        resp = requests.get(f"{BASE_URL}/api/summary", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the C++ HTTP service at {BASE_URL}: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert "total_size" in data, "Missing 'total_size' in /api/summary response"
    assert "total_dependencies" in data, "Missing 'total_dependencies' in /api/summary response"

    assert data["total_size"] == 1250, f"Expected total_size to be 1250, got {data['total_size']}"
    assert data["total_dependencies"] == 5, f"Expected total_dependencies to be 5, got {data['total_dependencies']}"

def test_api_critical():
    try:
        resp = requests.get(f"{BASE_URL}/api/critical", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the C++ HTTP service at {BASE_URL}: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert isinstance(data, list), f"Expected a JSON array, got {type(data)}"
    assert len(data) == 3, f"Expected exactly 3 critical backup IDs, got {len(data)}"

    # 'A' has the highest in-degree (2), so it must be in the top 3
    assert "A" in data, f"Expected 'A' to be in the top 3 critical backups, got {data}"

def test_api_backups():
    try:
        resp = requests.get(f"{BASE_URL}/api/backups", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the C++ HTTP service at {BASE_URL}: {e}")

    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert isinstance(data, list), f"Expected a JSON array, got {type(data)}"
    assert len(data) == 5, f"Expected exactly 5 backup jobs, got {len(data)}"

    for job in data:
        assert "id" in job, f"Missing 'id' in job: {job}"
        assert isinstance(job["id"], str), f"'id' should be a string in job: {job}"

        assert "depends_on" in job, f"Missing 'depends_on' in job: {job}"
        assert isinstance(job["depends_on"], list), f"'depends_on' should be an array in job: {job}"

        assert "size" in job, f"Missing 'size' in job: {job}"
        assert isinstance(job["size"], (int, float)), f"'size' should be a number in job: {job}"

        assert "criticality_score" in job, f"Missing 'criticality_score' in job: {job}"
        assert isinstance(job["criticality_score"], (int, float)), f"'criticality_score' should be a number in job: {job}"