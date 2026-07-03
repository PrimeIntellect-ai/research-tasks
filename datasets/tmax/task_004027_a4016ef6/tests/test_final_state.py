# test_final_state.py

import os
import json
import urllib.request

def test_compression_size():
    dat_path = '/home/user/data/configs.dat'
    assert os.path.exists(dat_path), f"File {dat_path} does not exist. Did you run the compression script?"

    size = os.path.getsize(dat_path)
    threshold = 85000
    assert size < threshold, f"Compression size metric failed: {dat_path} is {size} bytes, which is not less than the threshold of {threshold} bytes."

def test_data_integrity():
    raw_configs_dir = '/home/user/data/raw_configs'
    assert os.path.exists(raw_configs_dir), f"Directory {raw_configs_dir} does not exist."

    # Generate reference CSV data from raw JSON files
    records = []
    for fname in os.listdir(raw_configs_dir):
        if fname.endswith('.json'):
            with open(os.path.join(raw_configs_dir, fname), 'r') as f:
                data = json.load(f)
                records.append({
                    'timestamp': int(data['timestamp']),
                    'service': data['service'],
                    'rate_limit': data['config']['rate_limit'],
                    'timeout': data['config']['timeout']
                })

    # Sort chronologically by timestamp
    records.sort(key=lambda x: x['timestamp'])

    expected_lines = []
    for r in records:
        expected_lines.append(f"{r['timestamp']},{r['service']},{r['rate_limit']},{r['timeout']}")

    # Fetch from API
    url = "http://localhost:8080/history"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            actual_csv = response.read().decode('utf-8')
    except Exception as e:
        assert False, f"Failed to fetch data from {url}. Are Nginx and Flask running and configured correctly? Error: {e}"

    actual_lines = [line.strip() for line in actual_csv.split('\n') if line.strip()]

    # Tolerate if the user included a header row
    if actual_lines and actual_lines[0] == "timestamp,service,rate_limit,timeout":
        actual_lines = actual_lines[1:]

    assert len(actual_lines) == len(expected_lines), f"Data integrity metric failed: Expected {len(expected_lines)} rows, but got {len(actual_lines)} rows from the API."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Data integrity metric failed at row {i+1}:\nExpected: {expected}\nActual:   {actual}"