# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = '/home/user/corporate_audit.db'
CYCLE_TXT_PATH = '/home/user/cycle.txt'
INDEX_SCHEMA_TXT_PATH = '/home/user/index_schema.txt'

def test_cycle_output_file():
    """Verify that cycle.txt exists and contains the correct cycle path."""
    assert os.path.isfile(CYCLE_TXT_PATH), f"Output file not found at {CYCLE_TXT_PATH}"

    with open(CYCLE_TXT_PATH, 'r') as f:
        content = f.read().strip()

    expected_cycle = "1001,5555,6666,7777,1001"
    assert content == expected_cycle, f"Expected cycle path '{expected_cycle}', but found '{content}'"

def test_index_schema_output_file():
    """Verify that index_schema.txt exists and contains the correct index creation statement."""
    assert os.path.isfile(INDEX_SCHEMA_TXT_PATH), f"Index schema file not found at {INDEX_SCHEMA_TXT_PATH}"

    with open(INDEX_SCHEMA_TXT_PATH, 'r') as f:
        content = f.read().strip().upper()

    assert "CREATE INDEX" in content, "The file does not contain a 'CREATE INDEX' statement."
    assert "IDX_OWNER_SUB" in content, "The file does not contain the index name 'idx_owner_sub'."

def test_database_index_created():
    """Verify that the index idx_owner_sub was actually created in the database and indexes owner_id."""
    assert os.path.isfile(DB_PATH), f"Database file not found at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if the index exists in sqlite_master
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='index' AND name='idx_owner_sub';")
    result = cursor.fetchone()

    assert result is not None, "Index 'idx_owner_sub' was not found in the database."

    sql = result[0].upper()
    assert "OWNER_ID" in sql, "The index 'idx_owner_sub' does not appear to index the 'owner_id' column."

    # Alternatively, use PRAGMA index_info
    cursor.execute("PRAGMA index_info('idx_owner_sub');")
    index_info = cursor.fetchall()
    conn.close()

    assert len(index_info) > 0, "Could not retrieve index info for 'idx_owner_sub'."

    # The first column in the index should be owner_id
    indexed_columns = [row[2] for row in index_info]
    assert indexed_columns[0] == 'owner_id', f"Expected the first indexed column to be 'owner_id', got '{indexed_columns[0]}'."