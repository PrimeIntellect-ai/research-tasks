# test_final_state.py
import os
import sqlite3
import csv
import stat

def test_extractor_c_exists():
    path = '/home/user/pipeline/extractor.c'
    assert os.path.isfile(path), f"Source file {path} is missing."
    with open(path, 'r') as f:
        content = f.read()
        assert 'sqlite3_bind' in content, "The C source code does not appear to use sqlite3_bind_* for parameter binding."

def test_extractor_executable_exists():
    path = '/home/user/pipeline/extractor'
    assert os.path.isfile(path), f"Executable {path} is missing."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_alerts_csv_content():
    db_path = '/home/user/data/legacy_telemetry.db'
    csv_path = '/home/user/pipeline/alerts.csv'

    assert os.path.isfile(csv_path), f"Output file {csv_path} is missing."

    # Compute expected truth from the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
    WITH MovingAvgs AS (
        SELECT 
            device_uid, 
            recorded_at, 
            val,
            AVG(val) OVER (
                PARTITION BY device_uid 
                ORDER BY recorded_at 
                ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
            ) as m_avg
        FROM raw_telemetry
    )
    SELECT device_uid, recorded_at, val, m_avg FROM MovingAvgs WHERE m_avg > 50.0;
    """
    cursor.execute(query)
    expected_rows = cursor.fetchall()
    conn.close()

    expected_data = []
    for row in expected_rows:
        expected_data.append({
            'device': str(row[0]),
            'timestamp': str(row[1]),
            'reading': f"{row[2]:.2f}",
            'moving_average': f"{row[3]:.2f}"
        })

    # Sort expected data
    expected_data.sort(key=lambda x: (x['device'], int(x['timestamp'])))

    # Read actual CSV
    actual_data = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ['device', 'timestamp', 'reading', 'moving_average'], "CSV header is incorrect."
        for row in reader:
            actual_data.append(row)

    # Sort actual data
    actual_data.sort(key=lambda x: (x['device'], int(x['timestamp'])))

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} rows in CSV, found {len(actual_data)}."

    for actual, expected in zip(actual_data, expected_data):
        assert actual == expected, f"Row mismatch. Expected {expected}, got {actual}."