# test_final_state.py

import os
import json
import pytest

def test_run_pipeline_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_fr_fr_errors_log():
    log_path = "/home/user/errors_fr_FR.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."
    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read().strip().splitlines()
    assert "bad_placeholder" in content, f"Expected 'bad_placeholder' in {log_path}."
    assert len(content) == 1, f"Expected exactly 1 error in {log_path}, got {len(content)}."

def test_es_es_errors_log():
    log_path = "/home/user/errors_es_ES.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."
    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read().strip().splitlines()
    assert "count" in content, f"Expected 'count' in {log_path}."
    assert len(content) == 1, f"Expected exactly 1 error in {log_path}, got {len(content)}."

def test_fr_fr_output_json():
    json_path = "/home/user/output_fr_FR.json"
    assert os.path.isfile(json_path), f"{json_path} does not exist."
    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} contains invalid JSON.")

    expected = {
        "welcome": len("Bienvenue, %s!".encode('utf-8')),
        "multiline": len("Ligne 1\nLigne 2".encode('utf-8')),
        "count": len("Vous avez %d articles".encode('utf-8'))
    }
    assert data == expected, f"Content of {json_path} does not match expected byte lengths."

def test_es_es_output_json():
    json_path = "/home/user/output_es_ES.json"
    assert os.path.isfile(json_path), f"{json_path} does not exist."
    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} contains invalid JSON.")

    expected = {
        "welcome": len("¡Bienvenido, %s!".encode('utf-8')),
        "multiline": len("Línea 1\nLínea 2".encode('utf-8')),
        "bad_placeholder": len("Puntuación: %f".encode('utf-8'))
    }
    assert data == expected, f"Content of {json_path} does not match expected byte lengths."