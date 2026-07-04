# test_final_state.py

import os
import gzip
import json
import pytest

def test_archive_json_gz_exists_and_correct():
    archive_path = "/home/user/archive.json.gz"

    # 1. Verify /home/user/archive.json.gz exists.
    assert os.path.exists(archive_path), f"File {archive_path} does not exist."
    assert os.path.isfile(archive_path), f"{archive_path} is not a file."

    # 2. Read and uncompress /home/user/archive.json.gz.
    try:
        with gzip.open(archive_path, "rt", encoding="utf-8") as f:
            lines = f.read().strip().split('\n')
    except Exception as e:
        pytest.fail(f"Failed to read or decompress {archive_path}: {e}")

    # 3. Check that it contains exactly 6 lines of JSON objects.
    # Filter out any empty lines just in case, though strip() handles trailing newlines
    lines = [line for line in lines if line.strip()]
    assert len(lines) == 6, f"Expected exactly 6 lines in the archive, found {len(lines)}."

    expected_data = [
        {"timestamp": "2023-10-01T10:00:00Z", "level": "INFO", "message": "Backup service started"},
        {"timestamp": "2023-10-01T10:05:00Z", "level": "DEBUG", "message": "Scanning directories"},
        {"timestamp": "2023-10-01T10:10:00Z", "level": "WARN", "message": "File locked by another process"},
        {"timestamp": "2023-10-01T10:15:00Z", "level": "INFO", "message": "Retrying locked file"},
        {"timestamp": "2023-10-01T10:20:00Z", "level": "ERROR", "message": "Failed to backup file"},
        {"timestamp": "2023-10-01T10:25:00Z", "level": "INFO", "message": "Backup service shutting down"}
    ]

    # 4. Check that the parsed JSON objects match the original data in the correct order
    for idx, (line, expected) in enumerate(zip(lines, expected_data)):
        try:
            parsed_json = json.loads(line)
        except json.JSONDecodeError as e:
            pytest.fail(f"Line {idx + 1} is not valid JSON: {e}\nLine content: {line}")

        assert parsed_json == expected, f"Mismatch at line {idx + 1}.\nExpected: {expected}\nGot:      {parsed_json}"