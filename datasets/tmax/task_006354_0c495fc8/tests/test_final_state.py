# test_final_state.py

import os
import json
import pytest

INVENTORY_FILE = "/home/user/inventory.jsonl"
EXTRACTED_DIR = "/home/user/extracted_assets"
SCRIPT_FILE = "/home/user/organize_docs.py"
ARCHIVE_DIR = "/home/user/doc_archive"

def test_inventory_file_exists_and_contents():
    assert os.path.isfile(INVENTORY_FILE), f"Inventory file {INVENTORY_FILE} does not exist."

    expected_records = [
        {"file": os.path.join(ARCHIVE_DIR, "module1/intro.xml"), "type": "xml", "title": "Introduction to System"},
        {"file": os.path.join(ARCHIVE_DIR, "module1/meta.json"), "type": "json", "author": "Jane Doe"},
        {"file": os.path.join(ARCHIVE_DIR, "module1/textdata.blob"), "type": "blob", "status": "extracted"},
        {"file": os.path.join(ARCHIVE_DIR, "module2/advanced.xml"), "type": "xml", "title": "Advanced Configuration"},
        {"file": os.path.join(ARCHIVE_DIR, "module2/info.json"), "type": "json", "author": "John Smith"},
        {"file": os.path.join(ARCHIVE_DIR, "module2/assets/graphic1.blob"), "type": "blob", "status": "extracted"}
    ]

    actual_records = []
    with open(INVENTORY_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                actual_records.append(json.loads(line))
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON line in {INVENTORY_FILE}: {line}")

    assert len(actual_records) == len(expected_records), f"Expected {len(expected_records)} records, found {len(actual_records)}"

    # Sort both lists by file path to compare
    actual_records.sort(key=lambda x: x.get("file", ""))
    expected_records.sort(key=lambda x: x.get("file", ""))

    for expected, actual in zip(expected_records, actual_records):
        assert expected == actual, f"Record mismatch. Expected: {expected}, Actual: {actual}"

def test_extracted_assets():
    assert os.path.isdir(EXTRACTED_DIR), f"Directory {EXTRACTED_DIR} does not exist."

    graphic1_dat = os.path.join(EXTRACTED_DIR, "graphic1.dat")
    textdata_dat = os.path.join(EXTRACTED_DIR, "textdata.dat")

    assert os.path.isfile(graphic1_dat), f"Extracted file {graphic1_dat} missing."
    assert os.path.isfile(textdata_dat), f"Extracted file {textdata_dat} missing."

    # graphic2.dat should NOT exist
    graphic2_dat = os.path.join(EXTRACTED_DIR, "graphic2.dat")
    assert not os.path.exists(graphic2_dat), f"File {graphic2_dat} should not have been extracted."

    with open(graphic1_dat, "rb") as f:
        assert f.read() == b"\xAA\xBB\xCC\xDD", f"Content of {graphic1_dat} is incorrect."

    with open(textdata_dat, "rb") as f:
        assert f.read() == b"PAYLOAD_DATA_HERE", f"Content of {textdata_dat} is incorrect."

def test_script_uses_file_locking():
    assert os.path.isfile(SCRIPT_FILE), f"Script file {SCRIPT_FILE} does not exist."

    with open(SCRIPT_FILE, "r") as f:
        content = f.read()

    assert "fcntl.flock" in content, f"Script {SCRIPT_FILE} does not appear to use fcntl.flock for file locking."
    assert "fcntl.LOCK_EX" in content, f"Script {SCRIPT_FILE} does not appear to use fcntl.LOCK_EX."