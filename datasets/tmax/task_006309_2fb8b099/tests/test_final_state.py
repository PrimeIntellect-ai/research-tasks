# test_final_state.py
import os
import re
import csv
import sqlite3
import math

def test_pipeline_log_exists_and_content():
    log_path = '/home/user/pipeline.log'
    assert os.path.isfile(log_path), f"Log file not found at {log_path}"

    with open(log_path, 'r', encoding='utf-8') as f:
        logs = f.read()

    assert "Pipeline started" in logs, "Log file missing 'Pipeline started' message."
    assert "Processed 3000 rows" in logs, "Log file missing 'Processed 3000 rows' message."
    assert "Pipeline finished" in logs, "Log file missing 'Pipeline finished' message."

    # Check log format roughly: 2023-10-25 10:00:00,000 - INFO - Pipeline started
    # Regex for date time - level - message
    pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - (INFO|WARNING|ERROR|DEBUG|CRITICAL) - .+$"
    lines = [line.strip() for line in logs.strip().split('\n') if line.strip()]
    for line in lines:
        assert re.match(pattern, line), f"Log line does not match expected format: {line}"

def test_database_and_metrics():
    db_path = '/home/user/metrics.db'
    csv_path = '/home/user/sensor_data.csv'

    assert os.path.isfile(db_path), f"Database not found at {db_path}"

    # Read CSV and compute expected metrics
    data = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'timestamp': int(row['timestamp']),
                'sensor_id': row['sensor_id'],
                'value': float(row['value'])
            })

    # Sort by timestamp
    data.sort(key=lambda x: x['timestamp'])

    # Group by sensor_id
    grouped = {}
    for row in data:
        grouped.setdefault(row['sensor_id'], []).append(row)

    expected_results = []
    for sensor_id, rows in grouped.items():
        for i in range(len(rows)):
            row = rows[i]
            if i < 4:
                row['rolling_mean'] = None
                row['rolling_std'] = None
            else:
                window = [r['value'] for r in rows[i-4:i+1]]
                mean = sum(window) / 5
                variance = sum((x - mean) ** 2 for x in window) / 4
                std = math.sqrt(variance)
                row['rolling_mean'] = mean
                row['rolling_std'] = std
            expected_results.append(row)

    # Map expected results by (sensor_id, timestamp) for easy lookup
    expected_map = {(r['sensor_id'], r['timestamp']): r for r in expected_results}

    # Connect to DB and verify
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Check table existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rolling_metrics'")
    assert cursor.fetchone() is not None, "Table 'rolling_metrics' does not exist in the database."

    cursor.execute("SELECT * FROM rolling_metrics")
    db_rows = cursor.fetchall()

    assert len(db_rows) == 3000, f"Expected 3000 rows in rolling_metrics, found {len(db_rows)}"

    for db_row in db_rows:
        sensor_id = db_row['sensor_id']
        timestamp = int(db_row['timestamp'])
        value = float(db_row['value'])

        expected = expected_map.get((sensor_id, timestamp))
        assert expected is not None, f"Unexpected row in DB: sensor_id={sensor_id}, timestamp={timestamp}"

        assert math.isclose(value, expected['value'], rel_tol=1e-5), f"Value mismatch for {sensor_id} at {timestamp}"

        db_mean = db_row['rolling_mean']
        db_std = db_row['rolling_std']

        if expected['rolling_mean'] is None:
            # DB might store None, empty string, or NaN. We accept None or math.isnan
            is_null = db_mean is None or db_mean == '' or (isinstance(db_mean, float) and math.isnan(db_mean))
            assert is_null, f"Expected null rolling_mean for {sensor_id} at {timestamp}, got {db_mean}"
        else:
            assert db_mean is not None, f"Expected numeric rolling_mean for {sensor_id} at {timestamp}, got None"
            assert math.isclose(float(db_mean), expected['rolling_mean'], rel_tol=1e-5, abs_tol=1e-5), \
                f"rolling_mean mismatch for {sensor_id} at {timestamp}. Expected {expected['rolling_mean']}, got {db_mean}"

        if expected['rolling_std'] is None:
            is_null = db_std is None or db_std == '' or (isinstance(db_std, float) and math.isnan(db_std))
            assert is_null, f"Expected null rolling_std for {sensor_id} at {timestamp}, got {db_std}"
        else:
            assert db_std is not None, f"Expected numeric rolling_std for {sensor_id} at {timestamp}, got None"
            assert math.isclose(float(db_std), expected['rolling_std'], rel_tol=1e-5, abs_tol=1e-5), \
                f"rolling_std mismatch for {sensor_id} at {timestamp}. Expected {expected['rolling_std']}, got {db_std}"

    conn.close()