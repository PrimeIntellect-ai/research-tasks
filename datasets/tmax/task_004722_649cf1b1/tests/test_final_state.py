# test_final_state.py

import os
import sqlite3
import pandas as pd
from sklearn.metrics import f1_score
import pytest

def get_ground_truth(db_path):
    conn = sqlite3.connect(db_path)
    query = """
    WITH NewerStats AS (
        SELECT 
            chunk_id,
            is_encrypted,
            chunk_size,
            COUNT(*) OVER w as newer_count,
            SUM(chunk_size) OVER w as newer_sum_size
        FROM chunks
        WINDOW w AS (
            PARTITION BY server_id, file_path_hash 
            ORDER BY timestamp DESC 
            ROWS BETWEEN UNBOUNDED PRECEDING AND 1 PRECEDING
        )
    )
    SELECT chunk_id FROM NewerStats 
    WHERE is_encrypted = 0 
      AND newer_count >= 3 
      AND newer_sum_size > (2.5 * chunk_size)
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return set(df['chunk_id'])

def test_obsolete_chunks_f1_score():
    csv_path = '/home/user/obsolete_chunks.csv'
    db_path = '/home/user/backups.sqlite'

    assert os.path.exists(csv_path), f"Agent output file not found at {csv_path}"

    try:
        agent_df = pd.read_csv(csv_path)
        assert 'chunk_id' in agent_df.columns, "CSV must contain a 'chunk_id' column"
        agent_set = set(agent_df['chunk_id'])
    except Exception as e:
        pytest.fail(f"Failed to read {csv_path} or extract chunk_id: {e}")

    gt_set = get_ground_truth(db_path)

    all_items = gt_set.union(agent_set)
    if not all_items:
        score = 1.0
    else:
        y_true = [1 if x in gt_set else 0 for x in all_items]
        y_pred = [1 if x in agent_set else 0 for x in all_items]
        score = f1_score(y_true, y_pred)

    assert score >= 1.0, f"F1-score is {score:.4f}, expected exactly 1.0. The output does not perfectly match the oracle's logic."