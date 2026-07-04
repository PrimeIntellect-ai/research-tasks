# test_final_state.py

import os
import json
import pytest

def get_expected_outputs(input_file):
    if not os.path.exists(input_file):
        pytest.fail(f"Input file {input_file} does not exist.")

    events = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                events.append(json.loads(line))

    # Sort chronologically by ts, then lexicographically by id
    events.sort(key=lambda x: (x['ts'], x['id']))

    last_accepted = {}
    valid_events = []

    expected_log = []
    expected_stats = []

    for event in events:
        evt_id = event['id']
        ts = event['ts']
        module = event['module']
        key = event['key']
        value = event['value']

        state_key = (module, key)

        if state_key in last_accepted and last_accepted[state_key] == value:
            expected_log.append(f"DUPLICATE: {evt_id}")
        else:
            last_accepted[state_key] = value
            byte_len = len(value.encode('utf-8'))
            expected_log.append(f"VALID: {evt_id} - {module} - {byte_len}")

            valid_events.append((evt_id, ts))

            # Compute rolling count
            rolling_count = sum(1 for _, v_ts in valid_events if ts - 60 <= v_ts <= ts)
            expected_stats.append(f"{evt_id},{rolling_count}")

    return expected_log, expected_stats

def test_pipeline_log():
    log_file = '/home/user/pipeline.log'
    input_file = '/home/user/config_changes.jsonl'

    assert os.path.exists(log_file), f"Output file {log_file} is missing."

    expected_log, _ = get_expected_outputs(input_file)

    with open(log_file, 'r', encoding='utf-8') as f:
        actual_log = [line.strip() for line in f if line.strip()]

    assert actual_log == expected_log, f"Contents of {log_file} do not match the expected output. Expected {len(expected_log)} lines, got {len(actual_log)} lines. First mismatch or difference should be checked."

def test_stats_csv():
    stats_file = '/home/user/stats.csv'
    input_file = '/home/user/config_changes.jsonl'

    assert os.path.exists(stats_file), f"Output file {stats_file} is missing."

    _, expected_stats = get_expected_outputs(input_file)

    with open(stats_file, 'r', encoding='utf-8') as f:
        actual_stats = [line.strip() for line in f if line.strip()]

    assert actual_stats == expected_stats, f"Contents of {stats_file} do not match the expected output. Expected {len(expected_stats)} lines, got {len(actual_stats)} lines."