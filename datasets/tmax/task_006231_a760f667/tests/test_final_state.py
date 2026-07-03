# test_final_state.py

import os
import json
import pytest

def test_vulnerable_dbs_json():
    json_path = "/home/user/vulnerable_dbs.json"
    assert os.path.isfile(json_path), f"Expected JSON output file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert isinstance(data, list), f"Expected JSON array in {json_path}, but got {type(data).__name__}."
    assert data == ["db3", "db4"], f"Expected ['db3', 'db4'] in {json_path}, but got {data}."

def test_query_plan_txt():
    txt_path = "/home/user/query_plan.txt"
    assert os.path.isfile(txt_path), f"Expected query plan file {txt_path} does not exist."

    with open(txt_path, 'r') as f:
        content = f.read().strip()

    assert len(content) > 0, f"File {txt_path} is empty. It should contain the EXPLAIN output."

def test_kuzu_db_dir():
    db_dir = "/home/user/kuzu_db"
    assert os.path.isdir(db_dir), f"Expected KuzuDB directory {db_dir} does not exist."

def test_rust_project_exists():
    cargo_toml = "/home/user/backup_auditor/Cargo.toml"
    assert os.path.isfile(cargo_toml), f"Expected Rust project file {cargo_toml} does not exist."