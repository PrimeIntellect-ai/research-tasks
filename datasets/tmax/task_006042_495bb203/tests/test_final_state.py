# test_final_state.py

import os
import json
import csv
import pytest

def test_script_exists():
    script_path = "/home/user/find_expired.py"
    assert os.path.isfile(script_path), f"Expected script not found at {script_path}"

def test_csv_output():
    csv_path = "/home/user/expired_large_backups.csv"
    assert os.path.isfile(csv_path), f"Expected output CSV not found at {csv_path}"

    base_dir = "/home/user/storage_mounts/"
    expected_records = []

    # Derive expected state directly from the filesystem
    for root, _, files in os.walk(base_dir):
        for filename in files:
            if filename.endswith(".metadata.json"):
                metadata_path = os.path.join(root, filename)
                data_filename = filename[:-len(".metadata.json")] + ".data"
                data_path = os.path.join(root, data_filename)

                with open(metadata_path, 'r') as f:
                    try:
                        metadata = json.load(f)
                    except json.JSONDecodeError:
                        continue

                if metadata.get("retention_policy") == "expired" and metadata.get("size_mb", 0) > 500:
                    expected_records.append((data_path, str(metadata["size_mb"])))

    # Read the actual CSV
    actual_records = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            assert len(row) == 2, f"Invalid CSV format in row: {row}. Expected 2 columns."
            actual_records.append((row[0].strip(), row[1].strip()))

    # Sort both lists for order-independent comparison
    expected_records.sort()
    actual_records.sort()

    assert actual_records == expected_records, (
        f"CSV contents do not match expected records.\n"
        f"Expected: {expected_records}\n"
        f"Actual: {actual_records}"
    )