# test_final_state.py

import os
import sqlite3
import pytest
import requests

def get_db_breaches():
    conn = sqlite3.connect('/app/compliance.db')
    cursor = conn.cursor()
    # Correct join to find actual unauthorized access
    cursor.execute("""
        SELECT e.emp_id 
        FROM employees e 
        JOIN room_access r ON e.emp_id = r.emp_id 
        WHERE e.clearance != 'TOP_SECRET' AND r.room = 'ServerRoom'
    """)
    breaches = {row[0] for row in cursor.fetchall()}
    conn.close()
    return breaches

def test_db_breaches_file():
    expected_db_breaches = get_db_breaches()
    file_path = '/home/user/db_breaches.txt'

    assert os.path.exists(file_path), f"File not found: {file_path}"

    with open(file_path, 'r') as f:
        actual_db_breaches = {line.strip() for line in f if line.strip()}

    assert actual_db_breaches == expected_db_breaches, \
        f"Expected DB breaches {expected_db_breaches}, got {actual_db_breaches}"

def test_video_breaches_file():
    # From truth data: EMP801 and EMP805 are in the 00:00:10 to 00:00:25 window
    expected_video_breaches = {"EMP801", "EMP805"}
    file_path = '/home/user/video_breaches.txt'

    assert os.path.exists(file_path), f"File not found: {file_path}"

    with open(file_path, 'r') as f:
        actual_video_breaches = {line.strip() for line in f if line.strip()}

    assert actual_video_breaches == expected_video_breaches, \
        f"Expected video breaches {expected_video_breaches}, got {actual_video_breaches}"

def test_import_cypher_file():
    all_breaches = get_db_breaches()
    all_breaches.update({"EMP801", "EMP805"})

    file_path = '/home/user/import.cypher'
    assert os.path.exists(file_path), f"File not found: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read()

    for emp_id in all_breaches:
        expected_stmt = f'MERGE (e:Employee {{emp_id: "{emp_id}"}}) MERGE (r:Room {{name: "ServerRoom"}}) MERGE (e)-[:UNAUTHORIZED_ACCESS]->(r);'
        assert expected_stmt in content, f"Missing or incorrect Cypher statement for {emp_id}"

def test_http_server():
    all_breaches = get_db_breaches()
    all_breaches.update({"EMP801", "EMP805"})

    breach_id = list(all_breaches)[0] if all_breaches else "EMP042"
    non_breach_id = "EMP999"

    base_url = "http://127.0.0.1:8080/check"

    # Test 1: Unauthorized missing/wrong token
    try:
        resp = requests.get(f"{base_url}?emp_id={breach_id}", headers={"Authorization": "Bearer WRONG_TOKEN"}, timeout=2)
        assert resp.status_code == 401, f"Expected HTTP 401 for wrong token, got {resp.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP server is not reachable or failed on wrong token: {e}")

    # Test 2: Breach ID
    try:
        resp = requests.get(f"{base_url}?emp_id={breach_id}", headers={"Authorization": "Bearer AUDIT_SECURE_99"}, timeout=2)
        assert resp.status_code == 200, f"Expected HTTP 200 for breach ID, got {resp.status_code}"
        assert "STATUS: BREACH" in resp.text, f"Expected 'STATUS: BREACH' in response, got '{resp.text}'"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP server failed on breach ID request: {e}")

    # Test 3: Clear ID
    try:
        resp = requests.get(f"{base_url}?emp_id={non_breach_id}", headers={"Authorization": "Bearer AUDIT_SECURE_99"}, timeout=2)
        assert resp.status_code == 200, f"Expected HTTP 200 for clear ID, got {resp.status_code}"
        assert "STATUS: CLEAR" in resp.text, f"Expected 'STATUS: CLEAR' in response, got '{resp.text}'"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP server failed on clear ID request: {e}")