# test_final_state.py

import os
import csv
import json
import pytest

def test_extracted_and_renamed_files():
    extracted_dir = "/home/user/artifacts/extracted"
    metadata_file = os.path.join(extracted_dir, "metadata.json")

    assert os.path.isdir(extracted_dir), f"Directory {extracted_dir} does not exist."
    assert os.path.isfile(metadata_file), f"File {metadata_file} does not exist."

    # Read metadata to know what files should exist
    with open(metadata_file, "r") as f:
        metadata = json.load(f)

    for entry in metadata:
        old_id = entry["id"]
        target_name = entry["target_name"]

        old_path = os.path.join(extracted_dir, old_id)
        new_path = os.path.join(extracted_dir, target_name)

        assert not os.path.exists(old_path), f"File {old_path} was not renamed."
        assert os.path.isfile(new_path), f"File {new_path} does not exist. Renaming failed."

def test_verify_go_exists():
    verify_go = "/home/user/artifacts/verify.go"
    assert os.path.isfile(verify_go), f"Go program {verify_go} does not exist."

def test_report_csv_content():
    report_csv = "/home/user/artifacts/report.csv"
    assert os.path.isfile(report_csv), f"Report file {report_csv} does not exist."

    expected_rows = {
        "release_v1.0.0-linux-amd64.bin": "true",
        "release_v1.0.0-darwin-arm64.bin": "true",
        "release_v1.0.0-windows-amd64.exe": "false"
    }

    with open(report_csv, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The CSV file is empty."

    header = rows[0]
    assert header == ["TargetName", "Match"], f"CSV header is incorrect. Expected ['TargetName', 'Match'], got {header}"

    actual_rows = {}
    for row in rows[1:]:
        assert len(row) == 2, f"Invalid CSV row length: {row}"
        actual_rows[row[0]] = row[1].lower()

    for target_name, expected_match in expected_rows.items():
        assert target_name in actual_rows, f"Missing target name {target_name} in CSV report."
        assert actual_rows[target_name] == expected_match, f"Expected match value '{expected_match}' for {target_name}, got '{actual_rows[target_name]}'."

    assert len(actual_rows) == len(expected_rows), "CSV contains unexpected extra rows."