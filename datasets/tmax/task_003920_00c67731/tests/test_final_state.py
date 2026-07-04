# test_final_state.py
import os
import hashlib
import pytest

def test_processed_files_content():
    processed_dir = "/home/user/project_data/processed"

    expected_contents = {
        "file1.rle": "Hel*3o Wörld!*3".encode('utf-8'),
        "file2.rle": "a*4b*4c*4D*4".encode('utf-8'),
        "file3.rle": "Just a nôrmal file.*3".encode('utf-8')
    }

    for filename, expected_bytes in expected_contents.items():
        filepath = os.path.join(processed_dir, filename)
        assert os.path.isfile(filepath), f"Processed file {filepath} is missing."

        with open(filepath, "rb") as f:
            content = f.read()

        assert content == expected_bytes, f"Content of {filepath} is incorrect. Expected {expected_bytes}, got {content}."

def test_process_log():
    log_path = "/home/user/project_data/process.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = {
        "PROCESSED: file1.rle",
        "PROCESSED: file2.rle",
        "PROCESSED: file3.rle"
    }

    assert set(lines) == expected_lines, f"Log file {log_path} does not contain the correct entries. Got: {lines}"
    assert len(lines) == len(expected_lines), f"Log file {log_path} contains duplicate or extra entries."

def test_manifest_file():
    manifest_path = "/home/user/project_data/manifest.txt"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing."

    expected_contents = {
        "file1.rle": "Hel*3o Wörld!*3".encode('utf-8'),
        "file2.rle": "a*4b*4c*4D*4".encode('utf-8'),
        "file3.rle": "Just a nôrmal file.*3".encode('utf-8')
    }

    expected_lines = []
    for filename in sorted(expected_contents.keys()):
        content = expected_contents[filename]
        sha256_hash = hashlib.sha256(content).hexdigest()
        expected_lines.append(f"{sha256_hash}  {filename}")

    with open(manifest_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_lines, f"Manifest file {manifest_path} is incorrect. Expected: {expected_lines}, Got: {lines}"