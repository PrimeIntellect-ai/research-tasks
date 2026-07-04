# test_final_state.py
import os
import json
import hashlib

def test_archived_files():
    archive_dir = "/home/user/archived_gcode"
    assert os.path.isdir(archive_dir), f"Directory {archive_dir} does not exist"

    expected_files = ["print1.gcode", "print2.gcode", "print3.gcode"]
    for f in expected_files:
        path = os.path.join(archive_dir, f)
        assert os.path.isfile(path), f"Expected file {f} is missing from {archive_dir}"

def test_manifest_contents():
    manifest_path = "/home/user/gcode_manifest.jsonl"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} does not exist"

    expected_data = [
        ("print1.gcode", "G1 X10 Y10\nG1 Z0.2\n; filament used [mm] = 15.4\nM104 S0\n", 15.4),
        ("print2.gcode", "G28\nG1 X20 Y20\n; filament used [mm] = 3.2\nM140 S0\n", 3.2),
        ("print3.gcode", "M109 S200\nG1 X30 Y30\n; filament used [mm] = 100.0\nM104 S0\n", 100.0),
    ]

    expected_records = {}
    for fname, content, filament in expected_data:
        sha256 = hashlib.sha256(content.encode('utf-8')).hexdigest()
        expected_records[fname] = {
            "filename": fname,
            "sha256": sha256,
            "filament_mm": filament
        }

    with open(manifest_path, "r") as f:
        lines = f.read().strip().split('\n')

    # Ignore empty lines
    lines = [line for line in lines if line.strip()]

    assert len(lines) == 3, f"Expected 3 records in manifest, found {len(lines)}"

    parsed_records = {}
    for i, line in enumerate(lines):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            assert False, f"Line {i+1} in manifest is not valid JSON: {line}"

        assert "filename" in record, f"Line {i+1} missing 'filename' key"
        parsed_records[record["filename"]] = record

    for fname, expected in expected_records.items():
        assert fname in parsed_records, f"Manifest is missing record for {fname}"
        record = parsed_records[fname]
        assert record["sha256"] == expected["sha256"], f"Incorrect sha256 for {fname}. Expected {expected['sha256']}, got {record['sha256']}"
        assert float(record["filament_mm"]) == expected["filament_mm"], f"Incorrect filament_mm for {fname}. Expected {expected['filament_mm']}, got {record['filament_mm']}"

def test_processing_log_exists():
    log_path = "/home/user/processing.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist"