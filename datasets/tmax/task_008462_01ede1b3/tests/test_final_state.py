# test_final_state.py

import os
import ast

def test_extract_script_exists_and_uses_flock():
    script_path = "/home/user/extract_data.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    with open(script_path, "r") as f:
        code = f.read()

    assert "fcntl" in code, "The script does not import or use the fcntl module."
    assert "flock" in code, "The script does not use fcntl.flock to acquire a lock."

def test_wal_file_truncated():
    wal_path = "/home/user/sensor_data.wal"
    assert os.path.exists(wal_path), f"WAL file {wal_path} is missing. It should be truncated, not deleted."
    assert os.path.getsize(wal_path) == 0, f"WAL file {wal_path} was not truncated to 0 bytes."

def test_clean_data_csv_content():
    csv_path = "/home/user/clean_data.csv"
    assert os.path.exists(csv_path), f"Output file {csv_path} does not exist."

    with open(csv_path, "r") as f:
        csv_content = f.read().strip()

    expected_csv = (
        "sensor_id,timestamp,reading\n"
        "S1,2023-10-01T10:00:00Z,42.5\n"
        "S3,2023-10-01T10:00:02Z,41.9\n"
        "S1,2023-10-01T10:00:03Z,42.0"
    )

    assert csv_content == expected_csv, (
        f"CSV content does not match expected output.\n"
        f"Expected:\n{expected_csv}\n\n"
        f"Got:\n{csv_content}"
    )