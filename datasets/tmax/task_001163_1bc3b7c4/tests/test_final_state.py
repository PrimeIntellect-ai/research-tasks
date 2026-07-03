# test_final_state.py

import os
import csv

def test_backup_summary_csv_content():
    csv_path = "/home/user/backup_summary.csv"
    assert os.path.isfile(csv_path), f"File {csv_path} does not exist."

    expected_rows = [
        ['server_id', 'timestamp', 'backup_size'],
        ['srv-01', '2023-10-01T12:00:00Z', '1048576'],
        ['srv-02', '2023-10-01T12:05:00Z', '2048576'],
        ['srv-03', '2023-10-01T12:10:00Z', '512000']
    ]

    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert actual_rows == expected_rows, (
        f"Content of {csv_path} does not match expected output.\n"
        f"Expected: {expected_rows}\n"
        f"Actual: {actual_rows}"
    )

def test_data_json_not_extracted():
    json_path = "/home/user/data.json"
    assert not os.path.exists(json_path), (
        f"File {json_path} was found on disk. The instructions required "
        "reading the stream directly without extracting the file to disk."
    )