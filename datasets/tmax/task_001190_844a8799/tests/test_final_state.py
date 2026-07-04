# test_final_state.py
import os
import sqlite3
import pytest

def test_c_source_exists():
    assert os.path.exists('/home/user/filter_and_analyze.c'), "The C source file /home/user/filter_and_analyze.c is missing."

def test_report_csv_exists_and_correct():
    csv_path = '/home/user/report.csv'
    assert os.path.exists(csv_path), f"The report file {csv_path} was not generated."

    expected_csv = """sensor_id,epoch_time,reading,prev_reading,difference
101,1005,26.1,25.0,1.1
101,1010,27.0,26.1,0.9
102,1005,14.5,15.0,-0.5
102,1010,14.8,14.5,0.3
103,2005,12.5,10.0,2.5
103,2010,11.0,12.5,-1.5
"""

    with open(csv_path, 'r') as f:
        actual_csv = f.read()

    assert actual_csv.strip() == expected_csv.strip(), "The contents of the report.csv do not match the expected output."

def test_database_unmodified():
    db_path = '/home/user/backup.db'
    assert os.path.exists(db_path), f"{db_path} does not exist."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT count(*) FROM sensor_data")
    count = c.fetchone()[0]
    assert count == 12, f"The original database was modified! Expected 12 rows, but found {count}."

    conn.close()