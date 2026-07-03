# test_final_state.py

import os
import sqlite3
import csv
import json
from collections import defaultdict

def get_expected_data():
    csv_file = '/home/user/telemetry.csv'
    json_file = '/home/user/users.json'

    assert os.path.exists(csv_file), f"Input file {csv_file} is missing."
    assert os.path.exists(json_file), f"Input file {json_file} is missing."

    with open(json_file, 'r') as f:
        users_data = json.load(f)

    user_tiers = {u['user_id']: u['subscription_tier'] for u in users_data}

    strata = defaultdict(list)
    with open(csv_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            uid = row['user_id']
            if uid in user_tiers:
                row['subscription_tier'] = user_tiers[uid]
                strata[row['subscription_tier']].append(row)

    expected_rows = []
    for tier, records in strata.items():
        # Sort by timestamp ASC, then user_id ASC
        records.sort(key=lambda x: (x['timestamp'], x['user_id']))
        # Sample even indices
        sampled = [records[i] for i in range(len(records)) if i % 2 == 0]
        expected_rows.extend(sampled)

    # Order expected rows by subscription_tier, timestamp, user_id for deterministic comparison
    expected_rows.sort(key=lambda x: (x['subscription_tier'], x['timestamp'], x['user_id']))

    # Convert to tuples in the exact column order
    expected_tuples = [
        (r['user_id'], r['event_type'], r['timestamp'], r['region'], r['subscription_tier'])
        for r in expected_rows
    ]
    return expected_tuples

def test_database_exists():
    db_file = '/home/user/cleaned_sample.db'
    assert os.path.exists(db_file), f"Database file {db_file} does not exist."
    assert os.path.isfile(db_file), f"Path {db_file} is not a file."

def test_table_schema_and_content():
    db_file = '/home/user/cleaned_sample.db'
    assert os.path.exists(db_file), "Database file missing."

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='telemetry_sample';")
    table_exists = cursor.fetchone()
    assert table_exists is not None, "Table 'telemetry_sample' does not exist in the database."

    # Check columns
    cursor.execute("PRAGMA table_info(telemetry_sample);")
    columns_info = cursor.fetchall()

    expected_columns = [
        ('user_id', 'TEXT'),
        ('event_type', 'TEXT'),
        ('timestamp', 'TEXT'),
        ('region', 'TEXT'),
        ('subscription_tier', 'TEXT')
    ]

    actual_columns = [(col[1], col[2].upper()) for col in columns_info]

    # Check column names and order
    actual_col_names = [col[0] for col in actual_columns]
    expected_col_names = [col[0] for col in expected_columns]
    assert actual_col_names == expected_col_names, f"Column names or order incorrect. Expected {expected_col_names}, got {actual_col_names}."

    # Fetch all data
    cursor.execute("SELECT user_id, event_type, timestamp, region, subscription_tier FROM telemetry_sample ORDER BY subscription_tier, timestamp, user_id;")
    actual_data = cursor.fetchall()
    conn.close()

    expected_data = get_expected_data()

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} rows in telemetry_sample, got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual == expected, f"Row {i} mismatch. Expected {expected}, got {actual}."