# test_final_state.py
import os
import re
import csv
from datetime import datetime, timedelta

def tokenize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]', ' ', text)
    tokens = set(text.split())
    return tokens

def calculate_jaccard(set1, set2):
    if not set1 and not set2:
        return 1.0
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union

def test_drift_report():
    baseline_path = "/home/user/baseline.txt"
    changes_path = "/home/user/changes.log"
    report_path = "/home/user/drift_report.csv"

    assert os.path.isfile(baseline_path), f"File not found: {baseline_path}"
    assert os.path.isfile(changes_path), f"File not found: {changes_path}"
    assert os.path.isfile(report_path), f"File not found: {report_path}"

    with open(baseline_path, "r") as f:
        baseline_text = f.read()
    baseline_tokens = tokenize(baseline_text)

    expected_rows = []
    last_dt = None

    with open(changes_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(" | ", 1)
            if len(parts) != 2:
                continue
            ts_str, config_text = parts

            if ts_str == "MISSING":
                assert last_dt is not None, "First line cannot have MISSING timestamp"
                current_dt = last_dt + timedelta(minutes=5)
            else:
                current_dt = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ")

            last_dt = current_dt
            formatted_ts = current_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

            config_tokens = tokenize(config_text)
            score = calculate_jaccard(baseline_tokens, config_tokens)
            expected_rows.append((formatted_ts, f"{score:.4f}"))

    actual_rows = []
    with open(report_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                actual_rows.append(tuple(row))

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in CSV, found {len(actual_rows)}"

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch: expected {expected}, got {actual}"