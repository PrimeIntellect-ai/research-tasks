# test_final_state.py

import os
import glob
import gzip
import re

def test_recovery_ratio():
    truth_count_path = "/home/user/.hidden/truth_count.txt"
    assert os.path.exists(truth_count_path), "Truth count file is missing."

    with open(truth_count_path, "r") as f:
        total_expected = int(f.read().strip())

    assert total_expected > 0, "Expected total records should be greater than 0."

    arc_files = glob.glob("/home/user/archive/*.arc")
    assert len(arc_files) > 0, "No .arc files found in /home/user/archive/"

    recovered_records = 0
    header_errors = 0

    for arc in arc_files:
        with open(arc, "rb") as f:
            data = f.read()
            if not data.startswith(b"LOG_V1.0"):
                header_errors += 1
                continue
            try:
                decompressed = gzip.decompress(data[8:]).decode('utf-8')
                # Count records by finding the starting bracket pattern
                records = re.findall(r'^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\]', decompressed, re.MULTILINE)
                recovered_records += len(records)
            except Exception as e:
                pass

    assert header_errors == 0, f"Found {header_errors} .arc files with incorrect or missing magic header (expected LOG_V1.0)."

    recovery_ratio = recovered_records / total_expected

    assert recovery_ratio >= 0.95, (
        f"Recovery ratio too low. Expected >= 0.95, got {recovery_ratio:.4f} "
        f"({recovered_records} recovered out of {total_expected} total expected)."
    )