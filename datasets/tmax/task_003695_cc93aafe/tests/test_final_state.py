# test_final_state.py

import sqlite3
import requests
import pytest

PORT = 8123
TOKEN = "AlphaBravo123"
URL = f"http://127.0.0.1:{PORT}/api/v1/datasets/stats"

def get_expected_data():
    """Derive the expected JSON response from the current state of the database."""
    conn = sqlite3.connect('/app/datasets.db')
    c = conn.cursor()
    c.execute('''
        SELECT c.name, a.full_name, m.metric_value
        FROM tbl_collections c
        JOIN tbl_authors a ON c.author_id = a.id
        LEFT JOIN tbl_metrics m ON m.col_id = c.id
    ''')
    rows = c.fetchall()
    conn.close()

    data = {}
    for c_name, a_name, m_val in rows:
        if c_name not in data:
            data[c_name] = {'author': a_name, 'metrics': []}
        if m_val is not None:
            data[c_name]['metrics'].append(m_val)

    results = []
    for c_name in sorted(data.keys()):
        metrics = sorted(data[c_name]['metrics'], reverse=True)[:2]
        results.append({
            "dataset_name": c_name,
            "author_name": data[c_name]['author'],
            "top_metrics": metrics
        })
    return {"results": results}

def test_api_no_auth():
    """Test that the API returns 401 when no authorization header is provided."""
    try:
        resp = requests.get(URL, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API at {URL}: {e}")

    assert resp.status_code == 401, f"Expected 401 Unauthorized without token, got {resp.status_code}. Response: {resp.text}"

def test_api_invalid_auth():
    """Test that the API returns 401 when an invalid authorization header is provided."""
    headers = {"Authorization": "Bearer InvalidToken"}
    try:
        resp = requests.get(URL, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API at {URL}: {e}")

    assert resp.status_code == 401, f"Expected 401 Unauthorized with invalid token, got {resp.status_code}. Response: {resp.text}"

def test_api_valid_auth_and_data():
    """Test that the API returns 200 and the correct JSON data when a valid token is provided."""
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        resp = requests.get(URL, headers=headers, timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to API at {URL}: {e}")

    assert resp.status_code == 200, f"Expected 200 OK with valid token, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    expected = get_expected_data()
    assert data == expected, f"API response data did not match expected data.\nExpected: {expected}\nGot: {data}"