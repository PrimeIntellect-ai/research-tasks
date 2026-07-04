# test_final_state.py

import os
import sqlite3
import math
import csv
import pytest

RAW_CSV_PATH = '/home/user/raw_vectors.csv'
DB_PATH = '/home/user/vectors.db'
V1_SUM_PATH = '/home/user/v1_sum.txt'

@pytest.fixture(scope="module")
def expected_data():
    if not os.path.exists(RAW_CSV_PATH):
        pytest.fail(f"{RAW_CSV_PATH} is missing.")

    expected_v1_sum = 0.0
    expected_rows = []
    with open(RAW_CSV_PATH, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            vec = [float(x) for x in row]
            norm = math.sqrt(sum(x*x for x in vec))
            norm_vec = [round(x / norm, 6) for x in vec]
            expected_v1_sum += norm_vec[0]
            expected_rows.append(norm_vec)

    return expected_v1_sum, expected_rows

def test_v1_sum_file(expected_data):
    expected_v1_sum, _ = expected_data
    assert os.path.exists(V1_SUM_PATH), f"{V1_SUM_PATH} does not exist."

    with open(V1_SUM_PATH, 'r') as f:
        content = f.read().strip()

    try:
        actual_v1_sum = float(content)
    except ValueError:
        pytest.fail(f"Content of {V1_SUM_PATH} is not a valid float: '{content}'")

    assert math.isclose(actual_v1_sum, expected_v1_sum, rel_tol=1e-3, abs_tol=1e-3), \
        f"Expected v1 sum approximately {expected_v1_sum}, got {actual_v1_sum}"

def test_database_schema_and_counts(expected_data):
    _, expected_rows = expected_data
    assert os.path.exists(DB_PATH), f"Database file {DB_PATH} does not exist."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='normalized_vectors'")
    assert cursor.fetchone() is not None, "Table 'normalized_vectors' does not exist."

    # Check columns
    cursor.execute("PRAGMA table_info(normalized_vectors)")
    columns = cursor.fetchall()

    expected_cols = [f'v{i}' for i in range(1, 11)]
    actual_cols = [col[1] for col in columns]
    assert actual_cols == expected_cols, f"Expected columns {expected_cols}, got {actual_cols}"

    # Check row count
    cursor.execute("SELECT COUNT(*) FROM normalized_vectors")
    count = cursor.fetchone()[0]
    expected_count = len(expected_rows)
    assert count == expected_count, f"Expected {expected_count} rows, got {count}"

    # Verify a few rows to ensure correct normalization
    cursor.execute("SELECT * FROM normalized_vectors LIMIT 10")
    db_rows = cursor.fetchall()

    for db_row, exp_row in zip(db_rows, expected_rows[:10]):
        for db_val, exp_val in zip(db_row, exp_row):
            assert math.isclose(db_val, exp_val, rel_tol=1e-5, abs_tol=1e-5), \
                f"Value mismatch in DB: expected {exp_val}, got {db_val}"

    conn.close()