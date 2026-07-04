# test_final_state.py
import os
import sqlite3
import pytest

DB_PATH = '/home/user/output/analytics.db'

def test_db_exists():
    assert os.path.exists(DB_PATH), f"Database not found at {DB_PATH}. Ensure your script creates the database at the exact specified path."

def test_table_exists():
    assert os.path.exists(DB_PATH), f"Database missing: {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='item_centrality'")
    table = cursor.fetchone()
    conn.close()
    assert table is not None, "Table 'item_centrality' does not exist in the database."

def test_top_3_results():
    assert os.path.exists(DB_PATH), f"Database missing: {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT item_id, centrality FROM item_centrality ORDER BY centrality DESC, item_id ASC")
        rows = cursor.fetchall()
    except sqlite3.OperationalError as e:
        pytest.fail(f"Failed to query 'item_centrality' table: {e}")
    finally:
        conn.close()

    assert len(rows) == 3, f"Expected exactly 3 rows in 'item_centrality' representing the top 3 items, but found {len(rows)}."

    # Derivation based on the provided events.jsonl:
    # A, B, C, D all have degree 4 out of 5 possible edges (centrality 0.8).
    # E, F have degree 2 out of 5 possible edges (centrality 0.4).
    # Sorting by centrality DESC, then item_id ASC yields A, B, C as the top 3.
    expected_rows = [
        ('Item_A', 0.8),
        ('Item_B', 0.8),
        ('Item_C', 0.8)
    ]

    for i, (row, expected) in enumerate(zip(rows, expected_rows)):
        assert row[0] == expected[0], f"Rank {i+1} item_id mismatch: expected '{expected[0]}', got '{row[0]}'. Make sure ties are sorted alphabetically ascending."
        assert isinstance(row[1], (int, float)), f"Centrality for {row[0]} should be a number, got {type(row[1])}."
        assert abs(row[1] - expected[1]) < 0.001, f"Rank {i+1} centrality mismatch for {row[0]}: expected {expected[1]}, got {row[1]}."