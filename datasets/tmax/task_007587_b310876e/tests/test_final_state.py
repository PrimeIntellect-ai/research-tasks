# test_final_state.py

import os
import json

def test_backup_manifest_exists():
    file_path = "/home/user/backup_manifest.json"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you run the script?"

def test_backup_manifest_content():
    file_path = "/home/user/backup_manifest.json"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {file_path} does not contain valid JSON."

    expected_manifest = [
        {
            "database": "logs_db",
            "policy": "weekly_full"
        },
        {
            "database": "payments_db",
            "policy": "daily_incremental"
        },
        {
            "database": "users_db",
            "policy": "hourly_snapshot"
        }
    ]

    assert isinstance(manifest, list), f"Expected the JSON in {file_path} to be a list of objects."
    assert len(manifest) == len(expected_manifest), f"Expected exactly {len(expected_manifest)} entries in the manifest, found {len(manifest)}."

    # The task specifies it must be sorted alphabetically by database name
    assert manifest == expected_manifest, f"The content of {file_path} does not match the expected output. Make sure the SPARQL query is fixed to avoid cross joins and the output is sorted."