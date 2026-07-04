# test_final_state.py
import os
import sqlite3
import pandas as pd
import pytest

def test_database_and_table_exist():
    db_path = "/home/user/tracking.db"
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='positions'")
    table_exists = cursor.fetchone()
    conn.close()

    assert table_exists is not None, "Table 'positions' does not exist in the database."

def test_smoothed_speeds_csv_and_mse():
    agent_csv = "/home/user/smoothed_speeds.csv"
    ref_csv = "/tmp/reference_speeds.csv"

    assert os.path.isfile(agent_csv), f"Output file {agent_csv} does not exist."
    assert os.path.isfile(ref_csv), f"Reference file {ref_csv} does not exist."

    try:
        agent_df = pd.read_csv(agent_csv)
    except Exception as e:
        pytest.fail(f"Failed to read {agent_csv}: {e}")

    try:
        ref_df = pd.read_csv(ref_csv)
    except Exception as e:
        pytest.fail(f"Failed to read {ref_csv}: {e}")

    assert 'frame_id' in agent_df.columns, "'frame_id' column missing from output CSV."
    assert 'moving_avg_distance' in agent_df.columns, "'moving_avg_distance' column missing from output CSV."

    merged = pd.merge(ref_df, agent_df, on='frame_id', suffixes=('_ref', '_agent'))
    assert len(merged) > 0, "No matching frame_ids found between output and reference."

    mse = ((merged['moving_avg_distance_ref'] - merged['moving_avg_distance_agent'])**2).mean()

    assert mse <= 0.5, f"MSE of moving_avg_distance is {mse}, which exceeds the threshold of 0.5."