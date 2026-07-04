# test_final_state.py
import os
import re
import csv

INPUT_FILE = "/home/user/config_events.txt"
OUTPUT_DIR = "/home/user/output"
LATEST_CONFIGS_FILE = os.path.join(OUTPUT_DIR, "latest_configs.csv")
HOURLY_COUNTS_FILE = os.path.join(OUTPUT_DIR, "hourly_counts.csv")

def normalize_key(key):
    return re.sub(r'[^a-z0-9]', '_', key.lower())

def compute_expected_state(filepath):
    latest_configs = {}
    unique_values = {}
    hourly_counts = {}

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 5:
                continue

            ts_str, user, action, key, value = parts
            ts = int(ts_str)

            norm_key = normalize_key(key)

            latest_configs[norm_key] = value
            if norm_key not in unique_values:
                unique_values[norm_key] = set()
            unique_values[norm_key].add(value)

            window = ts - (ts % 3600)
            hourly_counts[window] = hourly_counts.get(window, 0) + 1

    expected_configs = []
    for k in sorted(latest_configs.keys()):
        expected_configs.append(f"{k},{latest_configs[k]},{len(unique_values[k])}")

    expected_counts = []
    for w in sorted(hourly_counts.keys()):
        expected_counts.append(f"{w},{hourly_counts[w]}")

    return expected_configs, expected_counts

def test_output_directory_exists():
    assert os.path.isdir(OUTPUT_DIR), f"Output directory {OUTPUT_DIR} was not created."

def test_latest_configs_csv():
    assert os.path.isfile(LATEST_CONFIGS_FILE), f"File {LATEST_CONFIGS_FILE} is missing."

    expected_configs, _ = compute_expected_state(INPUT_FILE)

    with open(LATEST_CONFIGS_FILE, 'r') as f:
        actual_configs = [line.strip() for line in f if line.strip()]

    assert actual_configs == expected_configs, (
        f"Contents of {LATEST_CONFIGS_FILE} do not match expected.\n"
        f"Expected: {expected_configs}\n"
        f"Actual: {actual_configs}"
    )

def test_hourly_counts_csv():
    assert os.path.isfile(HOURLY_COUNTS_FILE), f"File {HOURLY_COUNTS_FILE} is missing."

    _, expected_counts = compute_expected_state(INPUT_FILE)

    with open(HOURLY_COUNTS_FILE, 'r') as f:
        actual_counts = [line.strip() for line in f if line.strip()]

    assert actual_counts == expected_counts, (
        f"Contents of {HOURLY_COUNTS_FILE} do not match expected.\n"
        f"Expected: {expected_counts}\n"
        f"Actual: {actual_counts}"
    )