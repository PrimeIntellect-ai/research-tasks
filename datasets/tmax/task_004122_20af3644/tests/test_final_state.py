# test_final_state.py
import pytest
import requests

BASE_URL = "http://127.0.0.1:8443"

def test_audit_alice():
    url = f"{BASE_URL}/api/v1/audit/alice"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()

    assert data.get("user_id") == "alice", "Incorrect user_id for alice"
    assert sorted(data.get("effective_permissions", [])) == ["APPROVE_TRANSFER", "FUNDS_TRANSFER", "GENERATE_REPORT", "VIEW_LEDGER"], "Incorrect effective_permissions for alice"
    assert data.get("is_compliant") is False, "is_compliant should be false for alice"
    # The toxic pair can be in any order, so we sort it
    assert sorted(data.get("toxic_pair", [])) == ["APPROVE_TRANSFER", "FUNDS_TRANSFER"], "Incorrect toxic_pair for alice"

def test_audit_bob():
    url = f"{BASE_URL}/api/v1/audit/bob"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()

    assert data.get("user_id") == "bob", "Incorrect user_id for bob"
    assert sorted(data.get("effective_permissions", [])) == ["GENERATE_REPORT", "VIEW_LEDGER"], "Incorrect effective_permissions for bob"
    assert data.get("is_compliant") is True, "is_compliant should be true for bob"
    assert data.get("toxic_pair") == [], "toxic_pair should be empty for bob"

def test_audit_diana():
    url = f"{BASE_URL}/api/v1/audit/diana"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()

    assert data.get("user_id") == "diana", "Incorrect user_id for diana"
    assert sorted(data.get("effective_permissions", [])) == ["CREATE_VENDOR", "PAY_VENDOR"], "Incorrect effective_permissions for diana"
    assert data.get("is_compliant") is False, "is_compliant should be false for diana"
    assert sorted(data.get("toxic_pair", [])) == ["CREATE_VENDOR", "PAY_VENDOR"], "Incorrect toxic_pair for diana"

def test_stats_centrality():
    url = f"{BASE_URL}/api/v1/stats/centrality"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()

    assert isinstance(data, list), "Expected a JSON array"
    assert len(data) == 3, f"Expected top 3 permissions, got {len(data)}"

    # We expect CREATE_VENDOR: 2, GENERATE_REPORT: 2, VIEW_LEDGER: 2
    # Order doesn't matter for the test if they are tied, but they should all have count 2
    expected_perms = {"CREATE_VENDOR", "GENERATE_REPORT", "VIEW_LEDGER"}

    actual_perms = set()
    for item in data:
        assert "permission" in item, "Missing 'permission' key in centrality stats"
        assert "user_count" in item, "Missing 'user_count' key in centrality stats"
        assert item["user_count"] == 2, f"Expected user_count 2 for {item['permission']}, got {item['user_count']}"
        actual_perms.add(item["permission"])

    assert actual_perms == expected_perms, f"Expected permissions {expected_perms}, got {actual_perms}"