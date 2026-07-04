# test_final_state.py

import os
import json
import re
import math
from collections import defaultdict

def test_error_log_exists_and_correct():
    raw_logs_path = "/home/user/loc_data/raw_logs.txt"
    error_log_path = "/home/user/loc_data/error.log"

    assert os.path.exists(raw_logs_path), f"Input file {raw_logs_path} missing."
    assert os.path.exists(error_log_path), f"Error log {error_log_path} was not created."

    pattern = re.compile(r"^\[(.*?)\] LANG:(.*?) \| SRC:(.*?) \| TR:(.*?)$")

    expected_errors = []
    with open(raw_logs_path, "r") as f:
        for line in f:
            if not pattern.match(line.rstrip('\n')):
                expected_errors.append(line)

    with open(error_log_path, "r") as f:
        actual_errors = f.readlines()

    assert actual_errors == expected_errors, "error.log does not contain the exact malformed lines from raw_logs.txt."

def test_stats_json_exists_and_correct():
    raw_logs_path = "/home/user/loc_data/raw_logs.txt"
    stats_json_path = "/home/user/loc_data/stats.json"

    assert os.path.exists(raw_logs_path), f"Input file {raw_logs_path} missing."
    assert os.path.exists(stats_json_path), f"Output file {stats_json_path} was not created."

    pattern = re.compile(r"^\[(.*?)\] LANG:(.*?) \| SRC:(.*?) \| TR:(.*?)$")

    translations = defaultdict(list)

    with open(raw_logs_path, "r") as f:
        for line in f:
            match = pattern.match(line.rstrip('\n'))
            if match:
                timestamp, lang, src, tr = match.groups()
                translations[lang].append((timestamp, src, tr))

    expected_stats = {}
    for lang, items in translations.items():
        # Sort chronologically by timestamp
        items.sort(key=lambda x: x[0])

        # Take the last 3
        last_items = items[-3:]

        ratios = []
        for _, src, tr in last_items:
            if len(src) == 0:
                ratios.append(0.0)
            else:
                ratios.append(len(tr) / len(src))

        avg = sum(ratios) / len(ratios) if ratios else 0.0
        expected_stats[lang] = round(avg, 4)

    with open(stats_json_path, "r") as f:
        try:
            actual_stats = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("stats.json is not valid JSON.")

    # Check keys match exactly
    assert sorted(actual_stats.keys()) == sorted(expected_stats.keys()), "Language keys in stats.json do not match expected languages."

    for lang, expected_val in expected_stats.items():
        actual_val = actual_stats[lang]
        assert math.isclose(actual_val, expected_val, rel_tol=1e-5, abs_tol=1e-4), \
            f"Value for {lang} is incorrect. Expected {expected_val}, got {actual_val}."