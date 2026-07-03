# test_final_state.py

import os
import sqlite3
import pytest
import requests
import time

API_URL = "http://127.0.0.1:8080/api/backups"
TOKEN = "BRAVO-992-SECURE"

def wait_for_service():
    """Wait briefly for the service to be ready."""
    for _ in range(10):
        if os.path.exists('/home/user/service_ready.txt'):
            return True
        time.sleep(0.5)
    return False

def get_expected_data(tenant_id, page, limit):
    conn = sqlite3.connect('/app/backup_catalog.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM backups WHERE tenant_id=?", (tenant_id,))
    total_records = c.fetchone()[0]

    offset = (page - 1) * limit
    c.execute("""
        SELECT datastore_type, file_path, backup_timestamp, size_bytes 
        FROM backups 
        WHERE tenant_id=? 
        ORDER BY backup_timestamp DESC 
        LIMIT ? OFFSET ?
    """, (tenant_id, limit, offset))
    rows = c.fetchall()

    recovery_plan = {}
    for row in rows:
        ds_type = row[0]
        key = f"{ds_type}_backups"
        if key not in recovery_plan:
            recovery_plan[key] = []
        recovery_plan[key].append({
            "path": row[1],
            "timestamp": row[2],
            "size_mb": round(row[3] / (1024 * 1024), 2)
        })

    conn.close()

    return {
        "request_metadata": {
            "tenant_id": tenant_id,
            "page": page,
            "limit": limit,
            "total_records": total_records
        },
        "recovery_plan": recovery_plan
    }

@pytest.fixture(autouse=True)
def check_service_ready():
    assert wait_for_service(), "Service ready signal file (/home/user/service_ready.txt) not found."

def test_unauthorized_no_token():
    response = requests.get(f"{API_URL}?tenant_id=ALPHA-774")
    assert response.status_code == 401, f"Expected 401 Unauthorized when missing token, got {response.status_code}. Response: {response.text}"

def test_unauthorized_wrong_token():
    headers = {"Authorization": "Bearer WRONG-TOKEN"}
    response = requests.get(f"{API_URL}?tenant_id=ALPHA-774", headers=headers)
    assert response.status_code == 401, f"Expected 401 Unauthorized with wrong token, got {response.status_code}. Response: {response.text}"

def test_valid_request_schema_and_data():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    tenant_id = "ALPHA-774"
    page = 1
    limit = 2

    response = requests.get(f"{API_URL}?tenant_id={tenant_id}&page={page}&limit={limit}", headers=headers)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON. Response: {response.text}")

    expected_data = get_expected_data(tenant_id, page, limit)

    assert data == expected_data, f"JSON response does not match expected schema/data.\nExpected: {expected_data}\nGot: {data}"

def test_valid_request_page_2():
    headers = {"Authorization": f"Bearer {TOKEN}"}
    tenant_id = "ALPHA-774"
    page = 2
    limit = 2

    response = requests.get(f"{API_URL}?tenant_id={tenant_id}&page={page}&limit={limit}", headers=headers)
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    data = response.json()
    expected_data = get_expected_data(tenant_id, page, limit)

    assert data == expected_data, f"JSON response does not match expected schema/data for page 2.\nExpected: {expected_data}\nGot: {data}"