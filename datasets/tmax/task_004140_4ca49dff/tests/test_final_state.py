# test_final_state.py
import os
import json
import sqlite3
import pytest

REPORT_PATH = '/home/user/chain_report.json'
DB_PATH = '/home/user/backups.db'

def get_expected_chains(db_path):
    """
    Derive the expected output directly from the database using a recursive CTE.
    This ensures we match the intent of the rubric regardless of minor data changes.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    query = """
    WITH RECURSIVE
      chain(root_id, job_id, server_id, size_bytes) AS (
        SELECT job_id, job_id, server_id, size_bytes
        FROM jobs
        WHERE parent_id IS NULL

        UNION ALL

        SELECT c.root_id, j.job_id, j.server_id, j.size_bytes
        FROM jobs j
        JOIN chain c ON j.parent_id = c.job_id
      )
    SELECT 
      s.hostname,
      c.root_id,
      SUM(c.size_bytes) as total_size,
      COUNT(c.job_id) as job_count
    FROM chain c
    JOIN servers s ON c.server_id = s.server_id
    GROUP BY c.root_id, s.hostname
    HAVING total_size > 5000
    ORDER BY c.root_id ASC
    """

    c.execute(query)
    rows = c.fetchall()

    expected = {}
    for row in rows:
        hostname = row['hostname']
        if hostname not in expected:
            expected[hostname] = []
        expected[hostname].append({
            "root_job_id": row['root_id'],
            "total_size": row['total_size'],
            "job_count": row['job_count']
        })

    conn.close()
    return expected

def test_chain_report_exists():
    assert os.path.exists(REPORT_PATH), f"The output file {REPORT_PATH} was not found."
    assert os.path.isfile(REPORT_PATH), f"The path {REPORT_PATH} is not a file."

def test_chain_report_content():
    assert os.path.exists(REPORT_PATH), f"Cannot verify content, {REPORT_PATH} is missing."

    with open(REPORT_PATH, 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"The file {REPORT_PATH} does not contain valid JSON. Error: {e}")

    expected_data = get_expected_chains(DB_PATH)

    # Check if the keys (hostnames) match exactly
    assert set(actual_data.keys()) == set(expected_data.keys()), \
        f"Hostnames in report do not match expected. Expected: {list(expected_data.keys())}, Actual: {list(actual_data.keys())}"

    # Check the lists of chains for each hostname
    for hostname, expected_chains in expected_data.items():
        actual_chains = actual_data[hostname]

        assert isinstance(actual_chains, list), f"The value for '{hostname}' must be a list."
        assert len(actual_chains) == len(expected_chains), \
            f"Expected {len(expected_chains)} chains for '{hostname}', but found {len(actual_chains)}."

        # The chains must be sorted by root_job_id in ascending order as per requirements
        for i, (expected_chain, actual_chain) in enumerate(zip(expected_chains, actual_chains)):
            assert actual_chain.get('root_job_id') == expected_chain['root_job_id'], \
                f"Mismatch in root_job_id for '{hostname}' at index {i}. Expected {expected_chain['root_job_id']}, got {actual_chain.get('root_job_id')}."
            assert actual_chain.get('total_size') == expected_chain['total_size'], \
                f"Mismatch in total_size for '{hostname}' chain {expected_chain['root_job_id']}. Expected {expected_chain['total_size']}, got {actual_chain.get('total_size')}."
            assert actual_chain.get('job_count') == expected_chain['job_count'], \
                f"Mismatch in job_count for '{hostname}' chain {expected_chain['root_job_id']}. Expected {expected_chain['job_count']}, got {actual_chain.get('job_count')}."