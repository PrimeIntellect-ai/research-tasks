# test_final_state.py

import os
import struct
import pytest

def test_updates_csv_content():
    """
    Verifies that updates.csv exists and contains the correct alphabetically sorted updates.
    """
    csv_path = "/home/user/updates.csv"
    assert os.path.exists(csv_path), f"File {csv_path} does not exist. Did you redirect stdout to it?"

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "cache_layer,0,5",
        "db_backend,1,2"
    ]

    assert lines == expected_lines, (
        f"CSV content mismatch.\nExpected:\n{expected_lines}\nGot:\n{lines}\n"
        "Ensure you are printing in the format 'app_name,old_version,new_version' "
        "and sorting alphabetically by app_name."
    )

def test_state_bin_updated_correctly():
    """
    Verifies that state.bin has been updated with the new versions and new applications,
    while preserving existing ones and adhering strictly to the 36-byte binary format.
    """
    state_path = "/home/user/state.bin"
    assert os.path.exists(state_path), f"File {state_path} does not exist."

    size = os.path.getsize(state_path)
    assert size % 36 == 0, f"State file size ({size} bytes) is not a multiple of 36 bytes."
    assert size == 144, f"State file size mismatch. Expected 144 bytes (4 records), got {size} bytes."

    records = {}
    with open(state_path, "rb") as f:
        while True:
            data = f.read(36)
            if not data:
                break
            assert len(data) == 36, "Incomplete record found at the end of the file."

            name_bytes, version = struct.unpack("<32si", data)

            try:
                name = name_bytes.rstrip(b'\x00').decode('ascii')
            except UnicodeDecodeError:
                pytest.fail("Failed to decode application name as ASCII. Ensure proper null-padding.")

            records[name] = version

    expected_records = {
        "web_server": 3,
        "db_backend": 2,
        "queue_mgr": 4,
        "cache_layer": 5
    }

    assert records == expected_records, (
        f"State file records mismatch.\nExpected: {expected_records}\nGot: {records}\n"
        "Ensure you are updating existing records properly and appending new ones."
    )