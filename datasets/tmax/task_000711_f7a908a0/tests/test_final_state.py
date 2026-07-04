# test_final_state.py

import os
import json
import csv
from collections import defaultdict

def test_high_priority_missing_csv():
    output_path = "/home/user/high_priority_missing.csv"
    telemetry_path = "/home/user/telemetry.jsonl"
    metadata_path = "/home/user/string_metadata.csv"

    assert os.path.exists(output_path), f"Output file missing: {output_path}"
    assert os.path.exists(telemetry_path), f"Telemetry file missing: {telemetry_path}"
    assert os.path.exists(metadata_path), f"Metadata file missing: {metadata_path}"

    # 1. Read metadata and filter high priority strings
    high_priority_meta = {}
    with open(metadata_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['priority'] == 'high':
                high_priority_meta[row['string_id']] = row['module']

    # 2. Read telemetry and aggregate
    counts = defaultdict(int)
    with open(telemetry_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            string_id = record.get('string_id')
            if string_id in high_priority_meta:
                hour = record['timestamp'][:13]
                lang = record['lang']
                module = high_priority_meta[string_id]
                counts[(hour, lang, string_id, module)] += 1

    # 3. Sort the expected data
    expected_rows = []
    for (hour, lang, string_id, module), count in counts.items():
        expected_rows.append({
            'hour': hour,
            'lang': lang,
            'string_id': string_id,
            'module': module,
            'missing_count': count
        })

    # Sort by hour (asc), missing_count (desc), string_id (asc)
    expected_rows.sort(key=lambda x: (x['hour'], -x['missing_count'], x['string_id']))

    # 4. Read the actual output
    actual_rows = []
    with open(output_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            assert False, "Output CSV is empty"

        expected_header = ['hour', 'lang', 'string_id', 'module', 'missing_count']
        assert header == expected_header, f"Header mismatch. Expected {expected_header}, got {header}"

        for row in reader:
            if not row:
                continue
            assert len(row) == 5, f"Row has incorrect number of columns: {row}"
            actual_rows.append({
                'hour': row[0],
                'lang': row[1],
                'string_id': row[2],
                'module': row[3],
                'missing_count': int(row[4])
            })

    # 5. Compare
    assert len(actual_rows) == len(expected_rows), f"Row count mismatch. Expected {len(expected_rows)}, got {len(actual_rows)}"

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}"