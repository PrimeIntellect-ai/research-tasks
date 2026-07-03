# test_final_state.py
import os
import json
import csv
import io

def test_clean_data_csv():
    raw_path = "/home/user/raw_data.jsonl"
    clean_path = "/home/user/clean_data.csv"

    assert os.path.exists(clean_path), f"File {clean_path} is missing."

    # Compute expected state based on the raw data
    records = {}
    with open(raw_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            ts = data['timestamp']
            mid = data['metric_id'].lower()
            # Overwrites previous entries, effectively keeping the LAST occurrence
            records[(ts, mid)] = {
                'timestamp': ts,
                'metric_id': mid,
                'value': data['value'],
                'message': data['message']
            }

    # Sort by timestamp, then metric_id
    sorted_keys = sorted(records.keys(), key=lambda x: (x[0], x[1]))

    expected_output = io.StringIO()
    # QUOTE_NONNUMERIC matches `jq -r '@csv'` behavior (quotes strings, leaves numbers unquoted)
    writer = csv.writer(expected_output, quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
    for k in sorted_keys:
        row = records[k]
        writer.writerow([row['timestamp'], row['metric_id'], row['value'], row['message']])

    expected_csv_str = expected_output.getvalue().strip()

    with open(clean_path, 'r', encoding='utf-8') as f:
        actual_csv_str = f.read().strip()

    assert actual_csv_str == expected_csv_str, (
        "The content of clean_data.csv does not match the expected output. "
        "Ensure you have deduplicated correctly (keeping the last occurrence), "
        "normalized metric_ids to lowercase, sorted by timestamp then metric_id, "
        "and properly formatted as CSV."
    )

def test_report_txt():
    raw_path = "/home/user/raw_data.jsonl"
    report_path = "/home/user/report.txt"

    assert os.path.exists(report_path), f"File {report_path} is missing."

    # Recompute the expected metrics and count
    records = {}
    with open(raw_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            ts = data['timestamp']
            mid = data['metric_id'].lower()
            records[(ts, mid)] = True

    count = len(records)
    unique_metrics = sorted(list(set([k[1] for k in records.keys()])))
    metrics_str = ",".join(unique_metrics)

    expected_report = (
        "ETL Cleanup Report\n"
        "------------------\n"
        f"Total Clean Records: {count}\n"
        f"Unique Metrics: {metrics_str}"
    )

    with open(report_path, 'r', encoding='utf-8') as f:
        actual_report = f.read().strip()

    assert actual_report == expected_report, (
        "The content of report.txt does not match the expected output. "
        "Ensure the template is exactly as specified, the count is correct, "
        "and the unique metrics are comma-separated and alphabetically sorted."
    )