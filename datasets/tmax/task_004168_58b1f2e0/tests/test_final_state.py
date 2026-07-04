# test_final_state.py
import os
import sqlite3
import pandas as pd
import numpy as np
import pytest

def true_value(sensor_id, t):
    # Deterministic pseudo-random frequency and phase based on sensor_id
    seed = int(sensor_id.replace('sensor_', ''))
    np.random.seed(seed)
    freq = np.random.uniform(0.01, 0.1)
    phase = np.random.uniform(0, 2 * np.pi)
    return np.sin(freq * t + phase)

def test_sqlite_db_exists():
    """Verify that the SQLite database was created at the correct path."""
    db_path = "/home/user/sensors.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

def test_sqlite_schema():
    """Verify the schema of the readings table."""
    db_path = "/home/user/sensors.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='readings'")
    table = cursor.fetchone()
    assert table is not None, "Table 'readings' does not exist in the database."

    # Check schema
    cursor.execute("PRAGMA table_info(readings)")
    columns = {row[1]: row[2].upper() for row in cursor.fetchall()}

    expected_columns = {
        'sensor_id': 'TEXT',
        'timestamp': 'INTEGER',
        'value': 'REAL'
    }

    for col, data_type in expected_columns.items():
        assert col in columns, f"Column '{col}' is missing from the 'readings' table."
        # SQLite types can be flexible, but we expect them to match the required schema
        assert expected_columns[col] in columns[col], f"Column '{col}' has incorrect type. Expected {expected_columns[col]}, got {columns[col]}."

def test_imputation_mse():
    """Verify that the imputed values meet the MSE threshold."""
    db_path = "/home/user/sensors.db"
    assert os.path.isfile(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)

    # Check if table exists before reading
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='readings'")
    if not cursor.fetchone():
        pytest.fail("Table 'readings' does not exist in the database.")

    df = pd.read_sql_query("SELECT * FROM readings", conn)

    assert not df.empty, "The 'readings' table is empty."
    assert 'sensor_id' in df.columns, "Missing 'sensor_id' column."
    assert 'timestamp' in df.columns, "Missing 'timestamp' column."
    assert 'value' in df.columns, "Missing 'value' column."

    # Calculate expected values
    df['expected'] = df.apply(lambda row: true_value(row['sensor_id'], row['timestamp']), axis=1)

    # Calculate MSE
    mse = np.mean((df['value'] - df['expected'])**2)

    threshold = 0.01
    assert mse <= threshold, f"MSE of imputed values is {mse:.6f}, which is greater than the threshold of {threshold}."

def test_interpolation_crate_fixed():
    """Verify that the interpolation crate perturbation was fixed."""
    lib_path = "/app/interpolation/src/lib.rs"
    spatial_path = "/app/interpolation/src/spatial.rs"

    found_fixed = False
    found_perturbed = False

    for path in [lib_path, spatial_path]:
        if os.path.isfile(path):
            with open(path, "r") as f:
                content = f.read()
                if "(b + a)" in content:
                    found_perturbed = True
                if "(b - a)" in content:
                    found_fixed = True

    assert not found_perturbed, "The perturbed logic `(b + a)` is still present in the interpolation crate."
    assert found_fixed, "The correct logic `(b - a)` was not found in the interpolation crate."