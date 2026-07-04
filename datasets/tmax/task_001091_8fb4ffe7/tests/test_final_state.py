# test_final_state.py

import os
import json
import struct
import pytest

BASE_DIR = "/home/user"
BACKUPS_DIR = os.path.join(BASE_DIR, "backups")
INVENTORY_CSV = os.path.join(BASE_DIR, "inventory.csv")
REPORT_JSON = os.path.join(BASE_DIR, "audit_report.json")

def get_inventory():
    inventory = {}
    if not os.path.exists(INVENTORY_CSV):
        return inventory
    with open(INVENTORY_CSV, "r", encoding="utf-8") as f:
        lines = f.read().strip().splitlines()
        for line in lines[1:]: # skip header
            if "," in line:
                orig_name, days = line.split(",", 1)
                try:
                    inventory[orig_name.strip()] = int(days.strip())
                except ValueError:
                    pass
    return inventory

def get_expected_report():
    inventory = get_inventory()
    report = []

    if not os.path.exists(BACKUPS_DIR):
        return report

    for filename in os.listdir(BACKUPS_DIR):
        if not filename.endswith(".bkp"):
            continue
        filepath = os.path.join(BACKUPS_DIR, filename)
        with open(filepath, "rb") as f:
            magic = f.read(4)
            if magic != b"BKP1":
                continue

            ts_bytes = f.read(8)
            if len(ts_bytes) < 8:
                continue
            creation_timestamp = struct.unpack("<Q", ts_bytes)[0]

            len_bytes = f.read(2)
            if len(len_bytes) < 2:
                continue
            name_len = struct.unpack("<H", len_bytes)[0]

            orig_name_bytes = f.read(name_len)
            if len(orig_name_bytes) < name_len:
                continue
            original_filename = orig_name_bytes.decode("utf-8")

            retention_days = inventory.get(original_filename, 30)
            expiration_timestamp = creation_timestamp + (retention_days * 86400)

            report.append({
                "archive_filename": filename,
                "original_filename": original_filename,
                "creation_timestamp": creation_timestamp,
                "expiration_timestamp": expiration_timestamp
            })

    report.sort(key=lambda x: x["archive_filename"])
    return report

def test_audit_report_exists():
    assert os.path.isfile(REPORT_JSON), f"File {REPORT_JSON} does not exist. The Rust program must generate this file."

def test_audit_report_content():
    assert os.path.isfile(REPORT_JSON), f"File {REPORT_JSON} does not exist."

    with open(REPORT_JSON, "r", encoding="utf-8") as f:
        try:
            actual_report = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {REPORT_JSON} as JSON: {e}")

    assert isinstance(actual_report, list), f"Expected the JSON root to be an array, got {type(actual_report).__name__}"

    expected_report = get_expected_report()

    assert len(actual_report) == len(expected_report), f"Expected {len(expected_report)} items in the report, got {len(actual_report)}"

    # Check sorting
    actual_filenames = [item.get("archive_filename") for item in actual_report]
    expected_filenames = [item["archive_filename"] for item in expected_report]
    assert actual_filenames == expected_filenames, "The JSON array must be sorted by 'archive_filename' alphabetically."

    for actual, expected in zip(actual_report, expected_report):
        assert actual == expected, f"Mismatch in report item.\nExpected: {expected}\nGot: {actual}"