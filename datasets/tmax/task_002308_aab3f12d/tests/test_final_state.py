# test_final_state.py
import os
import json
import hashlib
import subprocess
import gzip
import csv
import pytest

def test_optimized_logs_size_and_content():
    output_path = "/home/user/optimized_logs.csv.gz"
    assert os.path.exists(output_path), f"File {output_path} does not exist."

    size = os.path.getsize(output_path)
    assert size < 1200000, f"File size {size} bytes is not strictly less than the 1200000 bytes threshold."

    # Recalculate expected valid rows from the source files
    expected_rows = []
    backup_dir = "/home/user/legacy_backups"

    for i in range(50):
        pck_file = os.path.join(backup_dir, f"backup_{i:02d}.pck")
        if not os.path.exists(pck_file):
            continue

        proc = subprocess.run(["/app/pck_unpack", pck_file], capture_output=True, text=True)
        for line in proc.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                payload = data.get("payload", "")
                checksum = data.get("checksum", "")
                if hashlib.md5(payload.encode('utf-8')).hexdigest() == checksum:
                    expected_rows.append((data.get("timestamp", ""), data.get("severity", ""), payload))
            except Exception:
                pass

    # Read the generated CSV
    actual_rows = []
    try:
        with gzip.open(output_path, "rt", encoding="utf-8") as f:
            reader = csv.reader(f)
            headers = next(reader)
            assert headers == ["timestamp", "severity", "payload"], f"Incorrect CSV headers: {headers}"
            for row in reader:
                actual_rows.append(tuple(row))
    except Exception as e:
        pytest.fail(f"Failed to read or parse {output_path}: {e}")

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} valid rows, but got {len(actual_rows)}."

    # Sort both lists to compare contents irrespective of the sorting strategy used for compression
    expected_rows.sort()
    actual_rows.sort()

    assert actual_rows == expected_rows, "The extracted CSV data does not match the expected valid rows from the legacy backups."