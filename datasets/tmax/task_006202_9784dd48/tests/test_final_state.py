# test_final_state.py
import os
import json
import pytest

def test_parser_c_exists_and_uses_mmap():
    parser_path = '/home/user/parser.c'
    assert os.path.isfile(parser_path), f"C parser file {parser_path} is missing."
    with open(parser_path, 'r', encoding='utf-8') as f:
        content = f.read()
    assert 'mmap' in content, "The C parser must use memory-mapped I/O (mmap)."

def test_valid_files_moved():
    expected_files = [
        ('/home/user/organized_project/PROJ-A/2021-01/alpha.bin', "alpha.bin"),
        ('/home/user/organized_project/PROJ-B/2021-07/beta.bin', "beta.bin"),
        ('/home/user/organized_project/PROJ-A/2022-01/gamma.bin', "gamma.bin"),
    ]
    for full_path, fname in expected_files:
        assert os.path.isfile(full_path), f"Valid file {fname} was not moved to the correct destination: {full_path}"

def test_invalid_files_remain():
    invalid_files = [
        '/home/user/raw_data/invalid/bad_magic.bin',
        '/home/user/raw_data/invalid/too_short.bin'
    ]
    for full_path in invalid_files:
        assert os.path.isfile(full_path), f"Invalid file {full_path} should remain in its original location."

def test_no_valid_files_in_raw_data():
    raw_data_dir = '/home/user/raw_data'
    valid_filenames = {'alpha.bin', 'beta.bin', 'gamma.bin'}
    found_valid_files = []
    for root, _, files in os.walk(raw_data_dir):
        for file in files:
            if file in valid_filenames:
                found_valid_files.append(os.path.join(root, file))
    assert not found_valid_files, f"Valid files should not remain in raw_data: {found_valid_files}"

def test_parsed_metrics_jsonl():
    jsonl_path = '/home/user/parsed_metrics.jsonl'
    assert os.path.isfile(jsonl_path), f"Parsed metrics file {jsonl_path} is missing."

    expected_records = {
        "alpha.bin": {"file": "alpha.bin", "timestamp": 1609459200, "project": "PROJ-A", "metric": 123.4567},
        "beta.bin": {"file": "beta.bin", "timestamp": 1625097600, "project": "PROJ-B", "metric": 987.6543},
        "gamma.bin": {"file": "gamma.bin", "timestamp": 1640995200, "project": "PROJ-A", "metric": 11.1111},
    }

    parsed_records = {}
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                parsed_records[record.get('file')] = record
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON found in {jsonl_path}: {line}")

    assert len(parsed_records) == len(expected_records), f"Expected {len(expected_records)} records, found {len(parsed_records)}."

    for fname, expected in expected_records.items():
        assert fname in parsed_records, f"Record for {fname} is missing in {jsonl_path}."
        actual = parsed_records[fname]
        assert actual.get('timestamp') == expected['timestamp'], f"Incorrect timestamp for {fname}."
        assert actual.get('project') == expected['project'], f"Incorrect project for {fname}."
        assert abs(actual.get('metric', 0) - expected['metric']) < 1e-4, f"Incorrect metric value for {fname}."