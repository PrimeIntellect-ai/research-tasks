# test_final_state.py
import json
import struct
import os
import pytest

def parse_version(v: str):
    parts = v.split('-')
    base = parts[0].split('.')
    major = int(base[0])
    minor = int(base[1])
    patch = int(base[2])
    tag = parts[1] if len(parts) > 1 else 'final'
    tag_weights = {'alpha': 1, 'beta': 2, 'rc': 3, 'final': 4}
    return (major, minor, patch, tag_weights.get(tag, 0))

def get_expected_approvals(jsonl_path: str):
    approvals = []
    history = {}
    with open(jsonl_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            req = json.loads(line)
            env_id = req['env_id']
            ts = req['timestamp']
            cur = req['current_version']
            tgt = req['target_version']

            if parse_version(tgt) > parse_version(cur):
                env_history = history.get(env_id, [])
                # Filter timestamps to only those strictly within the 60s window
                env_history = [t for t in env_history if ts - t < 60]

                if len(env_history) < 2:
                    env_history.append(ts)
                    history[env_id] = env_history
                    approvals.append((env_id, ts, tgt.encode('utf-8')))
    return approvals

def test_approved_bin_exists_and_correct():
    bin_path = '/home/user/approved.bin'
    jsonl_path = '/home/user/requests.jsonl'

    assert os.path.isfile(bin_path), f"Output file {bin_path} does not exist. Did you run the C program?"
    assert os.path.isfile(jsonl_path), f"Input file {jsonl_path} is missing."

    expected = get_expected_approvals(jsonl_path)

    with open(bin_path, 'rb') as f:
        data = f.read()

    offset = 0
    actual = []
    try:
        while offset < len(data):
            env_id, ts, tgt_len = struct.unpack_from('<IQB', data, offset)
            offset += 13
            tgt = data[offset:offset+tgt_len]
            offset += tgt_len
            actual.append((env_id, ts, tgt))
    except struct.error:
        pytest.fail(f"Failed to parse binary file at offset {offset}: malformed structure or unexpected EOF.")

    assert offset == len(data), f"Extra unparsed bytes found at the end of {bin_path}. Expected EOF at offset {offset}."

    assert len(actual) == len(expected), f"Expected {len(expected)} approved requests, but found {len(actual)} in binary file."

    for i, (act, exp) in enumerate(zip(actual, expected)):
        assert act == exp, f"Mismatch at approval record {i+1}:\nExpected: env_id={exp[0]}, ts={exp[1]}, target_version={exp[2].decode()}\nFound: env_id={act[0]}, ts={act[1]}, target_version={act[2].decode(errors='replace')}"