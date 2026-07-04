# test_final_state.py

import os
import sqlite3
import pytest

def test_c_parser_exists():
    assert os.path.isfile('/home/user/parser.c'), "C source code /home/user/parser.c does not exist."
    assert os.path.isfile('/home/user/parser'), "Compiled executable /home/user/parser does not exist."
    assert os.access('/home/user/parser', os.X_OK), "/home/user/parser is not executable."

def test_parsed_logs_csv():
    csv_path = '/home/user/parsed_logs.csv'
    assert os.path.isfile(csv_path), f"{csv_path} does not exist."

    with open(csv_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, f"{csv_path} is empty."
    assert lines[0] == "timestamp,username,action,resource", f"Incorrect header in {csv_path}."

    expected_records = [
        "2023-10-01 12:00:00,user1,WRITE,/data/fileA.txt",
        "2023-10-01 12:00:00,user1,WRITE,/data/fileB.txt",
        "2023-10-01 12:05:00,user2,READ,/data/fileA.txt",
        "2023-10-01 12:10:00,user1,WRITE,/data/fileB.txt",
        "2023-10-01 12:10:00,user1,WRITE,/data/fileC.txt",
        "2023-10-01 12:10:00,user1,WRITE,/data/fileD.txt",
        "2023-10-01 12:15:00,user3,WRITE,/data/fileB.txt",
        "2023-10-01 12:15:00,user3,WRITE,/data/fileD.txt",
        "2023-10-01 12:20:00,user4,WRITE,/data/fileE.txt",
        "2023-10-01 12:25:00,user2,READ,/data/fileC.txt",
        "2023-10-01 12:25:00,user2,READ,/data/fileE.txt",
        "2023-10-01 12:30:00,user5,WRITE,/data/fileA.txt",
        "2023-10-01 12:30:00,user5,WRITE,/data/fileB.txt"
    ]

    assert lines[1:] == expected_records, f"Parsed records in {csv_path} do not match the expected output."

def test_sqlite_db_exists():
    db_path = '/home/user/audit.db'
    assert os.path.isfile(db_path), f"Database {db_path} does not exist."

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='logs';")
        table = cursor.fetchone()
        assert table is not None, "Table 'logs' does not exist in the database."
        conn.close()
    except sqlite3.Error as e:
        pytest.fail(f"Failed to connect to SQLite database or query 'logs' table: {e}")

def test_top_writes_csv():
    csv_path = '/home/user/top_writes.csv'
    assert os.path.isfile(csv_path), f"{csv_path} does not exist."

    with open(csv_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/data/fileB.txt,4",
        "/data/fileA.txt,2",
        "/data/fileD.txt,2"
    ]

    assert lines == expected_lines, f"Contents of {csv_path} do not match expected top writes."

def test_c_parser_uses_iconv():
    c_source_path = '/home/user/parser.c'
    assert os.path.isfile(c_source_path), f"{c_source_path} does not exist."

    with open(c_source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "iconv" in content, f"C source code {c_source_path} does not appear to use the iconv library."