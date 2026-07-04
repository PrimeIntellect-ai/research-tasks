# test_final_state.py

import os
import csv
import re
import collections
import pytest

def test_script_executable():
    script_path = '/home/user/process_locales.sh'
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_processed_output():
    input_path = '/home/user/locales_etl_dump.csv'
    output_path = '/home/user/fr_FR_rolling_stats.csv'

    assert os.path.exists(output_path), f"Output file {output_path} does not exist. Did the script run successfully?"

    # 1. Compute expected output from the input file
    records = {}
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 6:
                continue
            ts_str, sid, loc, src, tr, sc = row
            ts = int(ts_str)

            # Filter by locale
            if loc != 'fr-FR':
                continue

            # Filter out translations with 3+ consecutive uppercase letters
            if re.search(r'[A-Z]{3,}', tr):
                continue

            # Deduplicate by string_id keeping highest timestamp
            if sid not in records or records[sid]['ts'] < ts:
                records[sid] = {'ts': ts, 'sc': sc}

    # Sort chronologically
    sorted_recs = sorted(records.items(), key=lambda x: x[1]['ts'])

    # Impute and calculate rolling statistics
    last_score = 50.0
    window = collections.deque(maxlen=3)

    expected_rows = []
    for sid, data in sorted_recs:
        sc_str = data['sc']
        if sc_str == "":
            sc_val = last_score
        else:
            sc_val = float(sc_str)

        last_score = sc_val
        window.append(sc_val)

        rolling_avg = sum(window) / len(window)
        # We store the exact string representations expected
        expected_rows.append({
            'ts': data['ts'],
            'sid': sid,
            'sc': round(sc_val, 1),
            'avg': round(rolling_avg, 2)
        })

    # 2. Read student output and compare
    student_rows = []
    with open(output_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row: 
                continue
            assert len(row) == 4, f"Expected 4 columns in output CSV, got {len(row)} in row: {row}"
            ts, sid, sc, ra = row
            student_rows.append({
                'ts': int(ts),
                'sid': sid,
                'sc': float(sc),
                'avg': float(ra)
            })

    assert len(student_rows) == len(expected_rows), (
        f"Expected {len(expected_rows)} rows in the output, but got {len(student_rows)}. "
        "Check your filtering and deduplication logic."
    )

    for i, (exp, stu) in enumerate(zip(expected_rows, student_rows)):
        assert exp['ts'] == stu['ts'], f"Row {i+1}: Expected timestamp {exp['ts']}, got {stu['ts']}. Sort order or deduplication may be incorrect."
        assert exp['sid'] == stu['sid'], f"Row {i+1}: Expected string_id {exp['sid']}, got {stu['sid']}."

        # Compare floats with a small tolerance
        assert abs(exp['sc'] - stu['sc']) < 1e-5, (
            f"Row {i+1} (string_id {exp['sid']}): Expected confidence_score {exp['sc']}, got {stu['sc']}. "
            "Check your imputation logic."
        )

        assert abs(exp['avg'] - stu['avg']) < 1e-2 + 1e-5, (
            f"Row {i+1} (string_id {exp['sid']}): Expected rolling_avg {exp['avg']}, got {stu['avg']}. "
            "Check your rolling average calculation."
        )