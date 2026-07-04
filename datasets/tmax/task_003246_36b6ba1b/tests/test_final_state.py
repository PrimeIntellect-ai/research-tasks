# test_final_state.py

import os
import sqlite3
import pandas as pd
import numpy as np

def test_final_files_exist():
    """
    Verify that the outputs of the task exist.
    """
    expected_files = [
        "/home/user/pipeline.log",
        "/home/user/system_metrics.db",
        "/home/user/final_output.csv"
    ]

    for file_path in expected_files:
        assert os.path.exists(file_path), f"Missing expected output file: {file_path}"
        assert os.path.isfile(file_path), f"Expected a file, but found something else: {file_path}"
        assert os.path.getsize(file_path) > 0, f"Output file is empty: {file_path}"

def test_database_table_exists():
    """
    Verify that the SQLite database contains the expected table.
    """
    db_path = "/home/user/system_metrics.db"
    assert os.path.exists(db_path), f"Database missing: {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cleaned_metrics';")
    table = cursor.fetchone()
    conn.close()

    assert table is not None, "Table 'cleaned_metrics' not found in the database."

def test_mse_threshold():
    """
    Verify that the Mean Squared Error (MSE) of normalized_latency is within the acceptable threshold.
    """
    agent_csv = '/home/user/final_output.csv'
    truth_csv = '/app/hidden_truth.csv'

    assert os.path.exists(agent_csv), f"Agent output missing: {agent_csv}"
    assert os.path.exists(truth_csv), f"Truth file missing: {truth_csv}"

    try:
        agent_df = pd.read_csv(agent_csv)
        truth_df = pd.read_csv(truth_csv)

        # Merge on timestamp to align
        merged = pd.merge(truth_df, agent_df, on='timestamp', suffixes=('_true', '_agent'))

        # Ensure we have data to compare
        assert not merged.empty, "Merged dataframe is empty. Timestamps may not align or formats are incorrect."

        mse = np.mean((merged['normalized_latency_true'] - merged['normalized_latency_agent'])**2)
    except Exception as e:
        mse = 9999.0
        assert False, f"Failed to compute MSE due to exception: {e}"

    threshold = 2.5
    assert mse <= threshold, f"MSE of normalized_latency is {mse}, which exceeds the threshold of {threshold}."