# test_final_state.py
import os
import json
import glob
import pytest

ARCHIVE_DIR = "/home/user/archive"

def test_archive_directory_exists():
    assert os.path.isdir(ARCHIVE_DIR), f"Directory {ARCHIVE_DIR} does not exist."

def test_no_temp_files():
    temp_files = glob.glob(os.path.join(ARCHIVE_DIR, "*.tmp"))
    assert not temp_files, f"Found temporary files in archive directory, which violates atomic write requirements: {temp_files}"

def test_archive_files_exist_and_chunked_correctly():
    archive_files = glob.glob(os.path.join(ARCHIVE_DIR, "archive_part_*.jsonl"))
    assert archive_files, "No archive_part_*.jsonl files found in the archive directory."

    total_records = 0
    sources_found = set()
    app_jsonl_count = 0
    web_csv_count = 0

    for file_path in sorted(archive_files):
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()

            # All files except possibly the last should have exactly 10 records
            # Since there are exactly 10 records total in the truth data,
            # we expect exactly 1 file with 10 records.
            if file_path == sorted(archive_files)[-1]:
                assert len(lines) <= 10, f"File {file_path} exceeds the 10 records per chunk limit."
            else:
                assert len(lines) == 10, f"File {file_path} is not the last chunk but does not contain exactly 10 records."

            for line in lines:
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    pytest.fail(f"Invalid JSON line in {file_path}: {line}")

                assert "source" in record, f"Missing 'source' key in record: {record}"
                assert "data" in record, f"Missing 'data' key in record: {record}"

                source = record["source"]
                data = record["data"]
                sources_found.add(source)

                if source == "app.jsonl":
                    assert data.get("level") == "CRITICAL", f"Expected only CRITICAL level for app.jsonl, got: {data}"
                    app_jsonl_count += 1
                elif source == "web.csv":
                    assert data.get("status") == "ERROR", f"Expected only ERROR status for web.csv, got: {data}"
                    web_csv_count += 1
                else:
                    pytest.fail(f"Unexpected source file in archive: {source}")

                total_records += 1

    assert total_records == 10, f"Expected exactly 10 extracted records, found {total_records}."
    assert app_jsonl_count == 6, f"Expected 6 records from app.jsonl, found {app_jsonl_count}."
    assert web_csv_count == 4, f"Expected 4 records from web.csv, found {web_csv_count}."
    assert "app.jsonl" in sources_found, "Missing records from app.jsonl."
    assert "web.csv" in sources_found, "Missing records from web.csv."

def test_exact_expected_file_exists():
    expected_file = os.path.join(ARCHIVE_DIR, "archive_part_001.jsonl")
    assert os.path.isfile(expected_file), f"Expected file {expected_file} was not found. Check chunk naming logic."