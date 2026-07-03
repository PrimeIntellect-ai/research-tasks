# test_final_state.py

import os
import json
import pytest

def test_output_directory_exists():
    assert os.path.isdir('/home/user/output'), "The output directory /home/user/output does not exist."

def test_distances_json_exists_and_valid():
    json_path = '/home/user/output/distances.json'
    assert os.path.isfile(json_path), f"The file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} is not valid JSON.")

    assert isinstance(data, list), "The JSON output must be an array."
    if len(data) > 0:
        item = data[0]
        assert "sensor_a" in item, "Missing 'sensor_a' in JSON output."
        assert "sensor_b" in item, "Missing 'sensor_b' in JSON output."
        assert "jsd" in item, "Missing 'jsd' in JSON output."

def test_best_pair_txt():
    txt_path = '/home/user/output/best_pair.txt'
    assert os.path.isfile(txt_path), f"The file {txt_path} does not exist."

    with open(txt_path, 'r') as f:
        content = f.read().strip()

    assert content == "S1,S2", f"Expected 'S1,S2' in {txt_path}, but got '{content}'."

def test_rust_project_structure_and_rayon():
    cargo_toml_path = '/home/user/rust_dist/Cargo.toml'
    main_rs_path = '/home/user/rust_dist/src/main.rs'

    assert os.path.isfile(cargo_toml_path), f"The file {cargo_toml_path} does not exist."
    assert os.path.isfile(main_rs_path), f"The file {main_rs_path} does not exist."

    with open(cargo_toml_path, 'r') as f:
        cargo_content = f.read()
        assert "rayon" in cargo_content, "The 'rayon' crate is missing from Cargo.toml."

    with open(main_rs_path, 'r') as f:
        main_content = f.read()
        assert "par_iter" in main_content or "par_bridge" in main_content or "rayon::" in main_content, \
            "Could not find evidence of rayon parallelism (e.g., par_iter) in main.rs."

def test_workflow_notebook_exists_and_valid():
    ipynb_path = '/home/user/workflow.ipynb'
    assert os.path.isfile(ipynb_path), f"The file {ipynb_path} does not exist."

    with open(ipynb_path, 'r') as f:
        try:
            notebook = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {ipynb_path} is not valid JSON (Jupyter notebook).")

    assert "cells" in notebook, "The notebook does not have a 'cells' property."

    cells_source = []
    for cell in notebook.get("cells", []):
        source = cell.get("source", [])
        if isinstance(source, list):
            cells_source.extend(source)
        else:
            cells_source.append(source)

    full_source = "".join(cells_source)
    assert "cargo build --release" in full_source or "!cargo build --release" in full_source, \
        "The notebook does not contain a command to compile the Rust project in release mode."
    assert "distances.json" in full_source, "The notebook does not contain code to read distances.json."