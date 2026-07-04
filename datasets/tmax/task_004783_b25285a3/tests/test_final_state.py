# test_final_state.py
import os
import sqlite3
import requests
import pytest

BASE_URL = "http://127.0.0.1:8080"

def test_shared_library_exists():
    assert os.path.isfile("/app/bin/libaudiofeat.so"), "/app/bin/libaudiofeat.so does not exist. Did you compile the C library?"

def test_database_exists():
    assert os.path.isfile("/app/data/ci_service.db"), "/app/data/ci_service.db does not exist. Did you run the schema migrations?"

def test_server_log_exists():
    assert os.path.isfile("/app/logs/server.log"), "/app/logs/server.log does not exist. Is the server logging to this file?"

def test_database_schema():
    conn = sqlite3.connect("/app/data/ci_service.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(jobs)")
    columns = {row[1] for row in cursor.fetchall()}
    conn.close()

    expected_columns = {"id", "filepath", "feature_value", "status"}
    missing = expected_columns - columns
    assert not missing, f"Database table 'jobs' is missing columns: {missing}. Did you apply all migrations?"

def test_api_process_and_get():
    # Test POST /process
    payload = {"filepath": "/app/test_audio.wav"}
    try:
        resp_post = requests.post(f"{BASE_URL}/process", json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to POST /process: {e}")

    assert resp_post.status_code in (200, 201), f"Expected HTTP 200/201 from POST /process, got {resp_post.status_code}. Response: {resp_post.text}"

    try:
        data_post = resp_post.json()
    except Exception:
        pytest.fail(f"POST /process did not return valid JSON. Response: {resp_post.text}")

    assert "job_id" in data_post, f"POST /process response missing 'job_id'. Response: {data_post}"
    job_id = data_post["job_id"]

    # Test GET /job/<job_id>
    try:
        resp_get = requests.get(f"{BASE_URL}/job/{job_id}", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to GET /job/{job_id}: {e}")

    assert resp_get.status_code == 200, f"Expected HTTP 200 from GET /job/{job_id}, got {resp_get.status_code}. Response: {resp_get.text}"

    try:
        data_get = resp_get.json()
    except Exception:
        pytest.fail(f"GET /job/{job_id} did not return valid JSON. Response: {resp_get.text}")

    assert data_get.get("filepath") == "/app/test_audio.wav", f"Expected filepath '/app/test_audio.wav', got {data_get.get('filepath')}"

    # Calculate expected feature value dynamically
    try:
        size = os.path.getsize("/app/test_audio.wav")
        expected_feature = float(size % 1000) + 0.5
    except Exception:
        expected_feature = 24.5 # Fallback if file is missing or error

    assert data_get.get("feature_value") == expected_feature, f"Expected feature_value {expected_feature}, got {data_get.get('feature_value')}"
    assert data_get.get("status") == "COMPLETED", f"Expected status 'COMPLETED', got {data_get.get('status')}"

def test_api_get_not_found():
    try:
        resp_404 = requests.get(f"{BASE_URL}/job/999999", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to GET /job/999999: {e}")

    assert resp_404.status_code == 404, f"Expected HTTP 404 for missing job, got {resp_404.status_code}. Response: {resp_404.text}"