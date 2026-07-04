# test_final_state.py
import os
import csv
import hashlib

def test_threat_manifest_exists():
    manifest_path = "/home/user/threat_manifest.csv"
    assert os.path.isfile(manifest_path), f"The threat manifest file was not found at {manifest_path}"

def test_threat_manifest_content():
    manifest_path = "/home/user/threat_manifest.csv"
    assert os.path.isfile(manifest_path), f"The threat manifest file was not found at {manifest_path}"

    # Recompute expected hashes
    def get_hash(content):
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    expected_rows = {
        "102": {
            "path": "/home/user/.ssh/id_rsa",
            "hash": get_hash("fake private key\n")
        },
        "104": {
            "path": "/home/user/app_data_backup/secret.key",
            "hash": get_hash("secret key value\n")
        }
    }

    actual_rows = {}
    with open(manifest_path, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            assert len(row) == 3, f"Invalid CSV format in row: {row}. Expected 3 columns."
            rec_id, path, sha256 = [col.strip() for col in row]
            actual_rows[rec_id] = {"path": path, "hash": sha256}

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} records in manifest, found {len(actual_rows)}."

    for rec_id, expected_data in expected_rows.items():
        assert rec_id in actual_rows, f"Record ID {rec_id} is missing from the manifest."
        assert actual_rows[rec_id]["path"] == expected_data["path"], f"Incorrect normalized path for Record ID {rec_id}. Expected {expected_data['path']}, got {actual_rows[rec_id]['path']}."
        assert actual_rows[rec_id]["hash"] == expected_data["hash"], f"Incorrect SHA256 hash for Record ID {rec_id}. Expected {expected_data['hash']}, got {actual_rows[rec_id]['hash']}."