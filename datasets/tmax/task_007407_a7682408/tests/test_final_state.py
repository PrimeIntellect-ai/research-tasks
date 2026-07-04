# test_final_state.py
import os
import json

def test_backup_files_exist():
    expected_files = [
        "/home/user/dataset/backup/data1.dat",
        "/home/user/dataset/backup/data2.dat",
        "/home/user/dataset/backup/data3.dat",
        "/home/user/dataset/backup/data4.dat",
    ]
    for f in expected_files:
        assert os.path.isfile(f), f"Expected backed up file {f} is missing."

def test_manifest_content():
    manifest_path = "/home/user/dataset/backup/manifest.jsonl"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

    with open(manifest_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Manifest should contain exactly 4 lines, found {len(lines)}."

    records = {}
    for i, line in enumerate(lines):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            assert False, f"Line {i+1} in manifest is not valid JSON: {line}"

        assert "file" in record, f"Record missing 'file' key: {line}"
        records[record["file"]] = record

    expected_files = ["data1.dat", "data2.dat", "data3.dat", "data4.dat"]
    for ef in expected_files:
        assert ef in records, f"Manifest is missing record for {ef}."

    # Check specific values for data3.dat
    data3 = records["data3.dat"]
    assert data3.get("timestamp") == 1600000200, f"data3.dat timestamp incorrect: {data3.get('timestamp')}"
    assert float(data3.get("avg")) == 25.0, f"data3.dat avg incorrect: {data3.get('avg')}"

    # Check specific values for data4.dat
    data4 = records["data4.dat"]
    assert data4.get("timestamp") == 1600000300, f"data4.dat timestamp incorrect: {data4.get('timestamp')}"
    assert float(data4.get("avg")) == 150.15, f"data4.dat avg incorrect: {data4.get('avg')}"