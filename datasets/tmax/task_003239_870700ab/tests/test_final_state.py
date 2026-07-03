# test_final_state.py

import os
import json
import csv
from pathlib import Path

def get_expected_valid_paths():
    """
    Derive the expected valid paths from the JSON files in the incoming directory.
    """
    incoming_dir = Path("/home/user/backups/incoming")
    allowed_root = Path("/home/user/data").resolve()

    valid_entries = []

    if not incoming_dir.exists():
        return valid_entries

    for json_file in incoming_dir.rglob("*.json"):
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)

            backup_id = data.get("backup_id")
            files = data.get("files", [])

            for file_path in files:
                # If path is relative, it's relative to allowed_root
                if not os.path.isabs(file_path):
                    full_path = allowed_root / file_path
                else:
                    full_path = Path(file_path)

                resolved_path = full_path.resolve()

                # Check if resolved path is strictly inside allowed_root
                try:
                    resolved_path.relative_to(allowed_root)
                    valid_entries.append((backup_id, str(resolved_path)))
                except ValueError:
                    # Not inside allowed_root
                    pass
        except Exception:
            pass

    # Sort alphabetically by backup_id, then by valid_file_path
    valid_entries.sort(key=lambda x: (x[0], x[1]))
    return valid_entries

def test_csv_output():
    csv_path = "/home/user/backups/processed_manifest.csv"
    assert os.path.exists(csv_path), f"CSV file does not exist at {csv_path}"

    expected_entries = get_expected_valid_paths()

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV file is empty"
    assert rows[0] == ["backup_id", "valid_file_path"], "CSV header is missing or incorrect"

    actual_entries = [tuple(row) for row in rows[1:]]
    assert actual_entries == expected_entries, (
        f"CSV content mismatch.\nExpected: {expected_entries}\nGot: {actual_entries}"
    )

def test_txt_output():
    txt_path = "/home/user/backups/valid_ids.txt"
    assert os.path.exists(txt_path), f"TXT file does not exist at {txt_path}"

    expected_entries = get_expected_valid_paths()
    expected_ids = sorted(list(set(entry[0] for entry in expected_entries)))

    with open(txt_path, 'r') as f:
        actual_ids = [line.strip() for line in f if line.strip()]

    assert actual_ids == expected_ids, (
        f"TXT content mismatch.\nExpected: {expected_ids}\nGot: {actual_ids}"
    )

def test_python_script_exists():
    script_path = "/home/user/process_backups.py"
    assert os.path.exists(script_path), f"Python script does not exist at {script_path}"