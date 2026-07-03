# test_final_state.py

import os
import json
import csv
import pytest

def test_es_json_updated():
    es_path = "/home/user/locales/es.json"
    assert os.path.isfile(es_path), f"File {es_path} does not exist."
    with open(es_path, 'r') as f:
        data = json.load(f)

    expected = {
        "bye": "goodbye",
        "hello": "hola",
        "help": "help me",
        "thanks": "thank you",
        "welcome": "bienvenido"
    }
    assert data == expected, f"Content of {es_path} does not match expected final state."

def test_fr_json_updated():
    fr_path = "/home/user/locales/fr.json"
    assert os.path.isfile(fr_path), f"File {fr_path} does not exist."
    with open(fr_path, 'r') as f:
        data = json.load(f)

    expected = {
        "bye": "goodbye",
        "hello": "bonjour",
        "help": "help me"
    }
    assert data == expected, f"Content of {fr_path} does not match expected final state."

def test_hourly_summary_csv():
    csv_path = "/home/user/hourly_summary.csv"
    assert os.path.isfile(csv_path), f"File {csv_path} does not exist."

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    expected_rows = [
        ['locale', 'hour_bucket', 'count'],
        ['es', '2023-10-05 09:00', '2'],
        ['es', '2023-10-05 10:00', '2'],
        ['fr', '2023-10-05 09:00', '1'],
        ['fr', '2023-10-05 10:00', '1']
    ]

    assert rows == expected_rows, f"Content of {csv_path} does not match expected final state."

def test_pipeline_log():
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert "Updated locale: es" in lines, "pipeline.log is missing 'Updated locale: es'"
    assert "Updated locale: fr" in lines, "pipeline.log is missing 'Updated locale: fr'"