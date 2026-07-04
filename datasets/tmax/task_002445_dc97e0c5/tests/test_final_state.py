# test_final_state.py

import sqlite3
import requests
import pytest

def get_expected_data():
    conn = sqlite3.connect("/app/data/analytics.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
    WITH UserTotals AS (
        SELECT user_id, SUM(revenue) as total_revenue
        FROM events
        GROUP BY user_id
        HAVING SUM(revenue) > 500
    ),
    CumulativeRevenue AS (
        SELECT 
            e.user_id,
            e.event_timestamp,
            SUM(e.revenue) OVER (PARTITION BY e.user_id ORDER BY e.event_timestamp) as cumulative_revenue
        FROM events e
        JOIN UserTotals ut ON e.user_id = ut.user_id
    )
    SELECT user_id, event_timestamp, cumulative_revenue
    FROM CumulativeRevenue
    ORDER BY user_id, event_timestamp
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    expected = []
    for row in rows:
        expected.append({
            "user_id": row["user_id"],
            "event_timestamp": row["event_timestamp"],
            "cumulative_revenue": row["cumulative_revenue"]
        })
    return expected

def test_api_revenue_summary():
    """Test that the API returns the correct revenue summary."""
    url = "http://127.0.0.1:8080/api/revenue_summary"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}. Ensure the server is running. Error: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"
    assert "application/json" in response.headers.get("Content-Type", ""), f"Expected Content-Type to be application/json, got {response.headers.get('Content-Type')}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON. Response: {response.text}")

    assert isinstance(data, list), f"Expected response to be a JSON array, got {type(data).__name__}"

    expected_data = get_expected_data()

    # Sort both lists by user_id and event_timestamp to compare robustly
    data_sorted = sorted(data, key=lambda x: (x.get("user_id", 0), x.get("event_timestamp", "")))
    expected_sorted = sorted(expected_data, key=lambda x: (x["user_id"], x["event_timestamp"]))

    assert len(data_sorted) == len(expected_sorted), f"Expected {len(expected_sorted)} records, got {len(data_sorted)}"

    for actual, expected in zip(data_sorted, expected_sorted):
        assert actual.get("user_id") == expected["user_id"], f"Expected user_id {expected['user_id']}, got {actual.get('user_id')}"
        assert actual.get("event_timestamp") == expected["event_timestamp"], f"Expected event_timestamp {expected['event_timestamp']}, got {actual.get('event_timestamp')}"

        actual_rev = actual.get("cumulative_revenue")
        expected_rev = expected["cumulative_revenue"]
        assert actual_rev is not None, f"Missing cumulative_revenue in response object: {actual}"

        try:
            actual_rev_float = float(actual_rev)
            expected_rev_float = float(expected_rev)
        except (ValueError, TypeError):
            pytest.fail(f"Invalid cumulative_revenue format: expected number, got {actual_rev}")

        assert abs(actual_rev_float - expected_rev_float) < 0.01, f"Expected cumulative_revenue {expected_rev_float} for user {expected['user_id']} at {expected['event_timestamp']}, got {actual_rev_float}"