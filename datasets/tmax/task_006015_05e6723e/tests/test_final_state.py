# test_final_state.py

import os
import json

def test_pipeline_script_exists():
    """Check if the pipeline script exists."""
    path = "/home/user/pipeline.sh"
    assert os.path.isfile(path), f"File {path} does not exist."

def test_clean_l10n_jsonl_exists():
    """Check if the output JSONL file exists."""
    path = "/home/user/clean_l10n.jsonl"
    assert os.path.isfile(path), f"File {path} does not exist."

def test_clean_l10n_jsonl_content():
    """Validate the contents, formatting, and sorting of the output JSONL file."""
    path = "/home/user/clean_l10n.jsonl"
    assert os.path.isfile(path), f"File {path} does not exist."

    expected = [
        {"timestamp": 1670000001, "locale": "fr_FR", "msg_id": "bye", "translation": "Au revoir"},
        {"timestamp": 1670000002, "locale": "de_DE", "msg_id": "error", "translation": "Fehler aufgetreten bitte warten"},
        {"timestamp": 1670000005, "locale": "es_ES", "msg_id": "welcome", "translation": "Hola Mundo"},
        {"timestamp": 1670000010, "locale": "en_US", "msg_id": "info", "translation": "Update successful"}
    ]

    actual = []
    with open(path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                actual.append(obj)
            except json.JSONDecodeError as e:
                assert False, f"Line {line_num} in {path} is not valid JSON: {e}"

    assert len(actual) == len(expected), f"Expected {len(expected)} records in {path}, got {len(actual)}."

    for i, (act, exp) in enumerate(zip(actual, expected)):
        assert act == exp, f"Mismatch at line {i+1} in {path}:\nExpected: {exp}\nActual: {act}"