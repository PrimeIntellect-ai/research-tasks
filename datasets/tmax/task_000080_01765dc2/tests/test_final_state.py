# test_final_state.py

import os
import time
import subprocess
import sqlite3
import pandas as pd
import pytest

def test_process_script_execution_and_output():
    script_path = "/home/user/process.sh"
    db_path = "/home/user/data/warehouse.db"
    report_path = "/home/user/report.csv"

    assert os.path.exists(script_path), f"{script_path} does not exist."
    assert os.path.exists(db_path), f"{db_path} does not exist."

    # Remove report.csv if it exists to ensure we generate a new one
    if os.path.exists(report_path):
        os.remove(report_path)

    # Run the script and measure time
    start_time = time.time()
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    end_time = time.time()

    duration = end_time - start_time

    assert result.returncode == 0, f"process.sh failed with error:\n{result.stderr}"
    assert duration <= 1.5, f"Execution time {duration:.2f}s exceeded the 1.5s threshold."

    assert os.path.exists(report_path), f"{report_path} was not generated."

    # Calculate the expected truth directly from the database
    conn = sqlite3.connect(db_path)
    query = """
    SELECT r.region_name, SUM(t.amount) as total_volume
    FROM regions r
    JOIN accounts a ON r.region_id = a.region_id
    JOIN transactions t ON a.account_id = t.account_id
    WHERE a.status = 'active'
    GROUP BY r.region_name
    ORDER BY total_volume DESC
    """
    expected_df = pd.read_sql_query(query, conn)
    conn.close()

    # Read the actual output
    try:
        actual_df = pd.read_csv(report_path, header=None, names=['region_name', 'total_volume'])
    except Exception as e:
        pytest.fail(f"Failed to read {report_path}: {e}")

    assert len(actual_df) == len(expected_df), f"Mismatch in number of rows in report.csv. Expected {len(expected_df)}, got {len(actual_df)}."

    # Compare the results row by row
    for i in range(len(expected_df)):
        expected_region = expected_df.iloc[i]['region_name']
        actual_region = actual_df.iloc[i]['region_name']
        assert actual_region == expected_region, f"Row {i}: Expected region '{expected_region}', got '{actual_region}'."

        expected_vol = float(expected_df.iloc[i]['total_volume'])
        actual_vol = float(actual_df.iloc[i]['total_volume'])
        assert abs(actual_vol - expected_vol) < 1e-2, f"Row {i}: Expected volume {expected_vol}, got {actual_vol}."