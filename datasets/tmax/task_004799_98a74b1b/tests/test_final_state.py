# test_final_state.py

import os
import sqlite3
import pytest

def test_result_file_exists():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Result file {result_path} is missing. Did you run your C++ program and redirect/write the output?"

def test_cpp_file_exists():
    cpp_path = "/home/user/analyze_graph.cpp"
    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} is missing."

def test_result_content():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), "Cannot check content because result.txt is missing."

    # Compute the expected result directly from the database to be robust
    db_path = "/home/user/system_graph.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
        SELECT n.identifier, COUNT(e.dst_id) as out_degree
        FROM sys_nodes n
        JOIN sys_edges e ON n.node_id = e.src_id
        WHERE e.rel_type = 'DEPENDS_ON'
        GROUP BY n.node_id, n.identifier
        ORDER BY out_degree DESC, n.identifier ASC
        LIMIT 3
    """

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
    except sqlite3.Error as e:
        pytest.fail(f"Failed to query the database to determine expected results: {e}")
    finally:
        conn.close()

    expected_lines = [row[0] for row in rows]

    with open(result_path, "r") as f:
        actual_content = f.read().strip().splitlines()

    actual_lines = [line.strip() for line in actual_content if line.strip()]

    assert actual_lines == expected_lines, f"Expected the top 3 entities to be {expected_lines}, but got {actual_lines}. Make sure to sort by out-degree DESC and then alphabetically ASC."