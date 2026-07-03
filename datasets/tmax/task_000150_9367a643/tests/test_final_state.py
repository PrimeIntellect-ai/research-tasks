# test_final_state.py

import os
import json
import pytest

def test_find_fraud_script_exists_and_executable():
    script_path = "/home/user/find_fraud.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_venv_and_kuzu_db_exist():
    venv_path = "/home/user/venv"
    kuzu_db_path = "/home/user/kuzu_db"

    assert os.path.isdir(venv_path), f"The virtual environment directory {venv_path} was not created."
    assert os.path.isdir(kuzu_db_path), f"The Kuzu database directory {kuzu_db_path} was not created."

def test_suspects_json_content():
    json_path = "/home/user/suspects.json"
    assert os.path.isfile(json_path), f"The output file {json_path} does not exist."

    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {json_path} does not contain valid JSON.")

    assert isinstance(data, list), f"The content of {json_path} should be a JSON array (list)."

    expected_suspects = [
        "Frank White",
        "Grace Hall",
        "Harry King",
        "Jack Black"
    ]

    assert data == expected_suspects, f"The suspects list in {json_path} does not match the expected output. Got: {data}"