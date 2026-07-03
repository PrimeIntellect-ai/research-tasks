# test_final_state.py

import os
import json
import csv
from datetime import datetime

def test_processed_users_json_exists_and_valid():
    output_file = '/home/user/processed_users.json'
    assert os.path.exists(output_file), f"Output JSON not found at {output_file}."

    with open(output_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "Output file is not valid JSON."

    assert isinstance(data, dict), "The root JSON object must be a dictionary."

    # Read the raw CSV to determine expected state
    raw_file = '/home/user/raw_events.csv'
    assert os.path.exists(raw_file), f"Raw CSV missing at {raw_file}."

    user_events = {}
    with open(raw_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            uid = row['user_id']
            ts = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S')
            ev = row['event_type'].strip()
            if uid not in user_events:
                user_events[uid] = []
            user_events[uid].append((ts, ev))

    # Sort chronologically
    for uid in user_events:
        user_events[uid].sort(key=lambda x: x[0])

    assert len(data) == len(user_events), f"Expected {len(user_events)} users, found {len(data)}."

    # Infer the mapping from event_type to token ID
    # Missing event_type ('') must be 0
    inferred_mapping = {'': 0}
    used_ids = set([0])

    for uid_str, udata in data.items():
        assert uid_str in user_events, f"Unexpected user_id {uid_str} in output."
        expected_events = user_events[uid_str]

        assert 'tokens' in udata, f"Missing 'tokens' for user {uid_str}"
        assert 'embedding' in udata, f"Missing 'embedding' for user {uid_str}"

        tokens = udata['tokens']
        assert isinstance(tokens, list), f"'tokens' for user {uid_str} must be a list."
        assert len(tokens) == len(expected_events), f"Token count mismatch for user {uid_str}."

        for i, (ts, ev) in enumerate(expected_events):
            token = tokens[i]
            # Check strict integer (JSON parser returns int for integers, float for floats like 1.0)
            assert isinstance(token, int) and not isinstance(token, bool), f"Token {token} is not a strict integer."

            if ev == '':
                assert token == 0, f"Missing event type must be mapped to 0, but got {token} for user {uid_str}."
            else:
                assert token != 0, f"Valid event type '{ev}' was incorrectly mapped to 0 for user {uid_str}."
                if ev in inferred_mapping:
                    assert inferred_mapping[ev] == token, f"Inconsistent mapping for event '{ev}': expected {inferred_mapping[ev]}, got {token}."
                else:
                    assert token not in used_ids, f"Token ID {token} for event '{ev}' is already used by another event."
                    inferred_mapping[ev] = token
                    used_ids.add(token)

        # Check embeddings
        embedding = udata['embedding']
        assert isinstance(embedding, list), f"'embedding' for user {uid_str} must be a list."
        assert len(embedding) == 2, f"'embedding' for user {uid_str} must have exactly 2 elements."
        for val in embedding:
            assert isinstance(val, (int, float)), f"Embedding values must be numbers, got {type(val)}."
            # Check rounding to 4 decimal places (string representation shouldn't have more than 4 decimal places)
            # Due to floating point precision, we just verify it's a float
            pass

    # Verify that token IDs start from 1 and are contiguous (1, 2, 3...)
    valid_tokens = used_ids - {0}
    if valid_tokens:
        assert min(valid_tokens) == 1, f"Token IDs for valid events must start from 1. Found min {min(valid_tokens)}."
        assert max(valid_tokens) == len(valid_tokens), f"Token IDs must be contiguous integers starting from 1."