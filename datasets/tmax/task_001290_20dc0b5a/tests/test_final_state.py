# test_final_state.py

import os
import sqlite3
import subprocess
import pytest
import requests

def test_c_library_linked_correctly():
    lib_path = '/home/user/mathlib/libmathops.so'
    assert os.path.isfile(lib_path), f"{lib_path} does not exist. Did you recompile the library?"

    # Check if the shared library is linked against the math library (libm)
    result = subprocess.run(['ldd', lib_path], capture_output=True, text=True)
    assert 'libm.so' in result.stdout, "libmathops.so is not linked against the standard math library (libm.so). Check your Makefile."

def test_database_schema_migrated():
    db_path = '/home/user/db/metrics.db'
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(video_stats);")
    columns = [col[1] for col in cursor.fetchall()]
    conn.close()

    assert 'max_variation' in columns, "Column 'max_variation' was not added to the video_stats table."

def test_api_process_and_database_insertion():
    url = "http://127.0.0.1:8000/api/v1/process"
    try:
        response = requests.get(url, timeout=15)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the FastAPI service at {url}. Is it running? Error: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert data.get("status") == "ok", f"Expected status 'ok', got '{data.get('status')}'"
    assert "max_variation" in data, "Response JSON is missing the 'max_variation' key."

    api_max_variation = data["max_variation"]
    assert isinstance(api_max_variation, (int, float)), f"Expected max_variation to be a number, got {type(api_max_variation)}"

    # Now verify that the database was updated with this result
    db_path = '/home/user/db/metrics.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT filename, max_variation FROM video_stats WHERE filename = 'video.mp4' ORDER BY id DESC LIMIT 1;")
    row = cursor.fetchone()
    conn.close()

    assert row is not None, "No row found for 'video.mp4' in the video_stats table after calling the API."
    db_filename, db_max_variation = row
    assert db_filename == 'video.mp4', f"Expected filename 'video.mp4', got '{db_filename}'"

    # Allow for minor floating point differences if any
    assert abs(db_max_variation - api_max_variation) < 1e-5, f"Database max_variation ({db_max_variation}) does not match API response ({api_max_variation})."