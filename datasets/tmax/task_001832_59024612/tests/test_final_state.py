# test_final_state.py

import os
import json
import csv
from collections import defaultdict

def test_top_missing_csv_exists_and_correct():
    """Test that the CSV output exists, has the correct headers, and contains the correct aggregated data."""
    csv_path = "/home/user/top_missing.csv"
    assert os.path.exists(csv_path), f"Expected output file {csv_path} does not exist."
    assert os.path.isfile(csv_path), f"{csv_path} is not a file."

    jsonl_path = "/home/user/loc_errors.jsonl"
    assert os.path.exists(jsonl_path), f"Input file {jsonl_path} is missing."

    # Recompute the expected results from the input file
    windows = defaultdict(lambda: defaultdict(int))
    with open(jsonl_path, "r") as f:
        for line in f:
            if not line.strip(): 
                continue
            data = json.loads(line)
            ts = data.get("timestamp")
            if not ts:
                continue

            # Truncate timestamp to the hour to get the 1-hour tumbling window
            # e.g., "2023-10-15T14:23:01Z" -> "2023-10-15T14:00:00Z"
            window_start = ts[:14] + "00:00Z"
            key = data.get("key")
            locale = data.get("locale")
            windows[window_start][(locale, key)] += 1

    expected_rows = []
    for w_start in sorted(windows.keys()):
        counts = windows[w_start]
        # Sort by count descending, then locale ascending, then key ascending
        sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0][0], x[0][1]))
        best_loc_key, best_count = sorted_counts[0]
        expected_rows.append({
            "window_start": w_start,
            "locale": best_loc_key[0],
            "key": best_loc_key[1],
            "error_count": str(best_count)
        })

    # Read the actual output
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        actual_rows = list(reader)
        actual_fieldnames = reader.fieldnames

    expected_headers = ["window_start", "locale", "key", "error_count"]
    assert actual_fieldnames == expected_headers, \
        f"CSV headers do not match. Expected {expected_headers}, got {actual_fieldnames}"

    assert len(actual_rows) == len(expected_rows), \
        f"Expected {len(expected_rows)} rows in CSV, but got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual["window_start"] == expected["window_start"], \
            f"Row {i+1} window_start mismatch: expected {expected['window_start']}, got {actual['window_start']}"
        assert actual["locale"] == expected["locale"], \
            f"Row {i+1} locale mismatch: expected {expected['locale']}, got {actual['locale']}"
        assert actual["key"] == expected["key"], \
            f"Row {i+1} key mismatch: expected {expected['key']}, got {actual['key']}"
        assert str(actual["error_count"]) == expected["error_count"], \
            f"Row {i+1} error_count mismatch: expected {expected['error_count']}, got {actual['error_count']}"