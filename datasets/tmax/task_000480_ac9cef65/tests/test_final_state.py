# test_final_state.py
import os
import csv
from collections import defaultdict

def test_pipeline_and_analyzer_exist():
    assert os.path.isfile('/home/user/pipeline.sh'), "/home/user/pipeline.sh is missing."
    assert os.access('/home/user/pipeline.sh', os.X_OK), "/home/user/pipeline.sh is not executable."
    assert os.path.isfile('/home/user/analyzer.c'), "/home/user/analyzer.c is missing."

def test_anomalies_report():
    raw_events_path = '/home/user/raw_events.csv'
    report_path = '/home/user/anomalies_report.csv'

    assert os.path.isfile(raw_events_path), f"{raw_events_path} is missing."
    assert os.path.isfile(report_path), f"{report_path} was not generated."

    # 1. Deduplicate records
    # Keep the last occurrence of each translation_id
    records = []
    with open(raw_events_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 5:
                continue
            records.append({
                'timestamp': int(row[0]),
                'translation_id': row[1],
                'quality_score': float(row[4])
            })

    # Find the last occurrence for each translation_id
    last_occurrences = {}
    for i, rec in enumerate(records):
        last_occurrences[rec['translation_id']] = rec

    # Sort by timestamp ascending
    deduped = sorted(last_occurrences.values(), key=lambda x: x['timestamp'])

    # 2. Time-based bucketing
    buckets = defaultdict(list)
    for rec in deduped:
        bucket_id = rec['timestamp'] // 3600
        buckets[bucket_id].append(rec['quality_score'])

    sorted_bucket_ids = sorted(buckets.keys())

    # 3. Aggregation and Rolling Average
    expected_output_lines = []
    hourly_averages = []

    for bucket_id in sorted_bucket_ids:
        scores = buckets[bucket_id]
        hourly_avg = sum(scores) / len(scores)
        hourly_averages.append(hourly_avg)

        # Last 3 buckets including current
        window = hourly_averages[-3:]
        rolling_avg = sum(window) / len(window)

        # Anomaly detection
        anomaly_flag = 1 if hourly_avg < (rolling_avg - 5.0) else 0

        expected_output_lines.append(
            f"{bucket_id},{hourly_avg:.2f},{rolling_avg:.2f},{anomaly_flag}"
        )

    # 4. Compare with actual report
    with open(report_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_output_lines), \
        f"Expected {len(expected_output_lines)} lines in report, but found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_output_lines)):
        assert actual == expected, \
            f"Mismatch at line {i+1}: expected '{expected}', got '{actual}'."