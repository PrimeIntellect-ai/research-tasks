# test_final_state.py

import os
import sqlite3
import pytest

DB_PATH = "/home/user/etl_result.db"
CRON_BACKUP_PATH = "/home/user/crontab_backup.txt"
RAW_CSV_PATH = "/home/user/raw_vectors.csv"

def test_db_exists():
    assert os.path.exists(DB_PATH), f"Database {DB_PATH} was not created."
    assert os.path.isfile(DB_PATH), f"{DB_PATH} is not a file."

def test_processed_vectors_table_exists():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='processed_vectors'")
    table = cursor.fetchone()
    conn.close()
    assert table is not None, "Table 'processed_vectors' does not exist in the database."

def test_db_row_count():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM processed_vectors")
    count = cursor.fetchone()[0]
    conn.close()
    assert count == 5000, f"Expected exactly 5000 rows in 'processed_vectors', got {count}."

def test_db_sorting():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT poly_hash FROM processed_vectors")
    hashes = [row[0] for row in cursor.fetchall()]
    conn.close()

    assert len(hashes) > 0, "No records found to check sorting."
    assert hashes == sorted(hashes, reverse=True), "Records are not sorted by poly_hash in descending order."

def test_db_content_correctness():
    # Recompute expected data from the raw CSV
    expected_records = {}
    with open(RAW_CSV_PATH, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) != 11:
                continue
            record_id = int(parts[0])
            coeffs = [int(x) for x in parts[1:]]

            # Compute hash
            poly_hash = 0
            for i, c in enumerate(coeffs):
                poly_hash += c * (31 ** i)
            poly_hash %= 1000000007

            if poly_hash not in expected_records:
                expected_records[poly_hash] = (record_id, ",".join(parts[1:]))
            else:
                # Keep smallest record_id
                if record_id < expected_records[poly_hash][0]:
                    expected_records[poly_hash] = (record_id, ",".join(parts[1:]))

    # Now check the DB matches the expected data
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, poly_hash, coefficients FROM processed_vectors")
    db_records = cursor.fetchall()
    conn.close()

    assert len(db_records) == len(expected_records), "Mismatch in number of unique hashes."

    for db_id, db_hash, db_coeffs in db_records:
        assert db_hash in expected_records, f"Hash {db_hash} found in DB but not in expected data."
        exp_id, exp_coeffs = expected_records[db_hash]
        assert db_id == exp_id, f"For hash {db_hash}, expected record_id {exp_id}, got {db_id}. Deduplication did not keep the smallest record_id."
        assert db_coeffs == exp_coeffs, f"For hash {db_hash}, expected coefficients '{exp_coeffs}', got '{db_coeffs}'."

def test_cron_backup():
    assert os.path.exists(CRON_BACKUP_PATH), f"Cron backup file {CRON_BACKUP_PATH} was not created."

    with open(CRON_BACKUP_PATH, "r") as f:
        cron_content = f.read()

    assert "run_etl.py" in cron_content, "The cron job does not reference run_etl.py."

    has_15_min = "*/15 * * * *" in cron_content or "0,15,30,45 * * * *" in cron_content or "0,15,30,45" in cron_content
    assert has_15_min, "The cron job schedule is not set to run exactly every 15 minutes."