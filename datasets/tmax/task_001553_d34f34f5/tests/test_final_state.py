# test_final_state.py

import os
import sqlite3
import stat

def test_c_source_file_exists():
    """Verify that the C source code file exists."""
    src_path = "/home/user/etl_extract.c"
    assert os.path.isfile(src_path), f"C source file {src_path} is missing."

def test_compiled_binary_exists_and_executable():
    """Verify that the compiled binary exists and is executable."""
    bin_path = "/home/user/etl_extract"
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} is missing."

    # Check if executable
    st = os.stat(bin_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {bin_path} is not executable."

def test_cypher_output_correct():
    """Verify the generated Cypher output matches the expected output exactly."""
    out_path = "/home/user/graph_import.cypher"
    assert os.path.isfile(out_path), f"Output file {out_path} is missing."

    expected_lines = [
        "CREATE (u1:User {id: 1})-[:CONNECTED_ACTIVE]->(u2:User {id: 2})",
        "CREATE (u1:User {id: 1})-[:CONNECTED_ACTIVE]->(u2:User {id: 5})",
        "CREATE (u1:User {id: 2})-[:CONNECTED_ACTIVE]->(u2:User {id: 4})",
        "CREATE (u1:User {id: 4})-[:CONNECTED_ACTIVE]->(u2:User {id: 5})"
    ]

    with open(out_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Cypher output does not match expected.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )

def test_indexes_created():
    """Verify that at least one index was created on t_beta or t_gamma."""
    db_path = "/home/user/legacy.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name, tbl_name FROM sqlite_master WHERE type='index';")
    indexes = cursor.fetchall()
    conn.close()

    # Filter out auto-generated indexes like sqlite_autoindex
    user_indexes = [idx for idx in indexes if not idx[0].startswith("sqlite_")]

    assert len(user_indexes) > 0, "No custom indexes were created in the database."

    # Check if at least one index is on t_beta or t_gamma
    indexed_tables = {idx[1] for idx in user_indexes}
    assert "t_beta" in indexed_tables or "t_gamma" in indexed_tables, (
        f"Expected indexes on t_beta or t_gamma, but found indexes on: {indexed_tables}"
    )