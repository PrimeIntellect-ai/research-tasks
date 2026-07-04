# test_final_state.py
import os
import json
import csv
import pytest

def test_clean_translations_jsonl_exists():
    path = "/home/user/loc_pipeline/clean_translations.jsonl"
    assert os.path.isfile(path), f"Output file {path} is missing."

def test_rolling_stats_csv_exists():
    path = "/home/user/loc_pipeline/rolling_stats.csv"
    assert os.path.isfile(path), f"Output file {path} is missing."

def test_clean_translations_content():
    path = "/home/user/loc_pipeline/clean_translations.jsonl"
    records = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            records.append(json.loads(line))

    # Check deduplication, sorting, and cleaning logic
    expected_ids = ["btn_ok", "btn_cancel", "msg_error", "msg_error", "lbl_save", "msg_warn", "btn_ok", "msg_info", "msg_success"]
    expected_langs = ["en", "en", "en", "fr", "en", "fr", "fr", "fr", "fr"]
    expected_timestamps = [105, 110, 120, 140, 160, 170, 180, 190, 200]
    expected_texts = ["Okay", "Cancel", "Error \ufffd", "Erreur", "Save", "Attention\ufffd", "D\u00e9ccord!", "Info", "Succ\u00e8s"]

    assert len(records) == 9, f"Expected 9 records in clean_translations.jsonl, found {len(records)}"

    for i, record in enumerate(records):
        assert record["id"] == expected_ids[i], f"Record {i} id mismatch: expected {expected_ids[i]}, got {record['id']}"
        assert record["lang"] == expected_langs[i], f"Record {i} lang mismatch: expected {expected_langs[i]}, got {record['lang']}"
        assert record["timestamp"] == expected_timestamps[i], f"Record {i} timestamp mismatch: expected {expected_timestamps[i]}, got {record['timestamp']}"
        assert record["text"] == expected_texts[i], f"Record {i} text mismatch: expected {expected_texts[i]}, got {record['text']}"

def test_rolling_stats_csv_content():
    path = "/home/user/loc_pipeline/rolling_stats.csv"
    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            rows.append(row)

    expected_header = ["timestamp", "lang", "id", "text_length", "rolling_avg_len"]
    assert header == expected_header, f"CSV header mismatch: expected {expected_header}, got {header}"

    expected_rows = [
        ["105", "en", "btn_ok", "4", "4.00"],
        ["110", "en", "btn_cancel", "6", "5.00"],
        ["120", "en", "msg_error", "7", "5.67"],
        ["140", "fr", "msg_error", "6", "6.00"],
        ["160", "en", "lbl_save", "4", "5.67"],
        ["170", "fr", "msg_warn", "10", "8.00"],
        ["180", "fr", "btn_ok", "8", "8.00"],
        ["190", "fr", "msg_info", "4", "7.33"],
        ["200", "fr", "msg_success", "6", "6.00"]
    ]

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in CSV, found {len(rows)}"

    for i, (row, expected) in enumerate(zip(rows, expected_rows)):
        assert row[0] == expected[0], f"Row {i} timestamp mismatch"
        assert row[1] == expected[1], f"Row {i} lang mismatch"
        assert row[2] == expected[2], f"Row {i} id mismatch"
        assert row[3] == expected[3], f"Row {i} text_length mismatch"
        # Handle 4.0 vs 4.00
        assert float(row[4]) == float(expected[4]), f"Row {i} rolling_avg_len mismatch: expected {expected[4]}, got {row[4]}"