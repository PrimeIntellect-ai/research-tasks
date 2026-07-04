# test_final_state.py

import os
import sqlite3
import pandas as pd
import numpy as np
import pytest

DB_PATH = "/home/user/sensor_graph.db"
CSV_PATH = "/home/user/edges_export.csv"
REF_PATH = "/app/truth/reference.csv"

def test_db_exists_and_schema():
    assert os.path.exists(DB_PATH), f"Database not found at {DB_PATH}"

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='edges'")
    assert cursor.fetchone() is not None, "Table 'edges' does not exist in the database."

    # Check columns
    cursor.execute("PRAGMA table_info(edges)")
    columns = {row[1] for row in cursor.fetchall()}
    assert {'source', 'target', 'weight'}.issubset(columns), f"Table 'edges' is missing required columns. Found: {columns}"

    # Check index on weight
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='edges'")
    indices = [row[0] for row in cursor.fetchall()]

    index_on_weight = False
    for idx in indices:
        if idx and idx.startswith('sqlite_autoindex'):
            continue
        cursor.execute(f"PRAGMA index_info({idx})")
        idx_cols = [row[2] for row in cursor.fetchall()]
        if 'weight' in idx_cols:
            index_on_weight = True
            break

    assert index_on_weight, "No index found on the 'weight' column in the 'edges' table."

    conn.close()

def test_csv_exists_and_format():
    assert os.path.exists(CSV_PATH), f"CSV export not found at {CSV_PATH}"

    df = pd.read_csv(CSV_PATH)
    assert list(df.columns) == ['source', 'target', 'weight'], f"CSV columns are incorrect. Expected ['source', 'target', 'weight'], found: {list(df.columns)}"

    # Check if sorted by weight descending
    weights = df['weight'].tolist()
    assert weights == sorted(weights, reverse=True), "CSV is not sorted by weight descending."

    # Check source < target
    assert (df['source'] < df['target']).all(), "There are rows where source is not less than target."

    # Check weight > 0
    assert (df['weight'] > 0).all(), "There are rows with weight <= 0."

def test_mae_metric():
    assert os.path.exists(CSV_PATH), f"CSV export not found at {CSV_PATH}"
    assert os.path.exists(REF_PATH), f"Reference CSV not found at {REF_PATH}"

    ref = pd.read_csv(REF_PATH).set_index(['source', 'target'])
    pred = pd.read_csv(CSV_PATH).set_index(['source', 'target'])

    # Outer join to catch missing or extra edges
    merged = ref.join(pred, lsuffix='_ref', rsuffix='_pred', how='outer').fillna(0)

    mae = np.mean(np.abs(merged['weight_ref'] - merged['weight_pred']))

    assert mae <= 1.0, f"MAE of edge weights is {mae:.4f}, which is greater than the threshold of 1.0"