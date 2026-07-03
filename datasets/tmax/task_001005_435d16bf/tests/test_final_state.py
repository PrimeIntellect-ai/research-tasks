# test_final_state.py
import os
import csv
import sqlite3
import pytest

def get_actual_ids(csv_path):
    ids = set()
    try:
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    ids.add(int(row[0]))
    except Exception:
        pass
    return ids

def get_expected_ids(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Force fix index in memory/verifier just in case the agent failed but tried to generate a CSV anyway
    c.execute("REINDEX idx_status;")
    c.execute("""
        SELECT id FROM users 
        WHERE status = 'ACTIVE' AND priority > 50 
        ORDER BY created_at DESC, id ASC 
        LIMIT 500
    """)
    return set(row[0] for row in c.fetchall())

def test_etl_query_results():
    csv_path = '/home/user/results.csv'
    db_path = '/app/warehouse.db'

    assert os.path.exists(csv_path), f"Results CSV file is missing at {csv_path}."

    actual = get_actual_ids(csv_path)
    expected = get_expected_ids(db_path)

    intersection = len(actual.intersection(expected))
    union = len(actual.union(expected))

    jaccard = intersection / union if union > 0 else 0.0

    assert jaccard >= 1.0, f"Jaccard similarity {jaccard} is below threshold 1.0. Intersection: {intersection}, Union: {union}"

def test_c_program_exists():
    assert os.path.isfile('/home/user/etl_query.c'), "C source file /home/user/etl_query.c is missing."
    assert os.path.isfile('/home/user/etl_query'), "Compiled binary /home/user/etl_query is missing."