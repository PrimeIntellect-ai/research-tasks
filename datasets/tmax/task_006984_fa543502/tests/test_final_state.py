# test_final_state.py

import os
import json
import pytest

def test_processed_files_exist():
    """Test that the expected processed files exist."""
    assert os.path.isdir("/home/user/processed"), "The /home/user/processed directory was not created."
    assert os.path.isfile("/home/user/processed/es-ES.jsonl"), "The es-ES.jsonl file is missing."
    assert os.path.isfile("/home/user/processed/fr-FR.jsonl"), "The fr-FR.jsonl file is missing."
    assert os.path.isfile("/home/user/es-ES_rolling_avg.txt"), "The es-ES_rolling_avg.txt file is missing."

def test_es_es_processed_content():
    """Test that the es-ES.jsonl file contains the correct deduplicated, normalized, and sorted entries."""
    expected_es_es = [
        {"timestamp": 1600000002, "string_id": "txt_desc", "locale": "es-ES", "text": "A é B"},
        {"timestamp": 1600000003, "string_id": "btn_cancel", "locale": "es-ES", "text": "X"},
        {"timestamp": 1600000004, "string_id": "btn_greet", "locale": "es-ES", "text": "Hol á"},
        {"timestamp": 1600000006, "string_id": "btn_help", "locale": "es-ES", "text": "¡Ojo!"}
    ]

    file_path = "/home/user/processed/es-ES.jsonl"
    if not os.path.exists(file_path):
        pytest.fail(f"File {file_path} does not exist.")

    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_es_es), f"Expected {len(expected_es_es)} lines in es-ES.jsonl, got {len(lines)}."

    for i, line in enumerate(lines):
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in es-ES.jsonl is not valid JSON: {line}")

        assert parsed == expected_es_es[i], f"Mismatch at line {i+1} in es-ES.jsonl.\nExpected: {expected_es_es[i]}\nGot: {parsed}"

def test_fr_fr_processed_content():
    """Test that the fr-FR.jsonl file contains the correct deduplicated, normalized, and sorted entries."""
    expected_fr_fr = [
        {"timestamp": 1600000001, "string_id": "btn_greet", "locale": "fr-FR", "text": "Oui ça"}
    ]

    file_path = "/home/user/processed/fr-FR.jsonl"
    if not os.path.exists(file_path):
        pytest.fail(f"File {file_path} does not exist.")

    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_fr_fr), f"Expected {len(expected_fr_fr)} lines in fr-FR.jsonl, got {len(lines)}."

    for i, line in enumerate(lines):
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in fr-FR.jsonl is not valid JSON: {line}")

        assert parsed == expected_fr_fr[i], f"Mismatch at line {i+1} in fr-FR.jsonl.\nExpected: {expected_fr_fr[i]}\nGot: {parsed}"

def test_rolling_average():
    """Test that the rolling average file contains the correct calculations."""
    expected_averages = ["5.0", "3.0", "3.7", "3.7"]

    file_path = "/home/user/es-ES_rolling_avg.txt"
    if not os.path.exists(file_path):
        pytest.fail(f"File {file_path} does not exist.")

    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_averages), f"Expected {len(expected_averages)} lines in es-ES_rolling_avg.txt, got {len(lines)}."

    for i, (expected, actual) in enumerate(zip(expected_averages, lines)):
        assert actual == expected, f"Mismatch at line {i+1} in es-ES_rolling_avg.txt. Expected {expected}, got {actual}."