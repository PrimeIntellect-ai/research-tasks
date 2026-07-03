# test_final_state.py

import os
import json
import pytest

def test_corrupted_string_extracted():
    filepath = "/home/user/corrupted_string.txt"
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    with open(filepath, "r") as f:
        content = f.read().strip()

    expected = "CRITICAL_CORRUPT: x9F2kL0m"
    assert content == expected, f"Expected corrupted string to be '{expected}', but got '{content}'."

def test_final_counts_json():
    filepath = "/home/user/final_counts.json"
    assert os.path.isfile(filepath), f"File {filepath} is missing. Did you run the Go program?"

    with open(filepath, "r") as f:
        try:
            counts = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {filepath} does not contain valid JSON.")

    expected_counts = {
        "ERROR": 2,
        "FATAL": 1,
        "INFO": 6,
        "WARN": 3
    }

    assert counts == expected_counts, f"Expected counts {expected_counts}, but got {counts}."

def test_go_script_fixed():
    filepath = "/home/user/log_processor.go"
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    with open(filepath, "r") as f:
        content = f.read()

    # Check that the off-by-one bug is fixed.
    # The original had `len(lines)-1`.
    assert "len(lines)-1" not in content, "The off-by-one error `len(lines)-1` is still present in the Go script."

    # Check for some form of synchronization or safe concurrent map usage.
    # Typical fixes involve sync.Mutex, sync.RWMutex, sync.Map, or channels.
    has_mutex = "Mutex" in content
    has_sync_map = "sync.Map" in content
    has_channels = "chan " in content

    assert has_mutex or has_sync_map or has_channels, "No synchronization mechanism (Mutex, sync.Map, channels) found in the Go script to fix the race condition."