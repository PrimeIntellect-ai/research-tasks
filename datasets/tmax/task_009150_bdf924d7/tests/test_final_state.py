# test_final_state.py
import os
import sqlite3
import pytest

CPP_PATH = "/home/user/audit_processor.cpp"
CYPHER_PATH = "/home/user/flag_queries.cypher"
DB_PATH = "/home/user/audit.db"

def test_cpp_file_exists():
    assert os.path.exists(CPP_PATH), f"The C++ source file {CPP_PATH} is missing."
    assert os.path.isfile(CPP_PATH), f"{CPP_PATH} is not a valid file."

def test_cypher_queries_output():
    assert os.path.exists(CYPHER_PATH), f"The output file {CYPHER_PATH} was not created."
    assert os.path.isfile(CYPHER_PATH), f"{CYPHER_PATH} is not a valid file."

    # Connect to the database to derive the expected output
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Use SQLite window functions to determine which users have > 5 events in any 600s sliding window
    query = """
    SELECT DISTINCT user_id
    FROM (
        SELECT user_id, 
               COUNT(*) OVER (
                   PARTITION BY user_id 
                   ORDER BY access_time 
                   RANGE BETWEEN 600 PRECEDING AND CURRENT ROW
               ) as window_count
        FROM access_logs
    )
    WHERE window_count > 5
    ORDER BY user_id;
    """
    try:
        cursor.execute(query)
        flagged_users = [row[0] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        pytest.fail(f"Failed to execute verification query on database: {e}")
    finally:
        conn.close()

    expected_lines = [
        f"MATCH (u:User {{id: '{uid}'}}) SET u.compliance_risk = true;"
        for uid in flagged_users
    ]

    with open(CYPHER_PATH, 'r') as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"The contents of {CYPHER_PATH} do not match the expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {actual_lines}"
    )