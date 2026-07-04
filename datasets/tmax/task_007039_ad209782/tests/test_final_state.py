# test_final_state.py
import os
import sqlite3
import csv

def test_index_exists():
    db_path = '/home/user/telemetry.db'
    assert os.path.exists(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA index_list('logs')")
    indexes = cursor.fetchall()

    has_valid_index = False
    for idx in indexes:
        idx_name = idx[1]
        cursor.execute(f"PRAGMA index_info('{idx_name}')")
        cols = [row[2] for row in cursor.fetchall()]
        # The index should be on device_id and signal_strength for optimal partitioning and sorting
        if len(cols) >= 2 and set(cols[:2]) == {'device_id', 'signal_strength'}:
            has_valid_index = True
            break

    conn.close()
    assert has_valid_index, "Missing index on `device_id` and `signal_strength` in `logs` table."

def test_csv_exists_and_content():
    csv_path = '/home/user/top_signals.csv'
    assert os.path.exists(csv_path), f"{csv_path} does not exist. Did you run the C++ program?"

    db_path = '/home/user/telemetry.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Compute expected results using Python and SQLite
    cursor.execute("""
        SELECT device_id, epoch_sec, signal_strength,
               RANK() OVER(PARTITION BY device_id ORDER BY signal_strength DESC) as rank
        FROM logs
        WHERE signal_strength IS NOT NULL 
          AND signal_strength >= -100.0 
          AND signal_strength <= 0.0
    """)
    rows = cursor.fetchall()
    conn.close()

    expected_rows = []
    for r in rows:
        if r[3] <= 3:
            expected_rows.append(r)

    # Sort expected: device_id asc, rank asc
    expected_rows.sort(key=lambda x: (x[0], x[3]))

    # Read actual CSV
    actual_rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row: 
                continue
            try:
                actual_rows.append((row[0], int(row[1]), float(row[2]), int(row[3])))
            except ValueError as e:
                assert False, f"Invalid format in CSV row: {row}. Error: {e}"

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in CSV, got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch: expected {expected}, got {actual}."

def test_csv_no_out_of_bounds():
    csv_path = '/home/user/top_signals.csv'
    if not os.path.exists(csv_path):
        return # Handled by previous test

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row: continue
            signal_strength = float(row[2])
            assert -100.0 <= signal_strength <= 0.0, f"Found out-of-bounds signal_strength {signal_strength} in CSV."