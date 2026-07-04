# test_final_state.py

import os
import csv
import pytest

def test_output_csv_exists():
    output_csv_path = "/home/user/etl_pipeline/output.csv"
    assert os.path.isfile(output_csv_path), f"Expected output file {output_csv_path} does not exist. Did the Rust program run successfully?"

def test_output_csv_content():
    output_csv_path = "/home/user/etl_pipeline/output.csv"
    assert os.path.isfile(output_csv_path), "Output file missing."

    expected_rows = [
        ['id', 'email', 'score', 'comments'],
        ['1', '***@example.com', '85', 'Great service,\nwill use again.'],
        ['4', '***@domain.net', '92', 'Normal comment'],
        ['6', '***@corp.com', '0', 'Zero is valid,\nand it has\nmultiple newlines'],
        ['7', '***', '100', 'Missing at sign']
    ]

    actual_rows = []
    with open(output_csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            actual_rows.append(row)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows (including header), but got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i} mismatch. Expected {expected}, but got {actual}."

def test_rust_source_modified():
    main_rs_path = "/home/user/etl_pipeline/src/main.rs"
    assert os.path.isfile(main_rs_path), "main.rs is missing."
    with open(main_rs_path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "csv" in content or "Reader" in content or "Writer" in content, "main.rs does not seem to use the csv crate."
    assert "Hello, world!" not in content or len(content) > 50, "main.rs appears to be unmodified."