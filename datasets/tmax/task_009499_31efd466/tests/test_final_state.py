# test_final_state.py
import os
import json
import base64
import csv
import pytest

def test_processed_metrics_csv():
    raw_file = "/home/user/raw_translations.jsonl"
    csv_file = "/home/user/processed_metrics.csv"

    assert os.path.exists(csv_file), f"Output file {csv_file} does not exist."

    seen_tx = set()
    windows = {}
    expected_rows = []

    # Derive the expected state from the raw input file
    with open(raw_file, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            tx_id = record['tx_id']

            # Deduplication
            if tx_id in seen_tx:
                continue
            seen_tx.add(tx_id)

            lang = record['lang']
            charset = record['charset']

            # Map charset to Python's encoding names if necessary
            py_charset = charset
            if py_charset.lower() == "windows-1252":
                py_charset = "cp1252"

            raw_bytes = base64.b64decode(record['payload_b64'])
            text = raw_bytes.decode(py_charset)
            char_count = len(text)

            if lang not in windows:
                windows[lang] = []

            windows[lang].append(char_count)
            if len(windows[lang]) > 3:
                windows[lang].pop(0)

            avg = sum(windows[lang]) / len(windows[lang])
            expected_rows.append([str(tx_id), lang, f"{avg:.1f}"])

    # Read the actual output produced by the student
    actual_rows = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["tx_id", "lang", "avg_char_count"], f"Incorrect CSV header: {header}"

        for row in reader:
            if row:
                actual_rows.append(row)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} data rows, got {len(actual_rows)}"

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch: expected {expected}, got {actual}"