# test_final_state.py
import json
import os
import sqlite3
import pytest

DB_PATH = "/home/user/research.db"
RESULTS_PATH = "/home/user/results.json"

def get_expected_results():
    """Dynamically compute the expected results from the SQLite database."""
    assert os.path.exists(DB_PATH), f"Database file missing at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get nodes targeted by 'depends_on' from 'ROOT'
    cursor.execute("""
        SELECT target 
        FROM edges 
        WHERE source = 'ROOT' AND relation = 'depends_on'
    """)
    target_nodes = [row['target'] for row in cursor.fetchall()]

    expected_data = []

    for node in target_nodes:
        # Get metrics for the node, ordered by recorded_at
        cursor.execute("""
            SELECT recorded_at, score
            FROM metrics
            WHERE node_id = ?
            ORDER BY recorded_at ASC
        """, (node,))

        cumulative_score = 0.0
        for row in cursor.fetchall():
            cumulative_score += row['score']
            if cumulative_score >= 0.0:
                expected_data.append({
                    "node_id": node,
                    "recorded_at": row['recorded_at'],
                    "cumulative_score": float(cumulative_score)
                })

    conn.close()

    # Sort by node_id ascending, then recorded_at ascending
    expected_data.sort(key=lambda x: (x['node_id'], x['recorded_at']))
    return expected_data

def test_results_json_exists():
    """Verify that the results.json file was created."""
    assert os.path.exists(RESULTS_PATH), f"Expected output file not found at {RESULTS_PATH}"
    assert os.path.isfile(RESULTS_PATH), f"Path {RESULTS_PATH} is not a file"

def test_results_json_content():
    """Verify that results.json contains the correctly filtered and computed cumulative scores."""
    expected_data = get_expected_results()

    try:
        with open(RESULTS_PATH, 'r') as f:
            actual_data = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse JSON from {RESULTS_PATH}: {e}")

    assert isinstance(actual_data, list), "JSON root must be an array"
    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} records, found {len(actual_data)}"

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert "node_id" in actual, f"Record {i} missing 'node_id'"
        assert "recorded_at" in actual, f"Record {i} missing 'recorded_at'"
        assert "cumulative_score" in actual, f"Record {i} missing 'cumulative_score'"

        assert actual["node_id"] == expected["node_id"], f"Record {i}: Expected node_id '{expected['node_id']}', got '{actual['node_id']}'"
        assert actual["recorded_at"] == expected["recorded_at"], f"Record {i}: Expected recorded_at '{expected['recorded_at']}', got '{actual['recorded_at']}'"
        assert float(actual["cumulative_score"]) == expected["cumulative_score"], f"Record {i}: Expected cumulative_score {expected['cumulative_score']}, got {actual['cumulative_score']}"