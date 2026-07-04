# test_final_state.py

import os
import json
import csv

def truncate_ts(ts):
    """Truncates an ISO8601 timestamp to the minute."""
    # Example: 2023-10-25T14:32:45Z -> 2023-10-25T14:32:00Z
    return ts[:17] + "00Z"

def mask_ip(ip):
    """Masks the last octet of an IPv4 address."""
    parts = ip.split('.')
    if len(parts) == 4:
        parts[-1] = '0'
    return '.'.join(parts)

def mask_email(email):
    """Masks the local part of the email."""
    if '@' in email:
        local, domain = email.split('@', 1)
        if len(local) > 0:
            local = local[0] + "***"
        return f"{local}@{domain}"
    return email

def test_merged_jsonl_exists():
    assert os.path.isfile('/home/user/output/merged.jsonl'), "The output file /home/user/output/merged.jsonl is missing. Did the Rust program run successfully?"

def test_merged_jsonl_content():
    # Read and process logs
    logs = {}
    logs_file = '/home/user/data/logs.jsonl'
    assert os.path.isfile(logs_file), f"Input file {logs_file} is missing."

    with open(logs_file, 'r') as f:
        for line in f:
            if line.strip():
                record = json.loads(line)
                minute = truncate_ts(record['ts'])
                uid = record['uid']
                key = (uid, minute)
                # Store the log entry for the join
                logs[key] = record

    # Read and process transactions
    txs = {}
    tx_file = '/home/user/data/tx.csv'
    assert os.path.isfile(tx_file), f"Input file {tx_file} is missing."

    with open(tx_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            minute = truncate_ts(row['tx_ts'])
            uid = row['uid']
            amount = float(row['amount'])
            key = (uid, minute)
            if key not in txs:
                txs[key] = 0.0
            txs[key] += amount

    # Perform Inner Join and create expected output
    expected_output = []
    for key in set(logs.keys()).intersection(set(txs.keys())):
        uid, minute = key
        log = logs[key]
        expected_output.append({
            "minute": minute,
            "uid": uid,
            "masked_ip": mask_ip(log['ip']),
            "masked_email": mask_email(log['email']),
            "total_amount": round(txs[key], 2)
        })

    # Read actual output
    actual_output = []
    with open('/home/user/output/merged.jsonl', 'r') as f:
        for line in f:
            if line.strip():
                try:
                    actual_output.append(json.loads(line))
                except json.JSONDecodeError:
                    assert False, f"Output file contains invalid JSON: {line.strip()}"

    # Sort both lists to ensure order independence
    expected_sorted = sorted(expected_output, key=lambda x: (x['uid'], x['minute']))
    actual_sorted = sorted(actual_output, key=lambda x: (x.get('uid', ''), x.get('minute', '')))

    assert len(expected_sorted) == len(actual_sorted), f"Expected {len(expected_sorted)} records in merged.jsonl, but found {len(actual_sorted)}."

    # Compare records
    for exp, act in zip(expected_sorted, actual_sorted):
        assert 'minute' in act, "Missing 'minute' key in output record."
        assert exp['minute'] == act['minute'], f"Minute mismatch: expected {exp['minute']}, got {act['minute']}."

        assert 'uid' in act, "Missing 'uid' key in output record."
        assert exp['uid'] == act['uid'], f"UID mismatch: expected {exp['uid']}, got {act['uid']}."

        assert 'masked_ip' in act, "Missing 'masked_ip' key in output record."
        assert exp['masked_ip'] == act['masked_ip'], f"IP masking mismatch for uid {exp['uid']}: expected {exp['masked_ip']}, got {act['masked_ip']}."

        assert 'masked_email' in act, "Missing 'masked_email' key in output record."
        assert exp['masked_email'] == act['masked_email'], f"Email masking mismatch for uid {exp['uid']}: expected {exp['masked_email']}, got {act['masked_email']}."

        assert 'total_amount' in act, "Missing 'total_amount' key in output record."
        assert isinstance(act['total_amount'], (int, float)), f"'total_amount' should be a number for uid {exp['uid']}."
        assert abs(exp['total_amount'] - act['total_amount']) < 0.01, f"Total amount mismatch for uid {exp['uid']}: expected {exp['total_amount']}, got {act['total_amount']}."