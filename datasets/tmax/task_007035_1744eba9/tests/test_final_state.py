# test_final_state.py

import os
import csv
from collections import defaultdict

def test_pipeline_sh_exists_and_executable():
    path = "/home/user/pipeline.sh"
    assert os.path.exists(path), f"{path} does not exist."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_process_executable_exists():
    path = "/home/user/process"
    assert os.path.exists(path), f"{path} does not exist. Did the pipeline compile the Rust program?"
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_fr_stats_csv_and_max_avg():
    logs_path = "/home/user/translation_logs.csv"
    assert os.path.exists(logs_path), f"{logs_path} does not exist."

    # Derive expected results from the actual input data
    daily_words = defaultdict(int)
    with open(logs_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['locale'] == 'fr-FR':
                date = row['timestamp'][:10]
                daily_words[date] += int(row['words'])

    sorted_dates = sorted(daily_words.keys())

    expected_rows = []
    max_avg = 0.0

    for i, date in enumerate(sorted_dates):
        start_idx = max(0, i - 2)
        window = [daily_words[sorted_dates[j]] for j in range(start_idx, i + 1)]
        avg = sum(window) / len(window)
        expected_rows.append((date, str(daily_words[date]), f"{avg:.2f}"))
        if avg > max_avg:
            max_avg = avg

    # Check fr_stats.csv
    stats_path = "/home/user/fr_stats.csv"
    assert os.path.exists(stats_path), f"{stats_path} does not exist."

    with open(stats_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['date', 'daily_words', 'rolling_avg'], "Incorrect header in fr_stats.csv."

        actual_rows = list(reader)

    assert len(actual_rows) == len(expected_rows), f"Incorrect number of rows in fr_stats.csv. Expected {len(expected_rows)}, got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert tuple(actual) == expected, f"Row {i+1} mismatch in fr_stats.csv: expected {expected}, got {tuple(actual)}."

    # Check max_avg.txt
    max_path = "/home/user/max_avg.txt"
    assert os.path.exists(max_path), f"{max_path} does not exist."

    with open(max_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    expected_max_str = f"{max_avg:.2f}"
    assert content == expected_max_str, f"Content of max_avg.txt mismatch: expected '{expected_max_str}', got '{content}'."