# test_final_state.py

import os
import sqlite3
import subprocess
import pytest
import requests
import time

BASE_URL = "http://127.0.0.1:5000"

@pytest.fixture(scope="session", autouse=True)
def wait_for_server():
    """Wait for the server to be up before running tests."""
    max_retries = 10
    for _ in range(max_retries):
        try:
            requests.get(BASE_URL)
            return
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    pytest.fail("Server did not start on 127.0.0.1:5000")

def get_expected_embedding(description):
    """Run the binary to get the expected embedding for a description."""
    bin_path = "/app/scorer_bin"
    result = subprocess.run([bin_path, description], capture_output=True, text=True, check=True)
    return [float(x) for x in result.stdout.strip().split()]

def test_upload_and_validation():
    csv_content = """id,category,description,metric
1,ALPHA,test description,4.5
2,DELTA,invalid category row,1.0
3,BETA,another valid row,0.0
4,GAMMA,negative metric,-1.2
5,GAMMA,valid again,10.1
"""
    files = {'file': ('test.csv', csv_content, 'text/csv')}
    response = requests.post(f"{BASE_URL}/upload", files=files)
    assert response.status_code == 200, f"Expected 200 OK for upload, got {response.status_code}. Response: {response.text}"

def test_get_valid_records():
    valid_records = [
        (1, "ALPHA", "test description", 4.5),
        (3, "BETA", "another valid row", 0.0),
        (5, "GAMMA", "valid again", 10.1)
    ]

    for rec_id, category, description, metric in valid_records:
        response = requests.get(f"{BASE_URL}/record/{rec_id}")
        assert response.status_code == 200, f"Expected 200 OK for record {rec_id}, got {response.status_code}"

        data = response.json()
        assert data.get("id") == rec_id, f"Expected id {rec_id}, got {data.get('id')}"
        assert data.get("category") == category, f"Expected category {category}, got {data.get('category')}"
        assert data.get("description") == description, f"Expected description '{description}', got {data.get('description')}"
        assert float(data.get("metric")) == metric, f"Expected metric {metric}, got {data.get('metric')}"

        expected_embedding = get_expected_embedding(description)
        actual_embedding = data.get("embedding")
        assert isinstance(actual_embedding, list) and len(actual_embedding) == 4, "Embedding must be a list of 4 floats"

        for exp, act in zip(expected_embedding, actual_embedding):
            assert abs(exp - act) <= 0.0001, f"Embedding mismatch for record {rec_id}. Expected {expected_embedding}, got {actual_embedding}"

def test_get_invalid_records():
    invalid_ids = [2, 4]
    for rec_id in invalid_ids:
        response = requests.get(f"{BASE_URL}/record/{rec_id}")
        assert response.status_code == 404, f"Expected 404 Not Found for record {rec_id}, got {response.status_code}"

def test_database_state():
    db_path = "/home/user/data.db"
    assert os.path.exists(db_path), f"Database file {db_path} does not exist"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table schema
    cursor.execute("PRAGMA table_info(records)")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}

    expected_columns = {
        'id': 'INTEGER',
        'category': 'TEXT',
        'description': 'TEXT',
        'metric': 'REAL',
        'emb_0': 'REAL',
        'emb_1': 'REAL',
        'emb_2': 'REAL',
        'emb_3': 'REAL'
    }

    for col, col_type in expected_columns.items():
        assert col in columns, f"Column '{col}' missing from records table"
        assert col_type in columns[col], f"Column '{col}' has incorrect type. Expected {col_type}, got {columns[col]}"

    # Check row counts
    cursor.execute("SELECT COUNT(*) FROM records")
    count = cursor.fetchone()[0]
    # At least 3 valid rows should be present (maybe more if test run multiple times, but 3 from our upload)
    assert count >= 3, f"Expected at least 3 records in database, got {count}"

    conn.close()