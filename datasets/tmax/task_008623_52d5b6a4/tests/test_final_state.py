# test_final_state.py
import os
import csv
import hashlib
import pytest

CSV_FILE = "/home/user/config_history.csv"

def get_expected_data():
    # Defined by the problem statement and truth data
    raw_states = [
        (1600000000, "localhost", 5432, 100),
        (1600000060, "localhost", 5432, 100),
        (1600000120, "db.internal", 5432, 100),
        (1600000180, "db.internal", 5432, 100),
        (1600000240, "db.internal", 5432, 200),
        (1600000300, "localhost", 5432, 100),
    ]

    # Sort chronologically just in case
    raw_states.sort(key=lambda x: x[0])

    deduped_states = []
    last_hash = None

    for ts, host, port, max_conn in raw_states:
        hash_str = f"{host}:{port}:{max_conn}"
        curr_hash = hashlib.sha256(hash_str.encode('utf-8')).hexdigest()

        if curr_hash != last_hash:
            deduped_states.append({
                "timestamp": str(ts),
                "db_host": host,
                "db_port": str(port),
                "max_connections": str(max_conn),
                "config_hash": curr_hash
            })
            last_hash = curr_hash

    return deduped_states

def test_csv_file_exists():
    assert os.path.isfile(CSV_FILE), f"The output file {CSV_FILE} was not found."

def test_csv_headers():
    with open(CSV_FILE, 'r', newline='') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            pytest.fail(f"{CSV_FILE} is empty.")

    expected_headers = ["timestamp", "db_host", "db_port", "max_connections", "config_hash"]
    assert headers == expected_headers, f"CSV headers do not match. Expected {expected_headers}, got {headers}."

def test_csv_content_deduplicated_and_hashed():
    expected_data = get_expected_data()

    actual_data = []
    with open(CSV_FILE, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            actual_data.append(row)

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} rows of data (excluding header), got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."