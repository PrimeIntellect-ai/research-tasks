# test_final_state.py

import os
import csv
import pytest

def test_extracted_backup_exists():
    """Verify that the extracted backup directory exists."""
    assert os.path.isdir("/home/user/extracted_backup"), "/home/user/extracted_backup/ directory does not exist. Did you extract the archive?"

def test_process_script_exists_and_atomic():
    """Verify that process.py exists and uses atomic write operations."""
    script_path = "/home/user/process.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for atomic rename/replace/move
    has_atomic = any(func in content for func in ["os.rename", "os.replace", "shutil.move"])
    assert has_atomic, "The script does not appear to use os.rename, os.replace, or shutil.move for atomic writes."

def test_csv_chunks_content():
    """Verify the contents of the generated CSV chunk files."""
    expected_chunks = {
        "chunk_0.csv": [
            ["id", "name", "timestamp"],
            ["1", "Dave", "2023-01-04"],
            ["3", "Frank", "2023-01-06"],
            ["5", "Alice", "2023-01-01"]
        ],
        "chunk_1.csv": [
            ["id", "name", "timestamp"],
            ["8", "Charlie", "2023-01-03"],
            ["9", "Grace", "2023-01-07"],
            ["12", "Bob", "2023-01-02"]
        ],
        "chunk_2.csv": [
            ["id", "name", "timestamp"],
            ["15", "Eve", "2023-01-05"]
        ]
    }

    csv_dir = "/home/user/processed_csv"
    assert os.path.isdir(csv_dir), f"Directory {csv_dir} does not exist."

    for filename, expected_rows in expected_chunks.items():
        filepath = os.path.join(csv_dir, filename)
        assert os.path.isfile(filepath), f"Expected CSV file {filepath} is missing."

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            actual_rows = list(reader)

        assert actual_rows == expected_rows, f"Content of {filename} does not match the expected output. Got {actual_rows}, expected {expected_rows}."

def test_no_extra_chunks():
    """Verify that no extra chunk files were created."""
    csv_dir = "/home/user/processed_csv"
    if os.path.isdir(csv_dir):
        files = [f for f in os.listdir(csv_dir) if f.startswith("chunk_") and f.endswith(".csv")]
        assert len(files) == 3, f"Expected exactly 3 chunk files, but found {len(files)}: {files}"