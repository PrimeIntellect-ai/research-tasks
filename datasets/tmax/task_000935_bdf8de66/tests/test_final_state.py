# test_final_state.py
import os
import json
import csv
import pytest

def test_normalized_logs_exist_and_correct():
    output_path = '/home/user/normalized_logs.jsonl'
    assert os.path.exists(output_path), f"Output file not found: {output_path}"

    users_path = '/home/user/users.json'
    assert os.path.exists(users_path), f"Input file missing: {users_path}"

    raw_logs_path = '/home/user/raw_logs.csv'
    assert os.path.exists(raw_logs_path), f"Input file missing: {raw_logs_path}"

    # Derive truth from input files
    with open(users_path, 'r', encoding='utf-8') as f:
        users_list = json.load(f)
        users = {u['user_id']: u for u in users_list}

    expected_logs = {}
    with open(raw_logs_path, 'r', encoding='iso-8859-1') as f:
        reader = csv.DictReader(f)
        for row in reader:
            log_id = str(row['log_id'])
            # Deduplication: keep only the first occurrence
            if log_id not in expected_logs:
                user_id = row['user_id']
                user = users.get(user_id, {})
                expected_logs[log_id] = {
                    'log_id': log_id,
                    'timestamp': row['timestamp'],
                    'username': user.get('username', ''),
                    'department': user.get('department', ''),
                    'cleaned_message': row['message'].replace('\n', ' ')
                }

    actual_logs = {}
    with open(output_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON line at line {line_num} in output: {line}")

            if 'log_id' not in obj:
                pytest.fail(f"Missing 'log_id' in output line {line_num}: {line}")

            # log_id can be int or string, normalize to string for comparison
            log_id = str(obj['log_id'])
            actual_logs[log_id] = obj

    assert len(actual_logs) == len(expected_logs), f"Expected {len(expected_logs)} unique logs, found {len(actual_logs)}"

    for log_id, expected in expected_logs.items():
        assert log_id in actual_logs, f"Missing log_id '{log_id}' in output"
        actual = actual_logs[log_id]

        assert str(actual.get('log_id')) == expected['log_id'], f"Mismatch in log_id for record {log_id}"
        assert actual.get('timestamp') == expected['timestamp'], f"Mismatch in timestamp for record {log_id}"
        assert actual.get('username') == expected['username'], f"Mismatch in username for record {log_id}"
        assert actual.get('department') == expected['department'], f"Mismatch in department for record {log_id}"
        assert actual.get('cleaned_message') == expected['cleaned_message'], f"Mismatch in cleaned_message for record {log_id}. Make sure newlines are replaced by a single space and encoding is correct."