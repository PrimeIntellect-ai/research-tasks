# test_final_state.py
import json
import os
import sqlite3
import pytest

def test_recommendations_json_exists():
    assert os.path.isfile('/home/user/recommendations.json'), "The file /home/user/recommendations.json does not exist."

def test_recommendations_content():
    db_path = '/home/user/graph.db'
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    # Compute expected results dynamically from the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    WITH mutual_counts AS (
        SELECT e1.source_id AS user1, e2.source_id AS user2, COUNT(*) AS mutual_friends
        FROM edges e1
        JOIN edges e2 ON e1.target_id = e2.target_id
        WHERE e1.source_id < e2.source_id
        AND NOT EXISTS (
            SELECT 1 FROM edges e3 
            WHERE e3.source_id = e1.source_id AND e3.target_id = e2.source_id
        )
        GROUP BY e1.source_id, e2.source_id
    )
    SELECT user1, user2, mutual_friends,
           RANK() OVER (ORDER BY mutual_friends DESC, user1 ASC, user2 ASC) as rank
    FROM mutual_counts
    ORDER BY rank
    LIMIT 10;
    """

    cursor.execute(query)
    expected_rows = cursor.fetchall()
    conn.close()

    expected_data = []
    for row in expected_rows:
        expected_data.append({
            "user1": row[0],
            "user2": row[1],
            "mutual_friends": row[2],
            "rank": row[3]
        })

    with open('/home/user/recommendations.json', 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("The file /home/user/recommendations.json does not contain valid JSON.")

    assert isinstance(actual_data, list), "The JSON output should be a list of objects."
    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} recommendations, but got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual.get('user1') == expected['user1'], f"Mismatch at rank {expected['rank']}: expected user1={expected['user1']}, got {actual.get('user1')}."
        assert actual.get('user2') == expected['user2'], f"Mismatch at rank {expected['rank']}: expected user2={expected['user2']}, got {actual.get('user2')}."
        assert actual.get('mutual_friends') == expected['mutual_friends'], f"Mismatch at rank {expected['rank']}: expected mutual_friends={expected['mutual_friends']}, got {actual.get('mutual_friends')}."
        assert actual.get('rank') == expected['rank'], f"Mismatch at index {i}: expected rank={expected['rank']}, got {actual.get('rank')}."