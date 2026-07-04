# test_final_state.py
import os
import json
import csv
import re
from datetime import datetime, timedelta
import pytest

RAW_LOGS_PATH = "/home/user/data/raw_logs.csv"
OUTPUT_JSON_PATH = "/home/user/investigation_sample.json"
PIPELINE_SH_PATH = "/home/user/pipeline.sh"
CRON_TXT_PATH = "/home/user/cron.txt"

def parse_iso(ts_str):
    if ts_str.endswith('Z'):
        ts_str = ts_str[:-1] + '+00:00'
    return datetime.fromisoformat(ts_str)

def format_iso(dt):
    # Format to match pandas ISO8601 with Z
    return dt.strftime('%Y-%m-%dT%H:%M:%SZ')

def compute_expected_data():
    if not os.path.exists(RAW_LOGS_PATH):
        return []

    records = []
    with open(RAW_LOGS_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                'timestamp': parse_iso(row['timestamp']),
                'level': row['level'],
                'response_ms': float(row['response_ms'])
            })

    if not records:
        return []

    min_ts = min(r['timestamp'] for r in records)
    max_ts = max(r['timestamp'] for r in records)

    # pandas resample('5min') aligns to 5-minute boundaries
    start_bin = min_ts.replace(minute=min_ts.minute - (min_ts.minute % 5), second=0, microsecond=0)
    end_bin = max_ts.replace(minute=max_ts.minute - (max_ts.minute % 5), second=0, microsecond=0)

    bins = {}
    current = start_bin
    while current <= end_bin:
        bins[current] = {'total_requests': 0, 'error_count': 0, 'sum_response_ms': 0.0, 'avg_response_ms': None}
        current += timedelta(minutes=5)

    for r in records:
        ts = r['timestamp']
        b = ts.replace(minute=ts.minute - (ts.minute % 5), second=0, microsecond=0)
        bins[b]['total_requests'] += 1
        if r['level'] == 'ERROR':
            bins[b]['error_count'] += 1
        bins[b]['sum_response_ms'] += r['response_ms']

    # Calculate averages
    for b, data in bins.items():
        if data['total_requests'] > 0:
            data['avg_response_ms'] = data['sum_response_ms'] / data['total_requests']

    # Gap filling
    sorted_bins = sorted(bins.keys())
    for i in range(len(sorted_bins)):
        b = sorted_bins[i]
        if bins[b]['avg_response_ms'] is None:
            # ffill limit 1
            if i > 0 and bins[sorted_bins[i-1]]['total_requests'] > 0:
                bins[b]['avg_response_ms'] = bins[sorted_bins[i-1]]['avg_response_ms']
            else:
                bins[b]['avg_response_ms'] = 0.0

    # Stratified Sampling
    group_a = []
    group_b = []
    for b in sorted_bins:
        item = {
            'timestamp': b,
            'total_requests': bins[b]['total_requests'],
            'error_count': bins[b]['error_count'],
            'avg_response_ms': bins[b]['avg_response_ms']
        }
        if item['error_count'] > 0:
            group_a.append(item)
        else:
            group_b.append(item)

    # Sort Group A: error_count DESC, timestamp ASC
    group_a.sort(key=lambda x: (-x['error_count'], x['timestamp']))
    top_a = group_a[:3]

    # Sort Group B: total_requests DESC, timestamp ASC
    group_b.sort(key=lambda x: (-x['total_requests'], x['timestamp']))
    top_b = group_b[:3]

    final_sample = top_a + top_b
    final_sample.sort(key=lambda x: x['timestamp'])

    # Format output
    expected = []
    for item in final_sample:
        expected.append({
            'timestamp': format_iso(item['timestamp']),
            'total_requests': item['total_requests'],
            'error_count': item['error_count'],
            'avg_response_ms': item['avg_response_ms']
        })

    return expected

def test_pipeline_script_exists_and_executable():
    assert os.path.exists(PIPELINE_SH_PATH), f"Missing pipeline script: {PIPELINE_SH_PATH}"
    assert os.access(PIPELINE_SH_PATH, os.X_OK), f"Pipeline script {PIPELINE_SH_PATH} is not executable."

def test_cron_configuration():
    assert os.path.exists(CRON_TXT_PATH), f"Missing cron configuration file: {CRON_TXT_PATH}"
    with open(CRON_TXT_PATH, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    # Check for the correct cron expression and command
    assert content, f"{CRON_TXT_PATH} is empty."

    # Allow multiple spaces/tabs between fields
    parts = re.split(r'\s+', content)
    assert len(parts) >= 6, f"Cron expression in {CRON_TXT_PATH} does not have enough fields."

    cron_expr = " ".join(parts[:5])
    command = " ".join(parts[5:])

    assert cron_expr == "0 * * * *", f"Cron expression should be '0 * * * *', got '{cron_expr}'"
    assert PIPELINE_SH_PATH in command, f"Cron command should execute {PIPELINE_SH_PATH}, got '{command}'"

def test_investigation_sample_output():
    assert os.path.exists(OUTPUT_JSON_PATH), f"Missing output file: {OUTPUT_JSON_PATH}"

    with open(OUTPUT_JSON_PATH, 'r', encoding='utf-8') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_JSON_PATH} is not valid JSON.")

    assert isinstance(actual_data, list), "JSON output must be a list of objects (orient='records')."
    assert len(actual_data) == 6, f"Expected exactly 6 records in output, found {len(actual_data)}."

    expected_data = compute_expected_data()
    assert len(expected_data) == 6, "Expected data computation failed to find 6 records."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual.get('timestamp') == expected['timestamp'], f"Record {i}: Expected timestamp {expected['timestamp']}, got {actual.get('timestamp')}"
        assert actual.get('total_requests') == expected['total_requests'], f"Record {i}: Expected total_requests {expected['total_requests']}, got {actual.get('total_requests')}"
        assert actual.get('error_count') == expected['error_count'], f"Record {i}: Expected error_count {expected['error_count']}, got {actual.get('error_count')}"

        # Check float values with a small tolerance
        actual_avg = actual.get('avg_response_ms')
        expected_avg = expected['avg_response_ms']
        assert actual_avg is not None, f"Record {i}: Missing avg_response_ms"
        assert abs(actual_avg - expected_avg) < 1e-5, f"Record {i}: Expected avg_response_ms {expected_avg}, got {actual_avg}"