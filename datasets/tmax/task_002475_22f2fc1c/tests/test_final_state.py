# test_final_state.py
import os
import zipfile
import json
import pytest

def test_zip_exists():
    """Test that the output zip file exists."""
    zip_path = '/home/user/outgoing/payload.zip'
    assert os.path.isfile(zip_path), f"The output zip file {zip_path} is missing. The daemon may not have processed the archive."

def test_zip_contents():
    """Test that the output zip file contains the correct chunked and untouched files."""
    zip_path = '/home/user/outgoing/payload.zip'
    assert os.path.isfile(zip_path), f"The output zip file {zip_path} is missing."

    with zipfile.ZipFile(zip_path, 'r') as zf:
        namelist = zf.namelist()

        expected_files = [
            'massive_data.bin.part0',
            'massive_data.bin.part1',
            'massive_data.bin.part2',
            'info.txt',
            'edge_case.bin'
        ]

        for ef in expected_files:
            assert any(f.endswith(ef) for f in namelist), f"Expected file {ef} not found in zip archive."

        assert not any(f.endswith('massive_data.bin') or f == 'massive_data.bin' for f in namelist), \
            "The original unchunked file massive_data.bin was found in the zip. It should have been removed after chunking."

def test_log_file():
    """Test that the JSONL log file contains the correct entry."""
    log_path = '/home/user/artifact_log.jsonl'
    assert os.path.isfile(log_path), f"The log file {log_path} is missing."

    with open(log_path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) >= 1, "Log file is empty."

    parsed = None
    for line in lines:
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            if data.get("original_archive") == "payload.tar.gz":
                parsed = data
                break
        except json.JSONDecodeError:
            continue

    assert parsed is not None, "Could not find a valid JSON log entry for 'payload.tar.gz'."

    assert parsed.get("repackaged_archive") == "payload.zip", "The 'repackaged_archive' value is incorrect."

    chunked_files = parsed.get("chunked_files", {})
    assert "massive_data.bin" in chunked_files, "'massive_data.bin' is missing from the 'chunked_files' object."
    assert chunked_files["massive_data.bin"] == 3, "'massive_data.bin' should be chunked into exactly 3 parts."
    assert len(chunked_files) == 1, "The 'chunked_files' object should only contain files that were actually chunked (only massive_data.bin)."