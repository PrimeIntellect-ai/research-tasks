# test_final_state.py

import os
import csv
import hashlib
import pytest
from datetime import datetime, timedelta

def compute_expected_state(input_path):
    if not os.path.exists(input_path):
        return []

    with open(input_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Parse and group by server
    servers = {}
    env_servers = {}
    for row in rows:
        env = row['environment']
        srv = row['server_name']
        dt = row['timestamp']
        text = row['config_text']

        if env not in env_servers:
            env_servers[env] = set()
        env_servers[env].add(srv)

        if srv not in servers:
            servers[srv] = []
        servers[srv].append((dt, text, env))

    # Stratified sampling: first 2 servers per environment alphabetically
    sampled_servers = set()
    for env, srv_set in env_servers.items():
        sorted_srvs = sorted(list(srv_set))
        sampled_servers.update(sorted_srvs[:2])

    # Generate daily timeline
    start_date = datetime(2023, 10, 1)
    end_date = datetime(2023, 10, 7)

    expected_rows = []

    for srv in sampled_servers:
        srv_configs = servers[srv]
        env = srv_configs[0][2]

        # Sort configs by timestamp
        srv_configs.sort(key=lambda x: x[0])

        for day_offset in range(8):
            current_date = start_date + timedelta(days=day_offset)
            if current_date > end_date:
                break

            date_str = current_date.strftime('%Y-%m-%d')
            current_date_end = date_str + "T23:59:59Z"

            # Find the latest config on or before current_date_end
            latest_text = None
            for dt, text, _ in srv_configs:
                if dt <= current_date_end:
                    latest_text = text

            if latest_text is None:
                config_hash = "NO_CONFIG"
            else:
                config_hash = hashlib.md5(latest_text.encode('utf-8')).hexdigest()

            expected_rows.append({
                'date': date_str,
                'server_name': srv,
                'environment': env,
                'config_hash': config_hash
            })

    # Sort expected rows
    expected_rows.sort(key=lambda x: (x['environment'], x['server_name'], x['date']))
    return expected_rows

def test_stratified_config_timeline_exists():
    output_path = "/home/user/stratified_config_timeline.csv"
    assert os.path.isfile(output_path), f"Expected output file {output_path} does not exist."

def test_stratified_config_timeline_content():
    input_path = "/home/user/config_history.csv"
    output_path = "/home/user/stratified_config_timeline.csv"

    expected_rows = compute_expected_state(input_path)

    with open(output_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        actual_rows = list(reader)

    assert reader.fieldnames == ['date', 'server_name', 'environment', 'config_hash'], \
        f"CSV headers are incorrect. Expected ['date', 'server_name', 'environment', 'config_hash'], got {reader.fieldnames}"

    assert len(actual_rows) == len(expected_rows), \
        f"Expected {len(expected_rows)} rows, but got {len(actual_rows)} rows in the output CSV."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual['date'] == expected['date'], f"Row {i+1}: Expected date {expected['date']}, got {actual['date']}"
        assert actual['server_name'] == expected['server_name'], f"Row {i+1}: Expected server_name {expected['server_name']}, got {actual['server_name']}"
        assert actual['environment'] == expected['environment'], f"Row {i+1}: Expected environment {expected['environment']}, got {actual['environment']}"
        assert actual['config_hash'] == expected['config_hash'], f"Row {i+1}: Server {actual['server_name']} on {actual['date']} expected hash {expected['config_hash']}, got {actual['config_hash']}"