# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = '/home/user/research_data.db'
RESULT_PATH = '/home/user/result.txt'
INDEXES_SQL_PATH = '/home/user/indexes.sql'

def test_result_txt_content():
    assert os.path.exists(RESULT_PATH), f"File {RESULT_PATH} does not exist."
    with open(RESULT_PATH, 'r') as f:
        content = f.read().strip()
    assert content == "6", f"Expected {RESULT_PATH} to contain exactly '6', but got '{content}'."

def test_indexes_sql_content():
    assert os.path.exists(INDEXES_SQL_PATH), f"File {INDEXES_SQL_PATH} does not exist."
    with open(INDEXES_SQL_PATH, 'r') as f:
        content = f.read().lower()

    assert "create index" in content, f"{INDEXES_SQL_PATH} does not contain a 'CREATE INDEX' statement."
    assert "relationships" in content, f"{INDEXES_SQL_PATH} does not mention the 'relationships' table."
    assert "source_id" in content, f"{INDEXES_SQL_PATH} does not mention the 'source_id' column."

def test_database_index_created():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} does not exist."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA index_list('relationships')")
    indexes = cursor.fetchall()

    assert len(indexes) > 0, "No indexes were found on the 'relationships' table in the database."

    valid_index_found = False
    for idx in indexes:
        index_name = idx[1]
        cursor.execute(f"PRAGMA index_info('{index_name}')")
        columns = cursor.fetchall()
        # PRAGMA index_info returns (seqno, cid, name)
        # We check if the first column in the index is 'source_id'
        if columns and columns[0][2] == 'source_id':
            valid_index_found = True
            break

    assert valid_index_found, "No index found on the 'relationships' table that starts with the 'source_id' column."
    conn.close()