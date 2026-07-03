# test_final_state.py

import os
import sqlite3
import json
import hashlib
import uuid
import glob
import pytest

def test_db_v2_exists_and_schema():
    db_path = "/home/user/qa_env/db/users_v2.db"
    assert os.path.isfile(db_path), f"New database {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='secure_users';")
    table = cursor.fetchone()
    assert table is not None, "Table 'secure_users' does not exist in users_v2.db."

    cursor.execute("PRAGMA table_info(secure_users);")
    columns = {row[1]: row[2] for row in cursor.fetchall()}

    expected_columns = {
        'user_uuid': 'TEXT',
        'username': 'TEXT',
        'pass_hash': 'TEXT'
    }

    for col_name, col_type in expected_columns.items():
        assert col_name in columns, f"Column '{col_name}' is missing in 'secure_users'."
        # SQLite types can sometimes be case-insensitive or slightly varying, but TEXT is standard
        assert "TEXT" in columns[col_name].upper(), f"Column '{col_name}' should be of type TEXT."

    conn.close()

def test_db_v2_data():
    db_v1_path = "/home/user/qa_env/db/users_v1.db"
    db_v2_path = "/home/user/qa_env/db/users_v2.db"

    assert os.path.isfile(db_v1_path), f"Legacy database {db_v1_path} is missing."
    assert os.path.isfile(db_v2_path), f"New database {db_v2_path} is missing."

    conn_v1 = sqlite3.connect(db_v1_path)
    cursor_v1 = conn_v1.cursor()
    cursor_v1.execute("SELECT username, password FROM old_users;")
    old_users = cursor_v1.fetchall()
    conn_v1.close()

    conn_v2 = sqlite3.connect(db_v2_path)
    cursor_v2 = conn_v2.cursor()
    cursor_v2.execute("SELECT user_uuid, username, pass_hash FROM secure_users;")
    new_users = cursor_v2.fetchall()
    conn_v2.close()

    assert len(new_users) == len(old_users), f"Expected {len(old_users)} rows in secure_users, found {len(new_users)}."

    new_users_dict = {row[1]: {'uuid': row[0], 'hash': row[2]} for row in new_users}

    for username, password in old_users:
        assert username in new_users_dict, f"User '{username}' was not migrated to users_v2.db."

        user_data = new_users_dict[username]

        # Validate UUID
        try:
            val = uuid.UUID(user_data['uuid'], version=4)
        except ValueError:
            pytest.fail(f"user_uuid '{user_data['uuid']}' for user '{username}' is not a valid UUID4.")

        # Validate Hash
        expected_hash = hashlib.sha256(f"{username}{password}QA_SECURE_SALT_2024".encode('utf-8')).hexdigest()
        assert user_data['hash'] == expected_hash, f"Hash for user '{username}' is incorrect. Expected {expected_hash}, got {user_data['hash']}."

def test_cython_compiled_module():
    src_dir = "/home/user/qa_env/src"
    so_files = glob.glob(os.path.join(src_dir, "auth_hash.*.so"))

    assert len(so_files) > 0, "No compiled Cython module (auth_hash.*.so) found in /home/user/qa_env/src/."

def test_metrics_json():
    metrics_path = "/home/user/qa_env/results/metrics.json"
    assert os.path.isfile(metrics_path), f"Metrics file {metrics_path} is missing."

    with open(metrics_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Metrics file {metrics_path} is not valid JSON.")

    expected_keys = ["python_duration_seconds", "cython_duration_seconds", "cython_is_faster"]
    for key in expected_keys:
        assert key in data, f"Key '{key}' is missing from metrics.json."

    assert isinstance(data["python_duration_seconds"], (int, float)), "python_duration_seconds must be a number."
    assert isinstance(data["cython_duration_seconds"], (int, float)), "cython_duration_seconds must be a number."
    assert isinstance(data["cython_is_faster"], bool), "cython_is_faster must be a boolean."