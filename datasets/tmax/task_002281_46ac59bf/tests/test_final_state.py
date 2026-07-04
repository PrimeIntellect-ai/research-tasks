# test_final_state.py
import os
import csv
from collections import defaultdict
import pytest

def normalize_lang(lang):
    """Normalize language string to ll-CC format."""
    parts = lang.replace('_', '-').split('-')
    if len(parts) == 2:
        return f"{parts[0].lower()}-{parts[1].upper()}"
    return lang

def compute_expected_data():
    """Derive the expected output data from the input files."""
    input_files = [
        "/home/user/inputs/batch1.csv",
        "/home/user/inputs/batch2.csv"
    ]

    records = []
    for inp in input_files:
        if not os.path.exists(inp):
            continue
        with open(inp, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(row)

    # Deduplicate: keep highest timestamp per (msg_id, normalized_lang)
    dedup = {}
    for r in records:
        msg_id = r['msg_id']
        lang = normalize_lang(r['lang'])
        key = (msg_id, lang)
        ts = int(r['timestamp'])
        score = int(r['score'])

        if key not in dedup or ts > dedup[key]['timestamp']:
            dedup[key] = {
                'msg_id': msg_id,
                'lang': lang,
                'timestamp': ts,
                'score': score
            }

    # Group by normalized lang
    by_lang = defaultdict(list)
    for key, val in dedup.items():
        by_lang[val['lang']].append(val)

    # Sort and compute rolling average
    expected_rows = []
    for lang in sorted(by_lang.keys()):
        lang_records = sorted(by_lang[lang], key=lambda x: x['timestamp'])
        scores = []
        for r in lang_records:
            scores.append(r['score'])
            window = scores[-3:]
            avg = sum(window) / len(window)
            expected_rows.append({
                'msg_id': r['msg_id'],
                'lang': r['lang'],
                'timestamp': str(r['timestamp']),
                'score': str(r['score']),
                'rolling_avg_score': f"{avg:.2f}"
            })

    return expected_rows

def test_output_file_exists():
    output_path = "/home/user/output/final_translations.csv"
    assert os.path.isfile(output_path), f"Expected output file {output_path} does not exist."

def test_output_file_contents():
    output_path = "/home/user/output/final_translations.csv"
    assert os.path.isfile(output_path), "Cannot check contents, output file is missing."

    expected_data = compute_expected_data()

    with open(output_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail("Output CSV is empty, expected a header and data rows.")

        expected_header = ['msg_id', 'lang', 'timestamp', 'score', 'rolling_avg_score']
        assert header == expected_header, f"CSV header mismatch. Expected {expected_header}, got {header}."

        actual_data = []
        for row in reader:
            if not row or not any(row):
                continue
            assert len(row) == 5, f"Row {row} does not have exactly 5 columns."
            actual_data.append({
                'msg_id': row[0],
                'lang': row[1],
                'timestamp': row[2],
                'score': row[3],
                'rolling_avg_score': row[4]
            })

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} rows, but got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."