# test_final_state.py

import os
import sqlite3
import pytest
import csv

def test_top_nodes_csv():
    csv_path = '/home/user/top_nodes.csv'
    assert os.path.exists(csv_path), f"File {csv_path} does not exist."

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 3, f"Expected 3 rows in {csv_path}, found {len(rows)}."

    # Check exact values based on the graph math for us-east
    expected_rows = [
        ['n2', '0.8000'],
        ['n1', '0.2000'],
        ['n3', '0.2000']
    ]

    assert rows == expected_rows, f"Expected CSV rows {expected_rows}, got {rows}."

def test_ranking_sql():
    sql_path = '/home/user/ranking.sql'
    assert os.path.exists(sql_path), f"File {sql_path} does not exist."

    with open(sql_path, 'r') as f:
        query = f.read().strip()

    assert query, f"{sql_path} is empty."

    db_path = '/home/user/network.db'
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    try:
        c.execute(query)
        results = c.fetchall()
    except sqlite3.Error as e:
        pytest.fail(f"Executing {sql_path} failed with SQLite error: {e}")
    finally:
        conn.close()

    assert len(results) == 8, f"Expected 8 rows from ranking query, got {len(results)}."

    # Check that rank is calculated correctly
    # us-east edges: 
    # n3->n2 (2.0) rank 1
    # n1->n2 (1.5) rank 2
    # n5->n2 (1.0) rank 3
    # n2->n1 (1.0) rank 3
    # n1->n3 (0.8) rank 5
    # n4->n2 (0.5) rank 6
    # eu-west edges:
    # n7->n8 (1.2) rank 1
    # n6->n7 (1.0) rank 2

    ranks = {(row[0], row[1]): row[4] for row in results}
    assert ranks.get(('n3', 'n2')) == 1, "Incorrect rank for n3->n2"
    assert ranks.get(('n1', 'n2')) == 2, "Incorrect rank for n1->n2"
    assert ranks.get(('n7', 'n8')) == 1, "Incorrect rank for n7->n8"

def test_python_script_fixed():
    script_path = '/home/user/analyze_network.py'
    assert os.path.exists(script_path), f"Script file {script_path} is missing."

    with open(script_path, 'r') as f:
        content = f.read()

    assert "?" in content, "The script does not appear to use parameterized queries (missing '?')."
    assert "JOIN" in content.upper(), "The script does not appear to use a JOIN in the SQL query."