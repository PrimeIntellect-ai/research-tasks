# test_final_state.py

import os
import json
import csv
import pytest

PROJECT_DIR = "/home/user/l10n_processor"
INPUT_JSON = os.path.join(PROJECT_DIR, "input.json")
OUTPUT_CSV = os.path.join(PROJECT_DIR, "output.csv")

def test_output_csv_exists():
    assert os.path.isfile(OUTPUT_CSV), f"Output file missing: {OUTPUT_CSV}"

def test_output_csv_content():
    # Read the input data
    assert os.path.isfile(INPUT_JSON), f"Input file missing: {INPUT_JSON}"
    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Filter out empty text or text with U+FFFD
    filtered = []
    for row in data:
        text = row.get("text", "")
        if text == "" or "\ufffd" in text:
            continue
        filtered.append(row)

    # 2. Resolve duplicates (keep highest timestamp)
    dedup = {}
    for row in filtered:
        k = (row["key"], row["lang"])
        if k not in dedup or row["timestamp"] > dedup[k]["timestamp"]:
            dedup[k] = row

    # 3. Sort by key ascending, then lang ascending
    sorted_records = sorted(dedup.values(), key=lambda x: (x["key"], x["lang"]))

    # 4. Format as CSV
    expected_rows = [["key", "lang", "text"]]
    for row in sorted_records:
        expected_rows.append([row["key"], row["lang"], row["text"]])

    # Read the actual output
    actual_rows = []
    with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            actual_rows.append(row)

    # Assert
    assert actual_rows == expected_rows, (
        "The generated CSV does not match the expected output. "
        "Ensure you correctly filtered empty/corrupted records, deduplicated by highest timestamp, "
        "and sorted by key then lang."
    )