# test_final_state.py
import sqlite3
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080/api/audit/summary"
AUTH_HEADER = {"Authorization": "Bearer ComplianceAudit2024"}
DB_PATH = "/home/user/audit.db"

def get_expected_totals(emp_id):
    """Derive the expected totals directly from the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE emp_id = ?", (emp_id,))
    tx_amount = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM access_logs WHERE emp_id = ?", (emp_id,))
    access_count = c.fetchone()[0]
    conn.close()
    return tx_amount, access_count

def test_auth_missing():
    """Ensure the endpoint returns 401 when Authorization header is missing."""
    try:
        resp = requests.get(f"{BASE_URL}?emp_id=1", timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert resp.status_code == 401, f"Expected 401 Unauthorized for missing auth, got {resp.status_code}. Response: {resp.text}"

def test_auth_invalid():
    """Ensure the endpoint returns 401 when Authorization header is incorrect."""
    headers = {"Authorization": "Bearer WrongToken123"}
    try:
        resp = requests.get(f"{BASE_URL}?emp_id=1", headers=headers, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert resp.status_code == 401, f"Expected 401 Unauthorized for invalid auth, got {resp.status_code}. Response: {resp.text}"

@pytest.mark.parametrize("emp_id", [1, 2, 3])
def test_valid_employee_summaries(emp_id):
    """Test that the endpoint correctly aggregates data without cross-joining."""
    expected_tx, expected_access = get_expected_totals(emp_id)

    try:
        resp = requests.get(f"{BASE_URL}?emp_id={emp_id}", headers=AUTH_HEADER, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    assert resp.status_code == 200, f"Expected 200 OK for emp_id={emp_id}, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert data.get("emp_id") == emp_id, f"Expected emp_id {emp_id}, got {data.get('emp_id')}"

    actual_tx = data.get("total_tx_amount", 0)
    assert abs(actual_tx - expected_tx) < 0.01, f"Expected total_tx_amount {expected_tx}, got {actual_tx} (possible cross-join bug?)"

    actual_access = data.get("total_access_count")
    assert actual_access == expected_access, f"Expected total_access_count {expected_access}, got {actual_access} (possible cross-join bug?)"

def test_sql_injection_resilience():
    """Test that the endpoint is resilient to basic SQL injection on the emp_id parameter."""
    payload = "1 OR 1=1"
    try:
        resp = requests.get(f"{BASE_URL}?emp_id={payload}", headers=AUTH_HEADER, timeout=2)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    # It is acceptable to return 400 (Bad Request), 404 (Not Found), or 422 (Unprocessable Entity)
    if resp.status_code in [400, 404, 422]:
        return # Passed

    # If it returns 200, it must not return aggregated data for all users
    if resp.status_code == 200:
        try:
            data = resp.json()
        except ValueError:
            pytest.fail(f"Response is not valid JSON: {resp.text}")

        # Alice's expected tx amount is ~150.50. If it sums everyone, it will be much larger (> 900).
        actual_tx = data.get("total_tx_amount", 0)
        assert actual_tx < 200, f"SQL injection appears successful! Aggregated amount is {actual_tx}, expected <= 150.50"
    else:
        pytest.fail(f"Unexpected status code {resp.status_code} for SQL injection test. Expected 400/404/422 or a safe 200.")