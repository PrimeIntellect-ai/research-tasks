# test_final_state.py

import os
import json
import pytest

OUTPUT_JSON_PATH = "/home/user/output.json"
RUST_PROJECT_DIR = "/home/user/graph_pipeline"

def test_rust_project_exists():
    """Verify that the Rust project directory exists."""
    assert os.path.isdir(RUST_PROJECT_DIR), f"Rust project directory {RUST_PROJECT_DIR} does not exist."
    cargo_toml = os.path.join(RUST_PROJECT_DIR, "Cargo.toml")
    assert os.path.isfile(cargo_toml), f"Cargo.toml not found in {RUST_PROJECT_DIR}."
    src_dir = os.path.join(RUST_PROJECT_DIR, "src")
    assert os.path.isdir(src_dir), f"src directory not found in {RUST_PROJECT_DIR}."

def test_output_json_exists():
    """Verify that the output JSON file was created."""
    assert os.path.isfile(OUTPUT_JSON_PATH), f"Output file {OUTPUT_JSON_PATH} does not exist."

def test_output_json_content():
    """Verify the contents of the output JSON file."""
    with open(OUTPUT_JSON_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_JSON_PATH} is not valid JSON.")

    assert "reachable_nodes" in data, "JSON output is missing the 'reachable_nodes' key."

    reachable = data["reachable_nodes"]
    assert isinstance(reachable, list), "'reachable_nodes' must be a list."

    # Based on the graph logic:
    # N001 -> N003 (N001->N002 is deleted)
    # N003 -> N004 (N003->N005 is deleted)
    # 1 hop: N003
    # 2 hops: N004
    expected = ["N003", "N004"]

    assert reachable == expected, f"Expected reachable_nodes to be {expected}, but got {reachable}."