# test_final_state.py
import os
import csv
import sqlite3
import pytest

def test_query_rq():
    """Test that the SPARQL query file exists and contains expected keywords."""
    file_path = "/home/user/query.rq"
    assert os.path.exists(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read()

    assert "?x" in content, "Query missing variable ?x"
    assert "?y" in content, "Query missing variable ?y"
    assert "<follows>" in content, "Query missing <follows> relation"
    assert "<knows>" in content, "Query missing <knows> relation"
    assert "<http://example.org/TargetUser>" in content, "Query missing TargetUser URI"

def test_sqlite_db_and_indexes():
    """Test that the SQLite database exists, has the right schema, data, and indexes."""
    db_path = "/home/user/graph.db"
    nt_path = "/home/user/graph.nt"

    assert os.path.exists(db_path), f"Database {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='triples'")
    assert cursor.fetchone() is not None, "Table 'triples' is missing in the database."

    # Check columns
    cursor.execute("PRAGMA table_info(triples)")
    columns = [row[1] for row in cursor.fetchall()]
    assert set(columns).issuperset({"subject", "predicate", "object"}), "Table 'triples' missing required columns."

    # Check row count matches graph.nt
    if os.path.exists(nt_path):
        with open(nt_path, "r") as f:
            nt_lines = sum(1 for line in f if line.strip())

        cursor.execute("SELECT count(*) FROM triples")
        db_count = cursor.fetchone()[0]
        assert db_count == nt_lines, f"Expected {nt_lines} rows in triples table, found {db_count}."

    # Check for indexes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='triples' AND name NOT LIKE 'sqlite_autoindex%'")
    indexes = cursor.fetchall()
    assert len(indexes) > 0, "No custom indexes found on the 'triples' table to optimize the query."

    conn.close()

def test_result_csv():
    """Test that the result CSV exists, has the correct header, and exact expected data."""
    csv_path = "/home/user/result.csv"
    nt_path = "/home/user/graph.nt"

    assert os.path.exists(csv_path), f"CSV file {csv_path} is missing."
    assert os.path.exists(nt_path), f"Original graph file {nt_path} is missing."

    # Compute expected results directly from the N-Triples file
    follows_target = set()
    knows = []

    with open(nt_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) >= 3:
                s, p, o = parts[0], parts[1], parts[2]
                if p == "<follows>" and o == "<http://example.org/TargetUser>":
                    follows_target.add(s)
                if p == "<knows>":
                    knows.append((s, o))

    expected_pairs = []
    for s, o in knows:
        if s in follows_target and o in follows_target:
            # Strip angle brackets
            expected_pairs.append((s.strip("<>"), o.strip("<>")))

    # Sort alphabetically by user1, then user2
    expected_pairs.sort()

    # Read actual CSV
    with open(csv_path, "r") as f:
        reader = list(csv.reader(f))

    assert len(reader) > 0, "CSV file is empty."
    assert reader[0] == ["user1", "user2"], f"Expected CSV header ['user1', 'user2'], got {reader[0]}"

    actual_pairs = [(row[0], row[1]) for row in reader[1:]]

    assert actual_pairs == expected_pairs, f"CSV content does not match expected result. Expected {len(expected_pairs)} pairs, got {len(actual_pairs)}."