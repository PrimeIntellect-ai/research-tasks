# test_final_state.py

import os
import sys
import importlib.util
import sqlite3
import pytest

def import_module_from_path(module_name, file_path):
    assert os.path.isfile(file_path), f"Required file missing: {file_path}"
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        pytest.fail(f"Failed to import {file_path}: {e}")
    return module

def test_failure_count():
    count_file = "/home/user/failure_count.txt"
    assert os.path.isfile(count_file), f"Failure count file missing: {count_file}"

    with open(count_file, "r") as f:
        content = f.read().strip()

    assert content == "5", f"Expected failure count to be '5', but got '{content}'"

def test_build_query():
    query_file = "/home/user/build_query.py"
    module = import_module_from_path("build_query", query_file)

    assert hasattr(module, "get_anomaly_query"), "Function 'get_anomaly_query' missing in build_query.py"

    table_name = "test_backups"
    query = module.get_anomaly_query(table_name)

    assert isinstance(query, str), "get_anomaly_query must return a string"

    # Set up in-memory SQLite database to test the query
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute(f"CREATE TABLE {table_name} (backup_id INTEGER, db_name TEXT, backup_size_mb REAL, timestamp DATETIME)")

    # Insert test data
    # We need 6 rows for db1 to have a full 5-preceding window.
    # Window avg of first 5 = 100.0
    # Row 6: size 250.0 > 200% of 100.0 (which is 200.0), so this is an anomaly.
    # Row 7: size 150.0 (window avg of prev 5 is (100*4+250)/5 = 130.0). 200% is 260.0. Not an anomaly.
    data = [
        (1, 'db1', 100.0, '2023-01-01 10:00:00'),
        (2, 'db1', 100.0, '2023-01-02 10:00:00'),
        (3, 'db1', 100.0, '2023-01-03 10:00:00'),
        (4, 'db1', 100.0, '2023-01-04 10:00:00'),
        (5, 'db1', 100.0, '2023-01-05 10:00:00'),
        (6, 'db1', 250.0, '2023-01-06 10:00:00'), # Anomaly
        (7, 'db1', 150.0, '2023-01-07 10:00:00'),
        # db2 data
        (8, 'db2', 50.0, '2023-01-01 10:00:00'),
        (9, 'db2', 50.0, '2023-01-02 10:00:00'),
        (10, 'db2', 50.0, '2023-01-03 10:00:00'),
        (11, 'db2', 50.0, '2023-01-04 10:00:00'),
        (12, 'db2', 50.0, '2023-01-05 10:00:00'),
        (13, 'db2', 101.0, '2023-01-06 10:00:00'), # Anomaly (101 > 200% of 50 = 100)
    ]

    cursor.executemany(f"INSERT INTO {table_name} VALUES (?, ?, ?, ?)", data)
    conn.commit()

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0].lower() for desc in cursor.description]
    except sqlite3.Error as e:
        pytest.fail(f"Executing the generated query failed: {e}")

    expected_columns = ["backup_id", "db_name", "backup_size_mb", "rolling_avg"]
    for col in expected_columns:
        assert col in columns, f"Expected column '{col}' in output schema, got: {columns}"

    # We expect exactly backup_id 6 and 13 to be returned as anomalies
    anomaly_ids = [row[columns.index("backup_id")] for row in results]
    assert sorted(anomaly_ids) == [6, 13], f"Expected anomalies with backup_id [6, 13], but got {anomaly_ids}"

def test_sanitizer_adversarial_corpus():
    sanitizer_file = "/home/user/sanitizer.py"
    module = import_module_from_path("sanitizer", sanitizer_file)

    assert hasattr(module, "is_safe_filter"), "Function 'is_safe_filter' missing in sanitizer.py"
    is_safe_filter = module.is_safe_filter

    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.isdir(clean_dir), "Clean corpus directory missing"
    assert os.path.isdir(evil_dir), "Evil corpus directory missing"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.txt')]
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.txt')]

    clean_failed = []
    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        with open(filepath, "r") as f:
            content = f.read().strip()
        try:
            if not is_safe_filter(content):
                clean_failed.append(filename)
        except Exception as e:
            clean_failed.append(f"{filename} (raised exception: {e})")

    evil_failed = []
    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        with open(filepath, "r") as f:
            content = f.read().strip()
        try:
            if is_safe_filter(content):
                evil_failed.append(filename)
        except Exception:
            # Raising an exception on evil input is an acceptable way to reject it
            pass

    error_msg = []
    if clean_failed:
        error_msg.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_msg.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))