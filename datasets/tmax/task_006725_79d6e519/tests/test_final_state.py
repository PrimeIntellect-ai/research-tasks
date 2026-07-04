# test_final_state.py
import os
import json
import csv
import urllib.parse
import re

def get_all_expected_records():
    file_path = "/home/user/raw_logs.csv"
    if not os.path.exists(file_path):
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    exploded = []
    for row in rows:
        region = row['region']
        ip = row['ip_address']
        for date in ['2023-10-01', '2023-10-02', '2023-10-03']:
            val = row[date]
            if val and val != 'NaN':
                reqs = val.split('|')
                for req in reqs:
                    req_dec = urllib.parse.unquote(req)
                    match = re.match(r'"([A-Z]+)\s+([^\s]+)\s+[^"]+"\s+(\d+)', req_dec)
                    if match:
                        method = match.group(1)
                        endpoint = match.group(2).split('?')[0].lower()
                        status = int(match.group(3))
                        exploded.append({
                            'region': region,
                            'ip_address': ip,
                            'date': date,
                            'method': method,
                            'endpoint': endpoint,
                            'status_code': status
                        })
    return exploded

def test_sampled_logs_json_exists():
    file_path = "/home/user/sampled_logs.json"
    assert os.path.isfile(file_path), f"Output file {file_path} does not exist."

def test_sampled_logs_json_format():
    file_path = "/home/user/sampled_logs.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "Output file is not valid JSON."

    assert isinstance(data, list), "JSON output should be a list of records."
    if len(data) > 0:
        expected_keys = {'region', 'ip_address', 'date', 'method', 'endpoint', 'status_code'}
        assert set(data[0].keys()) == expected_keys, f"Expected keys {expected_keys}, got {set(data[0].keys())}"

def test_sampled_logs_content_and_sampling():
    file_path = "/home/user/sampled_logs.json"
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_expected = get_all_expected_records()

    # Check that every record in the output is a valid processed record
    for record in data:
        assert record in all_expected, f"Record {record} is not a valid parsed and cleaned log entry. Check your decoding, parsing, and normalization."
        assert '?' not in record['endpoint'], f"Query parameters should be removed from endpoint: {record['endpoint']}"
        assert record['endpoint'] == record['endpoint'].lower(), f"Endpoint should be lowercased: {record['endpoint']}"

    # Group expected records to find expected counts
    expected_groups = {}
    for item in all_expected:
        key = (item['region'], item['status_code'])
        expected_groups[key] = expected_groups.get(key, 0) + 1

    # Group actual records
    actual_groups = {}
    for item in data:
        key = (item['region'], item['status_code'])
        actual_groups[key] = actual_groups.get(key, 0) + 1

    # Verify exact sampling counts
    for key, total_count in expected_groups.items():
        expected_sampled = min(2, total_count)
        actual_sampled = actual_groups.get(key, 0)
        assert actual_sampled == expected_sampled, f"Group {key} should have {expected_sampled} samples, but got {actual_sampled}."

    # Ensure no extra groups
    for key in actual_groups:
        assert key in expected_groups, f"Found unexpected group {key} in output."