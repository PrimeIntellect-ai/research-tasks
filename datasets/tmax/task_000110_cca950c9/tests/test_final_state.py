# test_final_state.py
import subprocess
import json
import requests
import time
import pytest

def test_api_subordinates_page_1():
    url = "http://127.0.0.1:8000/api/subordinates?manager_id=1&page=1&limit=3"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API on 127.0.0.1:8000: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("API response is not valid JSON")

    expected = [
        {"_id": 2, "name": "Bob", "managerId": 1},
        {"_id": 3, "name": "Charlie", "managerId": 1},
        {"_id": 4, "name": "David", "managerId": 2}
    ]

    assert len(data) == 3, f"Expected 3 records, got {len(data)}"
    for i, exp in enumerate(expected):
        assert data[i]["_id"] == exp["_id"], f"Record {i} _id mismatch"
        assert data[i]["name"] == exp["name"], f"Record {i} name mismatch"
        assert data[i]["managerId"] == exp["managerId"], f"Record {i} managerId mismatch"

def test_api_subordinates_page_2():
    url = "http://127.0.0.1:8000/api/subordinates?manager_id=1&page=2&limit=3"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API on 127.0.0.1:8000: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("API response is not valid JSON")

    expected = [
        {"_id": 5, "name": "Eve", "managerId": 2},
        {"_id": 6, "name": "Frank", "managerId": 3},
        {"_id": 7, "name": "Grace", "managerId": 3}
    ]

    assert len(data) == 3, f"Expected 3 records, got {len(data)}"
    for i, exp in enumerate(expected):
        assert data[i]["_id"] == exp["_id"], f"Record {i} _id mismatch"
        assert data[i]["name"] == exp["name"], f"Record {i} name mismatch"
        assert data[i]["managerId"] == exp["managerId"], f"Record {i} managerId mismatch"

def test_mongodb_index_exists():
    cmd = [
        "mongosh", "corp", "--quiet", "--eval",
        "JSON.stringify(db.employees.getIndexes())"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to execute mongosh command: {e.stderr}")

    try:
        indexes = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Failed to parse mongosh output as JSON: {result.stdout}")

    has_manager_id_index = False
    for idx in indexes:
        if "managerId" in idx.get("key", {}) and idx["key"]["managerId"] == 1:
            has_manager_id_index = True
            break

    assert has_manager_id_index, "Ascending index on managerId is missing in corp.employees"