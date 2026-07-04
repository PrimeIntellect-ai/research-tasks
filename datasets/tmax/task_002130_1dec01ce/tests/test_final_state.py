# test_final_state.py
import os
import json

def test_process_log():
    log_path = '/home/user/process.log'
    assert os.path.isfile(log_path), f"{log_path} is missing."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected_line = "CORRUPT: broken_release.tar.gz"
    assert expected_line in content, f"Expected '{expected_line}' to be in {log_path}, but found: {content}"

def test_archive_backup_contents():
    backup_dir = '/home/user/archive_backup/'
    assert os.path.isdir(backup_dir), f"{backup_dir} is missing."

    files = set(os.listdir(backup_dir))
    expected_files = {'release_v1.tar.gz', 'release_v2.tar.gz'}

    assert files == expected_files, f"Expected {backup_dir} to contain exactly {expected_files}, but found {files}"

def test_doc_db_wal():
    wal_path = '/home/user/doc_db.wal'
    assert os.path.isfile(wal_path), f"{wal_path} is missing."

    with open(wal_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {wal_path}, found {len(lines)}"

    parsed_records = {}
    for line in lines:
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            assert False, f"Failed to parse JSON from line: {line}"

        release_name = record.get("release")
        parsed_records[release_name] = record

    assert "release_v1.tar.gz" in parsed_records, "Missing record for release_v1.tar.gz"
    assert "release_v2.tar.gz" in parsed_records, "Missing record for release_v2.tar.gz"

    # Check v1
    v1 = parsed_records["release_v1.tar.gz"]
    assert "binaries" in v1 and len(v1["binaries"]) == 1, "Invalid binaries list for v1"
    assert v1["binaries"][0]["name"] == "firmware.elf", "Expected firmware.elf in v1 binaries"
    assert isinstance(v1["binaries"][0].get("arch"), str) and len(v1["binaries"][0]["arch"]) > 0, "Missing or invalid architecture for firmware.elf"

    assert "gcode_times" in v1 and len(v1["gcode_times"]) == 1, "Invalid gcode_times list for v1"
    assert v1["gcode_times"][0] == {"name": "test.gcode", "time": "4500s"}, f"Unexpected gcode_times for v1: {v1['gcode_times']}"

    # Check v2
    v2 = parsed_records["release_v2.tar.gz"]
    assert "binaries" in v2 and len(v2["binaries"]) == 1, "Invalid binaries list for v2"
    assert v2["binaries"][0]["name"] == "util.bin", "Expected util.bin in v2 binaries"
    assert isinstance(v2["binaries"][0].get("arch"), str) and len(v2["binaries"][0]["arch"]) > 0, "Missing or invalid architecture for util.bin"

    assert "gcode_times" in v2 and len(v2["gcode_times"]) == 1, "Invalid gcode_times list for v2"
    assert v2["gcode_times"][0] == {"name": "calib.gcode", "time": "120s"}, f"Unexpected gcode_times for v2: {v2['gcode_times']}"