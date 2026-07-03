# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/backup_metadata.db"
LOG_PATH = "/home/user/chain_15.log"
RS_PATH_1 = "/home/user/get_chain.rs"
RS_PATH_2 = "/home/user/backup_tool/src/main.rs"

def get_expected_chain(db_path, target_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    WITH RECURSIVE backup_chain AS (
        SELECT id, parent_id, size_bytes, created_at
        FROM backups
        WHERE id = ?

        UNION ALL

        SELECT b.id, b.parent_id, b.size_bytes, b.created_at
        FROM backups b
        INNER JOIN backup_chain c ON c.parent_id = b.id
    )
    SELECT id, size_bytes FROM backup_chain
    ORDER BY created_at ASC;
    """
    cursor.execute(query, (target_id,))
    results = cursor.fetchall()
    conn.close()

    return [f"{row[0]},{row[1]}" for row in results]

def test_log_output_correct():
    assert os.path.isfile(LOG_PATH), f"Output log {LOG_PATH} does not exist."

    expected_lines = get_expected_chain(DB_PATH, 15)

    with open(LOG_PATH, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {LOG_PATH} do not match the expected backup chain.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )

def test_rust_code_parameterized():
    # Find the Rust source file
    rs_file = None
    if os.path.isfile(RS_PATH_1):
        rs_file = RS_PATH_1
    elif os.path.isfile(RS_PATH_2):
        rs_file = RS_PATH_2
    else:
        # Fallback: search for get_chain.rs or main.rs in /home/user
        for root, _, files in os.walk("/home/user"):
            for file in files:
                if file.endswith(".rs"):
                    rs_file = os.path.join(root, file)
                    break
            if rs_file:
                break

    assert rs_file is not None, "Could not find the Rust source file (e.g., /home/user/get_chain.rs)."

    with open(rs_file, "r") as f:
        content = f.read()

    # Check for parameterization markers commonly used in rusqlite
    has_params = "?" in content or "$1" in content or ":1" in content or "?1" in content
    assert has_params, f"The Rust source code in {rs_file} does not appear to use a parameterized query (missing '?', '$1', etc.)."