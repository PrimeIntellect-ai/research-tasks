# test_final_state.py
import os
import sqlite3

def test_index_created():
    db_path = "/home/user/research_data.db"
    assert os.path.exists(db_path), f"Database {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name='idx_target_id';")
    result = cursor.fetchone()
    conn.close()

    assert result is not None, "Index 'idx_target_id' was not created in the database."
    assert result[0] == "idx_target_id", "Index 'idx_target_id' was not found."

def test_summary_csv_contents():
    csv_path = "/home/user/summary.csv"
    assert os.path.exists(csv_path), f"Output file {csv_path} is missing."

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "Bio,4,3",
        "CS,5,1",
        "Math,7,6"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in summary.csv, found {len(lines)}."

    for expected, actual in zip(expected_lines, lines):
        assert actual == expected, f"Expected line '{expected}', but found '{actual}'."