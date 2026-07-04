# test_final_state.py
import os
import re
import sqlite3

def test_c_file_exists_and_content():
    """Verify the C file exists and contains required transaction and parameterization logic."""
    c_file_path = "/home/user/graph_etl.c"
    assert os.path.exists(c_file_path), f"C source file {c_file_path} does not exist."

    with open(c_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for dead-lock prevention transaction types
    has_immediate = re.search(r"BEGIN\s+IMMEDIATE", content, re.IGNORECASE)
    has_exclusive = re.search(r"BEGIN\s+EXCLUSIVE", content, re.IGNORECASE)
    assert has_immediate or has_exclusive, (
        "C code does not use 'BEGIN IMMEDIATE' or 'BEGIN EXCLUSIVE' "
        "to prevent deadlocks during the read-modify-write cycle."
    )

    # Check for parameterized queries
    assert "sqlite3_bind_" in content, (
        "C code does not use parameterized queries (missing 'sqlite3_bind_...'). "
        "String concatenation for SQL queries is not allowed."
    )

def test_plan_txt_exists_and_content():
    """Verify the EXPLAIN QUERY PLAN output file exists and indicates index usage."""
    plan_file_path = "/home/user/plan.txt"
    assert os.path.exists(plan_file_path), f"Query plan file {plan_file_path} does not exist."

    with open(plan_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    has_using_index = re.search(r"USING\s+INDEX", content, re.IGNORECASE)
    has_covering_index = re.search(r"COVERING\s+INDEX", content, re.IGNORECASE)

    assert has_using_index or has_covering_index, (
        "Query plan does not indicate the use of an index. "
        "Ensure you created an optimal index on user_connections and generated the EXPLAIN QUERY PLAN."
    )

def test_fof_graph_results():
    """Verify that the fof_graph table contains the mathematically correct results for users 1, 5, and 10."""
    db_path = "/home/user/etl.db"
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    try:
        cursor = conn.cursor()

        # Check if fof_graph table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='fof_graph';")
        assert cursor.fetchone() is not None, "Table 'fof_graph' does not exist in etl.db."

        # Calculate the expected results directly from the raw data
        # FoF: a -> b -> c, where a != c
        cursor.execute("""
            SELECT DISTINCT a.user_a, b.user_b
            FROM user_connections a
            JOIN user_connections b ON a.user_b = b.user_a
            WHERE a.user_a IN (1, 5, 10) AND a.user_a != b.user_b
            ORDER BY a.user_a, b.user_b
        """)
        expected = cursor.fetchall()

        # Fetch the actual results from the fof_graph table for the target users
        cursor.execute("""
            SELECT DISTINCT source, target
            FROM fof_graph
            WHERE source IN (1, 5, 10)
            ORDER BY source, target
        """)
        actual = cursor.fetchall()

        assert expected == actual, (
            f"Data in fof_graph is incorrect for users 1, 5, 10.\n"
            f"Expected: {expected}\n"
            f"Actual: {actual}"
        )

        # Check UNIQUE constraint on fof_graph (by checking table info or attempting a duplicate insert)
        # We can inspect the schema to ensure the UNIQUE constraint exists
        cursor.execute("PRAGMA index_list('fof_graph');")
        indexes = cursor.fetchall()
        unique_constraint_found = False
        for idx in indexes:
            if idx[2] == 1:  # unique = 1
                unique_constraint_found = True
                break

        assert unique_constraint_found, "Table 'fof_graph' does not have a UNIQUE constraint on (source, target)."

    finally:
        conn.close()