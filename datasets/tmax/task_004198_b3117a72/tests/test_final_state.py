# test_final_state.py

import os
import csv
import pytest
import requests

def test_cleaned_detections_csv():
    path = "/home/user/cleaned_detections.csv"
    assert os.path.isfile(path), f"Missing required file: {path}"

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "Cleaned CSV is empty"
    header = rows[0]
    expected_header = ["frame_id", "object_id", "x", "y", "w", "h", "area"]
    assert header == expected_header, f"Expected header {expected_header}, got {header}"

    # We expect specific rows based on the truth data
    # 1,101,10,10,50,50,2500
    # 3,102,5,5,10,10,100
    # 12,101,15,15,50,60,3000

    data_rows = rows[1:]
    assert len(data_rows) == 3, f"Expected 3 data rows, got {len(data_rows)}"

    assert data_rows[0] == ["1", "101", "10", "10", "50", "50", "2500"], "Row 1 mismatch"
    assert data_rows[1] == ["3", "102", "5", "5", "10", "10", "100"], "Row 2 mismatch"
    assert data_rows[2] == ["12", "101", "15", "15", "50", "60", "3000"], "Row 3 mismatch"

def test_experiments_log():
    path = "/home/user/experiments.log"
    assert os.path.isfile(path), f"Missing required file: {path}"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "Total Frames: 10" in content, f"Expected 'Total Frames: 10' in {path}, got:\n{content}"

def test_api_area_endpoint():
    url = "http://127.0.0.1:8080/area"

    # Test object_id=101
    resp1 = requests.get(url, params={"object_id": "101"}, timeout=5)
    assert resp1.status_code == 200, f"Expected 200 OK, got {resp1.status_code}"
    assert resp1.text.strip() == "5500", f"Expected '5500', got '{resp1.text}'"

    # Test object_id=102
    resp2 = requests.get(url, params={"object_id": "102"}, timeout=5)
    assert resp2.status_code == 200, f"Expected 200 OK, got {resp2.status_code}"
    assert resp2.text.strip() == "100", f"Expected '100', got '{resp2.text}'"

def test_api_secure_stats_endpoint():
    url = "http://127.0.0.1:8080/secure_stats"

    # Test without auth
    resp_no_auth = requests.get(url, timeout=5)
    assert resp_no_auth.status_code == 401, f"Expected 401 Unauthorized, got {resp_no_auth.status_code}"

    # Test with auth
    headers = {"Authorization": "Bearer ds_token_2024"}
    resp_auth = requests.get(url, headers=headers, timeout=5)
    assert resp_auth.status_code == 200, f"Expected 200 OK, got {resp_auth.status_code}"

    try:
        data = resp_auth.json()
    except ValueError:
        pytest.fail(f"Expected JSON response, got '{resp_auth.text}'")

    assert data == {"status": "ok"}, f"Expected {{'status': 'ok'}}, got {data}"