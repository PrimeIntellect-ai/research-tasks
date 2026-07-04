# test_final_state.py

import os
import re
import pytest

def test_violations_txt_correct():
    violations_path = "/home/user/violations.txt"
    assert os.path.isfile(violations_path), f"The file {violations_path} does not exist."

    with open(violations_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_violators = ["EMP_01", "EMP_05"]
    assert lines == expected_violators, f"Expected {expected_violators} in {violations_path}, but got {lines}."

def test_cypher_query_exists_and_looks_valid():
    query_path = "/home/user/query.cypher"
    assert os.path.isfile(query_path), f"The file {query_path} does not exist."

    with open(query_path, 'r') as f:
        query = f.read().upper()

    assert "MATCH" in query, "The Cypher query must contain a MATCH clause."
    assert "MANAGES" in query, "The Cypher query must reference the MANAGES relationship."
    assert "HAS_ACCESS" in query, "The Cypher query must reference the HAS_ACCESS relationship."
    assert "*" in query, "The Cypher query must use variable-length paths (e.g., [:MANAGES*0..]) for transitive management."

def test_rust_project_exists():
    cargo_toml = "/home/user/auditor/Cargo.toml"
    main_rs = "/home/user/auditor/src/main.rs"

    assert os.path.isfile(cargo_toml), f"Rust project file {cargo_toml} does not exist."
    assert os.path.isfile(main_rs), f"Rust source file {main_rs} does not exist."