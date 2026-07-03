# test_final_state.py

import os
import gzip
import pytest

def test_vendored_package_parser_go_fixed():
    parser_go_path = "/app/vendor/github.com/buger/jsonparser/parser.go"
    assert os.path.isfile(parser_go_path), f"File not found: {parser_go_path}"

    with open(parser_go_path, "r") as f:
        content = f.read()
    assert "math/rand/v2" not in content, f"Expected corrupted import 'math/rand/v2' to be removed from {parser_go_path}"
    assert "math/rand" in content, f"Expected correct import 'math/rand' in {parser_go_path}"

def test_bytesafe_module_fixed():
    bytesafe_path = "/app/vendor/github.com/buger/jsonparser/bytesafe"
    assert os.path.exists(bytesafe_path), f"Expected bytesafe module to be accessible at {bytesafe_path}"
    assert os.path.isdir(bytesafe_path), f"Expected {bytesafe_path} to be a directory (or symlink to a directory)"

def test_dataparser_compiled():
    binary_path = "/home/user/workspace/dataparser/dataparser"
    assert os.path.isfile(binary_path), f"Expected compiled binary at {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Expected {binary_path} to be executable"

def test_output_file_and_metric():
    symlink_path = "/home/user/latest.csv.gz"
    target_path = "/home/user/organized_datasets/latest_readings.csv.gz"

    assert os.path.islink(symlink_path), f"Symlink not created at {symlink_path}"
    assert os.path.isfile(target_path), f"Target file not found at {target_path}"

    real_path = os.path.realpath(symlink_path)
    assert os.path.realpath(target_path) == real_path, "Symlink does not point to the expected target"

    size = os.path.getsize(real_path)

    # Verify valid gzip and row count roughly matches expectation (e.g., 5000 rows)
    try:
        with gzip.open(real_path, 'rt') as f:
            lines = f.readlines()
    except Exception as e:
        pytest.fail(f"Failed to read {real_path} as gzip: {e}")

    assert len(lines) > 4500, f"Not enough data parsed. Expected > 4500 rows, found {len(lines)}"

    # The threshold test
    assert size <= 25000, f"File size {size} exceeds threshold of 25000 bytes. Ensure debug lines were stripped and gzip compression was used."