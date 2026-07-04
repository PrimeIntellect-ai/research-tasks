# test_final_state.py

import json
import os
import sqlite3
import pytest

DB_PATH = "/home/user/backup_catalog.db"
JSON_PATH = "/home/user/restore_plan.json"

def test_json_file_exists():
    assert os.path.exists(JSON_PATH), f"JSON file {JSON_PATH} does not exist."
    assert os.path.isfile(JSON_PATH), f"{JSON_PATH} is not a regular file."

def test_json_content_and_logic():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} missing."

    # Compute the expected result dynamically from the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Find most recent successful full backup
    cursor.execute("""
        SELECT id, start_time 
        FROM jobs 
        WHERE type='full' AND status='success' 
        ORDER BY start_time DESC 
        LIMIT 1
    """)
    full_backup = cursor.fetchone()
    assert full_backup is not None, "No successful full backup found in the database."
    full_backup_id, full_start_time = full_backup

    # Find successful incremental backups after the full backup
    cursor.execute("""
        SELECT id 
        FROM jobs 
        WHERE type='inc' AND status='success' AND start_time > ? 
        ORDER BY start_time ASC
    """, (full_start_time,))
    inc_backups = cursor.fetchall()
    inc_backup_ids = [row[0] for row in inc_backups]

    # Calculate total size of files for the restore chain
    all_ids = [full_backup_id] + inc_backup_ids
    placeholders = ",".join(["?"] * len(all_ids))
    cursor.execute(f"""
        SELECT SUM(size_bytes) 
        FROM files 
        WHERE job_id IN ({placeholders})
    """, all_ids)
    total_size = cursor.fetchone()[0] or 0

    conn.close()

    # Read and validate the JSON file
    with open(JSON_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} does not contain valid JSON.")

    assert "full_backup_id" in data, "Missing 'full_backup_id' key in JSON."
    assert "incremental_backup_ids" in data, "Missing 'incremental_backup_ids' key in JSON."
    assert "total_files_size" in data, "Missing 'total_files_size' key in JSON."

    assert data["full_backup_id"] == full_backup_id, \
        f"Expected full_backup_id {full_backup_id}, got {data['full_backup_id']}."

    assert isinstance(data["incremental_backup_ids"], list), \
        "'incremental_backup_ids' must be a list."
    assert data["incremental_backup_ids"] == inc_backup_ids, \
        f"Expected incremental_backup_ids {inc_backup_ids}, got {data['incremental_backup_ids']}."

    assert data["total_files_size"] == total_size, \
        f"Expected total_files_size {total_size}, got {data['total_files_size']}."

def test_index_created():
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} missing."
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT count(*) 
        FROM sqlite_master 
        WHERE type='index' AND tbl_name='jobs' AND name NOT LIKE 'sqlite_autoindex%';
    """)
    count = cursor.fetchone()[0]

    conn.close()

    assert count > 0, "No custom index was created on the 'jobs' table."