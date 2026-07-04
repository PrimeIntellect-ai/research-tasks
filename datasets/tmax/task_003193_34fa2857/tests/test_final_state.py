# test_final_state.py

import os
import sqlite3
import pandas as pd
import pytest

def test_report_accuracy():
    """
    Test that the agent's report.csv meets the required accuracy threshold
    compared to the expected golden truth.
    """
    db_path = '/home/user/backups.db'
    report_path = '/home/user/report.csv'

    assert os.path.isfile(db_path), f"Database file {db_path} is missing."
    assert os.path.isfile(report_path), f"Agent's report file {report_path} is missing."

    # Generate Golden Truth
    conn = sqlite3.connect(db_path)
    query = """
    WITH RECURSIVE job_chain AS (
        SELECT job_id, parent_job_id, status, size_bytes, start_time
        FROM backup_jobs
        WHERE job_id = 10000
        UNION ALL
        SELECT b.job_id, b.parent_job_id, b.status, b.size_bytes, b.start_time
        FROM backup_jobs b
        INNER JOIN job_chain jc ON b.parent_job_id = jc.job_id
    ),
    cumulative AS (
        SELECT job_id, parent_job_id, status, 
               SUM(size_bytes) OVER (ORDER BY start_time) as cumulative_size
        FROM job_chain
    )
    SELECT job_id FROM cumulative 
    WHERE status = 'FAILED' 
    ORDER BY cumulative_size DESC 
    LIMIT 50;
    """
    try:
        expected_df = pd.read_sql_query(query, conn)
        expected_ids = set(expected_df['job_id'].astype(int).tolist())
    except Exception as e:
        conn.close()
        pytest.fail(f"Failed to generate golden truth from database: {e}")
    finally:
        conn.close()

    # Evaluate Agent's Output
    try:
        agent_df = pd.read_csv(report_path)
        assert 'job_id' in agent_df.columns, "The agent's CSV must contain a 'job_id' column."
        agent_ids = set(agent_df['job_id'].astype(int).tolist())
    except Exception as e:
        pytest.fail(f"Failed to read or parse the agent's report.csv: {e}")

    intersection = len(expected_ids.intersection(agent_ids))
    union = len(expected_ids.union(agent_ids))
    accuracy = intersection / union if union > 0 else 0.0

    threshold = 0.95
    assert accuracy >= threshold, (
        f"Accuracy metric failed. "
        f"Calculated Jaccard similarity (accuracy): {accuracy:.4f}, "
        f"Required threshold: >= {threshold}. "
        f"Expected {len(expected_ids)} job_ids, got {len(agent_ids)} job_ids."
    )