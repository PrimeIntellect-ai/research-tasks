# test_final_state.py

import os
import json
import pytest

def test_csv_files_created_and_correct():
    """Verify that the CSV files are created with the correct content."""
    base_dir = "/home/user/organized_logs"

    expected_files = {
        "api.csv": [
            "2023-11-01T10:00:01Z,INFO,Request started",
            "2023-11-01T10:00:03Z,WARN,Rate limit approaching"
        ],
        "db.csv": [
            "2023-11-01T10:00:02Z,DEBUG,Connecting to postgres",
            "2023-11-01T10:00:05Z,INFO,Query executed in 5ms"
        ],
        "auth.csv": [
            "2023-11-01T10:00:04Z,ERROR,Invalid token format"
        ]
    }

    for filename, expected_lines in expected_files.items():
        filepath = os.path.join(base_dir, filename)
        assert os.path.isfile(filepath), f"Expected CSV file {filepath} does not exist."

        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        assert lines == expected_lines, f"Content of {filepath} does not match expected output."

def test_summary_json_correct():
    """Verify that summary.json exists and contains the correct counts."""
    summary_path = "/home/user/organized_logs/summary.json"
    assert os.path.isfile(summary_path), f"Summary file {summary_path} does not exist."

    with open(summary_path, 'r') as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {summary_path} is not valid JSON.")

    expected_summary = {"api": 2, "db": 2, "auth": 1}
    assert summary == expected_summary, f"Summary JSON content {summary} does not match expected {expected_summary}."

def test_rust_source_code_atomic_write():
    """Check that the Rust source code uses rename for atomic writes."""
    source_dir = "/home/user/log_transformer"
    assert os.path.exists(source_dir), f"Rust project/script path {source_dir} does not exist."

    # Check all .rs files in the directory recursively
    rust_files = []
    if os.path.isfile(source_dir):
        rust_files.append(source_dir)
    else:
        for root, _, files in os.walk(source_dir):
            for file in files:
                if file.endswith('.rs'):
                    rust_files.append(os.path.join(root, file))

    assert rust_files, f"No Rust source files found in {source_dir}."

    rename_found = False
    for filepath in rust_files:
        with open(filepath, 'r') as f:
            content = f.read()
            if "rename" in content:
                rename_found = True
                break

    assert rename_found, "Could not find 'rename' in the Rust source code. Atomic write requirement likely not met."

def test_binary_exists():
    """Verify that the compiled binary exists at the specified path."""
    binary_path = "/home/user/log_transformer_bin"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"File {binary_path} is not executable."