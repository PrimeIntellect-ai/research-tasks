# test_final_state.py

import os
import pytest

def test_tx_analyzer_project_exists():
    dir_path = "/home/user/tx_analyzer"
    assert os.path.exists(dir_path), f"The directory {dir_path} is missing. Did you initialize the Rust project?"
    assert os.path.isdir(dir_path), f"The path {dir_path} is not a directory."

    cargo_toml_path = os.path.join(dir_path, "Cargo.toml")
    assert os.path.exists(cargo_toml_path), f"Cargo.toml is missing in {dir_path}. Is it a valid Rust project?"

def test_resolution_txt_content():
    file_path = "/home/user/resolution.txt"
    assert os.path.exists(file_path), f"The file {file_path} is missing. Did you generate the output log?"
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

    expected_content = """Deadlock: TX_003, TX_005
Safe_TX_003_Step1: MATCH (n:User {uid: 512}) SET n.status = 'updated'
Safe_TX_003_Step2: MATCH (n:User {uid: 882}) SET n.status = 'updated'
Safe_TX_005_Step1: MATCH (n:User {uid: 512}) SET n.status = 'updated'
Safe_TX_005_Step2: MATCH (n:User {uid: 882}) SET n.status = 'updated'"""

    with open(file_path, "r") as f:
        actual_content = f.read().strip()

    # We compare line by line to provide a clear error message
    actual_lines = [line.strip() for line in actual_content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {file_path}, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in {file_path} does not match.\nExpected: {expected}\nActual:   {actual}"