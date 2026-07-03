# test_final_state.py

import os
import json
import importlib.util
import pytest

def test_pyproject_toml_fixed():
    path = "/home/user/fastparser_ext/pyproject.toml"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "setuptools-rust" in content, (
        f"The build-system requires in {path} does not seem to include 'setuptools-rust'."
    )

def test_test_api_script_exists():
    path = "/home/user/test_api.py"
    assert os.path.isfile(path), f"File {path} does not exist. You were supposed to write a script here."

def test_parsed_output_json():
    path = "/home/user/parsed_output.json"
    assert os.path.isfile(path), f"File {path} does not exist. Did your script run and create it?"

    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    expected = ["INIT_CONN", "FETCH_RECORDS", "UPDATE_STATE", "TERMINATE"]
    assert data == expected, (
        f"The parsed output in {path} is incorrect.\n"
        f"Expected: {expected}\n"
        f"Got: {data}"
    )

def test_fastparser_installed():
    # Check if fastparser can be imported
    spec = importlib.util.find_spec("fastparser")
    assert spec is not None, "The 'fastparser' module is not installed in the Python environment."