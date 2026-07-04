# test_final_state.py
import os
import glob
import struct
import sqlite3
import pytest

def get_expected_counts():
    total_records = 0
    status_1_count = 0

    files = sorted(glob.glob('/home/user/logs/*.bin'))
    for f in files:
        with open(f, 'rb') as fp:
            magic = fp.read(4)
            if magic != b'LOGS':
                continue
            count_data = fp.read(2)
            if len(count_data) < 2:
                continue
            count = struct.unpack('>H', count_data)[0]

            for _ in range(count):
                ts_data = fp.read(4)
                if len(ts_data) < 4:
                    break
                ts = struct.unpack('>I', ts_data)[0]

                status_data = fp.read(1)
                status = struct.unpack('B', status_data)[0]

                len_data = fp.read(1)
                msg_len = struct.unpack('B', len_data)[0]

                if msg_len == 255:
                    continue

                msg_data = fp.read(msg_len)
                total_records += 1
                if status == 1:
                    status_1_count += 1

    return total_records, status_1_count

def test_status_1_count_file():
    output_path = '/home/user/app/status_1_count.txt'
    assert os.path.isfile(output_path), f"Output file {output_path} is missing. Did you write the final count to it?"

    _, expected_status_1 = get_expected_counts()

    with open(output_path, 'r') as f:
        content = f.read().strip()

    assert content.isdigit(), f"File {output_path} does not contain a valid integer."
    assert int(content) == expected_status_1, f"Expected count {expected_status_1}, but got {content} in {output_path}."

def test_database_records_count():
    db_path = '/home/user/app/logs.db'
    assert os.path.isfile(db_path), f"Database file {db_path} is missing. Did the script run successfully?"

    expected_total, expected_status_1 = get_expected_counts()

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM logs")
    actual_total = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM logs WHERE status = 1")
    actual_status_1 = c.fetchone()[0]

    conn.close()

    assert actual_total == expected_total, f"Expected {expected_total} total records in database, but found {actual_total}. The parsing logic might not be correctly skipping deleted records or might be crashing."
    assert actual_status_1 == expected_status_1, f"Expected {expected_status_1} records with status 1 in database, but found {actual_status_1}."