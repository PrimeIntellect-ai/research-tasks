# test_final_state.py

import os
import json
import sqlite3
import hmac
import hashlib
import subprocess
import pytest

def test_migrate_script_exists():
    assert os.path.isfile('/home/user/migrate.py'), "The migration script /home/user/migrate.py is missing."

def test_test_api_auth_script_exists():
    assert os.path.isfile('/home/user/test_api_auth.py'), "The test script /home/user/test_api_auth.py is missing."

def test_api_db_sqlite_state():
    db_path = '/home/user/api_db.sqlite'
    assert os.path.isfile(db_path), f"The database file {db_path} does not exist."

    json_path = '/home/user/legacy_keys.json'
    secret_path = '/home/user/hmac_secret.txt'

    assert os.path.isfile(json_path), f"Missing {json_path}"
    assert os.path.isfile(secret_path), f"Missing {secret_path}"

    with open(json_path, 'r') as f:
        legacy_data = json.load(f)

    with open(secret_path, 'r') as f:
        secret = f.read().strip()

    expected_rows = []
    for entry in legacy_data:
        user_id = entry['user_id']
        legacy_key = entry['legacy_key']

        computed_hash = hmac.new(
            secret.encode('utf-8'),
            legacy_key.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        expected_rows.append((user_id, computed_hash, '2024-01-01T00:00:00Z'))

    expected_rows.sort(key=lambda x: x[0])

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check table schema
        cursor.execute("PRAGMA table_info(api_credentials)")
        columns = {row[1] for row in cursor.fetchall()}
        assert {'user_id', 'hmac_hash', 'migrated_at'}.issubset(columns), "The api_credentials table is missing required columns."

        cursor.execute("SELECT user_id, hmac_hash, migrated_at FROM api_credentials ORDER BY user_id ASC")
        rows = cursor.fetchall()
        conn.close()
    except sqlite3.Error as e:
        pytest.fail(f"SQLite error when accessing {db_path}: {e}")

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in api_credentials, but found {len(rows)}."

    for i in range(len(expected_rows)):
        assert rows[i] == expected_rows[i], f"Row {i} mismatch. Expected {expected_rows[i]}, got {rows[i]}."

def test_test_api_auth_execution():
    script_path = '/home/user/test_api_auth.py'
    assert os.path.isfile(script_path), f"Missing {script_path}"

    result = subprocess.run(
        ['python3', script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, (
        f"Executing {script_path} failed with exit code {result.returncode}.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )