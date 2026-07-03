# test_final_state.py
import os
import pytest

def test_wal_clean_metric():
    """
    Validates the final metric of success: the total file size of the directory
    /home/user/wal_clean/ must exactly match the expected compacted size.
    """
    d = '/home/user/wal_clean'
    assert os.path.exists(d), f"Directory {d} does not exist."
    assert os.path.isdir(d), f"{d} is not a directory."

    total_size = 0
    for f in os.listdir(d):
        path = os.path.join(d, f)
        if os.path.isfile(path):
            total_size += os.path.getsize(path)

    # Calculate the expected size based on the truth description
    # 10 WAL files
    # Header: 8 bytes
    # 50 Data records per file (interleaved 0x01 and 0x03, originally 100 records)
    # Data record size: 1 (type) + 4 (length) + 64 (payload) = 69 bytes
    # Expected file size = 8 + (50 * 69) = 3458 bytes
    # Total expected size = 10 * 3458 = 34580 bytes
    expected_size = 34580

    assert total_size == expected_size, (
        f"Metric mismatch: Total size of files in {d} is {total_size} bytes, "
        f"but expected exactly {expected_size} bytes."
    )