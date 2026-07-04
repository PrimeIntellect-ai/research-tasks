# test_final_state.py
import os
import sqlite3
import csv
import pytest

def test_top_5_triangles_csv():
    csv_path = '/home/user/top_5_triangles.csv'
    db_path = '/home/user/graph.db'

    assert os.path.exists(csv_path), f"Output file missing at {csv_path}"
    assert os.path.exists(db_path), f"Database file missing at {db_path}"

    # Compute the expected result dynamically from the database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    query = """
    SELECT c1.u1 AS u1_id, c1.u2 AS u2_id, c2.u2 AS u3_id, 
           (c1.weight + c2.weight + c3.weight) AS total_weight
    FROM connections c1
    JOIN connections c2 ON c1.u2 = c2.u1
    JOIN connections c3 ON c1.u1 = c3.u1 AND c2.u2 = c3.u2
    JOIN users u1 ON c1.u1 = u1.id
    JOIN users u2 ON c1.u2 = u2.id
    JOIN users u3 ON c2.u2 = u3.id
    WHERE u1.department = 'Engineering' 
      AND u2.department = 'Engineering' 
      AND u3.department = 'Engineering'
    ORDER BY total_weight DESC, u1_id ASC, u2_id ASC, u3_id ASC
    LIMIT 5;
    """

    c.execute(query)
    expected_rows = c.fetchall()
    conn.close()

    # Read the CSV file
    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        actual_rows = []
        for row in reader:
            if row:
                actual_rows.append(tuple(int(x) for x in row))

    expected_header = ['u1_id', 'u2_id', 'u3_id', 'total_weight']
    assert header == expected_header, f"CSV header is incorrect. Expected {expected_header}, got {header}"

    assert actual_rows == expected_rows, f"CSV data does not match expected output.\nExpected: {expected_rows}\nGot: {actual_rows}"

def test_query_plan_txt():
    txt_path = '/home/user/query_plan.txt'
    assert os.path.exists(txt_path), f"Query plan file missing at {txt_path}"

    with open(txt_path, 'r') as f:
        content = f.read().upper()

    # Check for common EXPLAIN QUERY PLAN keywords
    valid_keywords = ["SCAN", "SEARCH", "USING INDEX", "COROUTINE", "B-TREE", "LIST"]
    has_keyword = any(keyword in content for keyword in valid_keywords)

    assert has_keyword, "query_plan.txt does not appear to contain a valid SQLite EXPLAIN QUERY PLAN output."