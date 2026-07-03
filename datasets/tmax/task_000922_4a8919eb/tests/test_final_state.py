# test_final_state.py

import sqlite3
import requests
import pytest
import math

BASE_URL = "http://127.0.0.1:8080"

def test_db_epochs_populated():
    """Verify that the epochs table in metadata.db has been populated correctly."""
    db_path = "/app/metadata.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT epoch_index, activity_level FROM epochs WHERE subject_id=1 ORDER BY epoch_index ASC;")
    rows = cursor.fetchall()
    conn.close()

    assert len(rows) >= 5, f"Expected at least 5 epochs in the database, found {len(rows)}"

    expected_activities = {
        0: 0,
        1: 128,
        2: 255,
        3: 102,
        4: 191
    }

    for epoch_index, activity_level in rows:
        if epoch_index in expected_activities:
            expected = expected_activities[epoch_index]
            assert math.isclose(activity_level, expected, abs_tol=15), \
                f"Epoch {epoch_index} activity level {activity_level} is not close to expected {expected}"

def test_api_path_a_to_d():
    """Verify the /path endpoint computes the correct shortest path from A to D."""
    try:
        response = requests.get(f"{BASE_URL}/path?start=A&end=D", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {BASE_URL}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from /path is not valid JSON: {response.text}")

    assert "path" in data, "Response JSON missing 'path' key"
    assert "cost" in data, "Response JSON missing 'cost' key"

    expected_path = ["A", "C", "B", "D"]
    expected_cost = 9

    assert data["path"] == expected_path, f"Expected path {expected_path}, got {data['path']}"
    assert data["cost"] == expected_cost, f"Expected cost {expected_cost}, got {data['cost']}"

def test_api_path_c_to_a():
    """Verify the /path endpoint computes the correct shortest path from C to A."""
    try:
        response = requests.get(f"{BASE_URL}/path?start=C&end=A", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP server at {BASE_URL}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response from /path is not valid JSON: {response.text}")

    expected_path = ["C", "E", "A"]
    expected_cost = 9

    assert data["path"] == expected_path, f"Expected path {expected_path}, got {data['path']}"
    assert data["cost"] == expected_cost, f"Expected cost {expected_cost}, got {data['cost']}"

def test_api_activity():
    """Verify the /activity endpoint retrieves the correct epoch activity level."""
    expected_activities = {
        0: 0,
        1: 128,
        2: 255,
        3: 102,
        4: 191
    }

    for epoch, expected in expected_activities.items():
        try:
            response = requests.get(f"{BASE_URL}/activity?epoch={epoch}", timeout=5)
        except requests.RequestException as e:
            pytest.fail(f"Failed to connect to the HTTP server at {BASE_URL}: {e}")

        assert response.status_code == 200, f"Expected status code 200 for epoch {epoch}, got {response.status_code}. Response: {response.text}"

        try:
            data = response.json()
        except ValueError:
            pytest.fail(f"Response from /activity is not valid JSON: {response.text}")

        assert "epoch" in data, "Response JSON missing 'epoch' key"
        assert "activity" in data, "Response JSON missing 'activity' key"

        assert int(data["epoch"]) == epoch, f"Expected epoch {epoch}, got {data['epoch']}"
        assert math.isclose(float(data["activity"]), expected, abs_tol=15), \
            f"Expected activity for epoch {epoch} to be close to {expected}, got {data['activity']}"