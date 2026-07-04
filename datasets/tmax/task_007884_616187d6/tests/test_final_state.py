# test_final_state.py
import os
import sqlite3
import pytest

def test_pipeline_log():
    log_path = '/home/user/pipeline.log'
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        log_content = f.read()

    assert "Successfully processed 6 total rows" in log_content, \
        "The log file does not contain the expected success message with the correct row count."

def test_pipeline_cron():
    cron_path = '/home/user/pipeline.cron'
    assert os.path.isfile(cron_path), f"Cron file {cron_path} does not exist."

    with open(cron_path, 'r') as f:
        cron_content = f.read()

    assert "15 * * * *" in cron_content, "The cron file does not schedule the job at minute 15 of every hour."
    assert "/usr/bin/python3" in cron_content and "/home/user/process_pipeline.py" in cron_content, \
        "The cron file does not contain the correct command to execute the pipeline."

def test_database_aggregates():
    db_path = '/home/user/metrics.db'
    assert os.path.isfile(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='hourly_aggregates'")
    assert cursor.fetchone() is not None, "Table 'hourly_aggregates' does not exist in the database."

    # Check data
    cursor.execute("SELECT sensor_id, hour_bucket, avg_reading FROM hourly_aggregates ORDER BY sensor_id, hour_bucket")
    rows = cursor.fetchall()

    expected = [
        ('1', '2023-01-01 00:00:00', 15.0),
        ('1', '2023-01-01 01:00:00', 30.0),
        ('2', '2023-01-01 00:00:00', 100.0),
        ('2', '2023-01-01 01:00:00', 200.0)
    ]

    assert rows == expected, f"Database aggregates do not match the expected values. Got: {rows}"

    conn.close()