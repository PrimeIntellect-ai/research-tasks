# test_final_state.py

import os
import pytest

def get_expected_snapshots(csv_path):
    events = []
    with open(csv_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) == 3:
                ts, key, val = parts
                events.append((int(ts), key, val))

    if not events:
        return []

    first_ts = events[0][0]
    last_ts = events[-1][0]

    t0 = (first_ts // 1000 + 1) * 1000
    t_end = (last_ts // 1000 + 1) * 1000

    snapshots = []
    state = {}
    event_idx = 0
    n_events = len(events)

    for t in range(t0, t_end + 1000, 1000):
        while event_idx < n_events and events[event_idx][0] < t:
            _, key, val = events[event_idx]
            state[key] = val
            event_idx += 1

        if state:
            sorted_keys = sorted(state.keys())
            state_str = ",".join(f"{k}:{state[k]}" for k in sorted_keys)
            snapshots.append(f"{t}|{state_str}")

    return snapshots

def test_files_exist():
    assert os.path.exists("/home/user/resampler.rs"), "/home/user/resampler.rs is missing"
    assert os.path.exists("/home/user/Makefile"), "/home/user/Makefile is missing"
    assert os.path.exists("/home/user/snapshots.log"), "/home/user/snapshots.log is missing"

def test_snapshots_content():
    csv_path = "/home/user/config_events.csv"
    assert os.path.exists(csv_path), f"{csv_path} is missing"

    expected_snapshots = get_expected_snapshots(csv_path)

    log_path = "/home/user/snapshots.log"
    with open(log_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_snapshots), f"Expected {len(expected_snapshots)} snapshots, but got {len(actual_lines)}"

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_snapshots)):
        assert actual == expected, f"Mismatch at line {i+1}. Expected '{expected}', got '{actual}'"