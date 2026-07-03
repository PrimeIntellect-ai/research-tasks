# test_final_state.py

import os
import re
import csv
from collections import defaultdict

def parse_and_process_log(log_path):
    if not os.path.exists(log_path):
        return []

    # Regex to parse the log line
    line_re = re.compile(r'^\[(.*?)\] User=(.*?) Action=(.*?) Target=(.*?) Details="(.*?)"$')
    lines_added_re = re.compile(r'lines_added:\s*(\d+)')

    last_accepted = {}

    # Structure to hold bucketed data
    # bucket -> { 'changes': int, 'targets': set(), 'lines_added': int }
    buckets = defaultdict(lambda: {'changes': 0, 'targets': set(), 'lines_added': 0})

    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            match = line_re.match(line)
            if not match:
                continue

            timestamp, user, action, target, details = match.groups()

            # Normalize target
            target = target.lower()
            target = re.sub(r'/+', '/', target)

            # Deduplication
            event_signature = (action, details)
            if target in last_accepted and last_accepted[target] == event_signature:
                continue

            last_accepted[target] = event_signature

            # Feature extraction
            lines_match = lines_added_re.search(details)
            lines_added = int(lines_match.group(1)) if lines_match else 0

            # Time-based bucketing
            # Assuming format YYYY-MM-DDTHH:MM:SSZ
            # Truncate to hour
            if len(timestamp) >= 19 and timestamp[10] == 'T':
                hour_bucket = timestamp[:14] + "00:00Z"
            else:
                hour_bucket = timestamp # Fallback if format is weird

            buckets[hour_bucket]['changes'] += 1
            buckets[hour_bucket]['targets'].add(target)
            buckets[hour_bucket]['lines_added'] += lines_added

    # Generate expected CSV rows
    expected_rows = []
    for bucket in sorted(buckets.keys()):
        data = buckets[bucket]
        expected_rows.append([
            bucket,
            str(data['changes']),
            str(len(data['targets'])),
            str(data['lines_added'])
        ])

    return expected_rows

def test_summary_csv_exists():
    csv_path = "/home/user/summary.csv"
    assert os.path.isfile(csv_path), f"Expected output file {csv_path} does not exist."

def test_summary_csv_content():
    log_path = "/home/user/config_changes.log"
    csv_path = "/home/user/summary.csv"

    assert os.path.isfile(log_path), f"Input log file {log_path} is missing, cannot verify."
    assert os.path.isfile(csv_path), f"Output file {csv_path} is missing."

    expected_data = parse_and_process_log(log_path)

    actual_data = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        assert headers == ["Hour_Bucket", "Total_Changes", "Unique_Targets", "Total_Lines_Added"], \
            f"CSV headers are incorrect. Got: {headers}"

        for row in reader:
            if any(row):  # skip empty rows
                actual_data.append(row)

    assert len(actual_data) == len(expected_data), \
        f"Expected {len(expected_data)} data rows, but found {len(actual_data)}."

    for i, (actual_row, expected_row) in enumerate(zip(actual_data, expected_data)):
        assert actual_row == expected_row, \
            f"Row {i+1} mismatch. Expected {expected_row}, got {actual_row}."