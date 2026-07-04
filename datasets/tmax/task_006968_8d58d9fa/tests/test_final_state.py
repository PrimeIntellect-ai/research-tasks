# test_final_state.py

import os
import csv

def test_script_exists():
    script_path = '/home/user/etl_pipeline.py'
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_output_file_exists():
    output_path = '/home/user/outputs/processed_logs.csv'
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

def test_output_content_and_encoding():
    output_path = '/home/user/outputs/processed_logs.csv'

    # Try reading with utf-8 encoding
    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            actual_rows = list(reader)
    except UnicodeDecodeError:
        assert False, f"The output file {output_path} is not properly utf-8 encoded."
    except Exception as e:
        assert False, f"Failed to read {output_path}: {e}"

    expected_rows = [
        ['timestamp', 'masked_ip', 'masked_email', 'rolling_count'],
        ['1700000000', '192.168.1.XXX', 'a***@example.com', '1'],
        ['1700000010', '192.168.1.XXX', 'b***@test.org', '2'],
        ['1700000030', '192.168.1.XXX', 'a***@example.com', '3'],
        ['1700000050', '10.0.0.XXX', 'c***@foo.net', '1'],
        ['1700000070', '192.168.1.XXX', 'd***@bar.com', '3'],
        ['1700000100', '192.168.1.XXX', 'e***@baz.com', '2']
    ]

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i} mismatch. Expected {expected}, got {actual}."