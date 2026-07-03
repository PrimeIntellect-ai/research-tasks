# test_final_state.py

import os
import json
import csv
import hashlib
from datetime import datetime, timedelta, timezone

def compute_expected_data():
    records = []

    alpha_path = '/home/user/data/stream_alpha.csv'
    if os.path.exists(alpha_path):
        with open(alpha_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                dt_local = datetime.strptime(row['timestamp'], '%Y/%m/%d %H:%M:%S')
                dt_utc = dt_local + timedelta(hours=4)
                dt_utc = dt_utc.replace(tzinfo=timezone.utc)
                records.append({
                    'timestamp_dt': dt_utc,
                    'device_id': row['device_id'],
                    'sensor_value': float(row['sensor_value']),
                    'error_code': int(row['error_code'])
                })

    beta_path = '/home/user/data/stream_beta.csv'
    if os.path.exists(beta_path):
        with open(beta_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                dt_utc = datetime.fromtimestamp(int(row['ts']), tz=timezone.utc)
                records.append({
                    'timestamp_dt': dt_utc,
                    'device_id': row['dev'],
                    'sensor_value': float(row['val']),
                    'error_code': int(row['err'])
                })

    valid_records = []
    for r in records:
        if -50.0 <= r['sensor_value'] <= 150.0 and r['error_code'] == 0:
            valid_records.append(r)

    dedup = {}
    for r in valid_records:
        rounded_val = round(r['sensor_value'], 1)
        hash_str = f"{r['device_id']}_{rounded_val}"
        md5_hash = hashlib.md5(hash_str.encode('utf-8')).hexdigest()

        r['hash'] = md5_hash
        r['rounded_val'] = rounded_val

        if md5_hash not in dedup:
            dedup[md5_hash] = r
        else:
            if r['timestamp_dt'] < dedup[md5_hash]['timestamp_dt']:
                dedup[md5_hash] = r

    final_records = list(dedup.values())
    final_records.sort(key=lambda x: (x['timestamp_dt'], x['device_id']))

    expected = []
    for r in final_records:
        expected.append({
            "timestamp": r['timestamp_dt'].strftime('%Y-%m-%dT%H:%M:%SZ'),
            "device_id": r['device_id'],
            "sensor_value": r['rounded_val'],
            "hash": r['hash']
        })
    return expected

def test_output_file_exists():
    output_path = '/home/user/output/clean_sensors.jsonl'
    assert os.path.isfile(output_path), f"Expected output file {output_path} does not exist."

def test_output_file_contents():
    output_path = '/home/user/output/clean_sensors.jsonl'
    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    actual_records = []
    with open(output_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                actual_records.append(record)
            except json.JSONDecodeError:
                assert False, f"Line {line_num} in {output_path} is not valid JSON."

    expected_records = compute_expected_data()

    assert len(actual_records) == len(expected_records), (
        f"Expected {len(expected_records)} records, but found {len(actual_records)}. "
        "Check your filtering and deduplication logic."
    )

    for i, (actual, expected) in enumerate(zip(actual_records, expected_records)):
        assert set(actual.keys()) == {"timestamp", "device_id", "sensor_value", "hash"}, (
            f"Record {i+1} has incorrect keys. Expected exact keys: timestamp, device_id, sensor_value, hash."
        )
        assert actual["timestamp"] == expected["timestamp"], f"Record {i+1} timestamp mismatch. Expected {expected['timestamp']}, got {actual['timestamp']}."
        assert actual["device_id"] == expected["device_id"], f"Record {i+1} device_id mismatch. Expected {expected['device_id']}, got {actual['device_id']}."
        assert actual["sensor_value"] == expected["sensor_value"], f"Record {i+1} sensor_value mismatch. Expected {expected['sensor_value']}, got {actual['sensor_value']}."
        assert actual["hash"] == expected["hash"], f"Record {i+1} hash mismatch. Expected {expected['hash']}, got {actual['hash']}."