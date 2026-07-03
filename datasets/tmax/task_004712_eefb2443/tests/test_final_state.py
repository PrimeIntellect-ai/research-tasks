# test_final_state.py

import os
import json
import re
import pytest

def test_binary_exists():
    binary_path = "/home/user/ws_server/target/release/ws_server"
    assert os.path.isfile(binary_path), f"Compiled binary not found at {binary_path}. Did you successfully compile the Rust project?"
    assert os.access(binary_path, os.X_OK), f"File at {binary_path} is not executable."

def test_test_results():
    results_path = "/home/user/test_results.json"
    assert os.path.isfile(results_path), f"{results_path} not found. Did you run the test_client.py script?"

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Could not parse {results_path} as valid JSON.")

    assert data.get("success") is True, f"Expected 'success' to be true in {results_path}, but got {data.get('success')}."

def test_memory_profile_exists():
    profile_path = "/home/user/memory_profile.txt"
    assert os.path.isfile(profile_path), f"{profile_path} not found. Did you run the server under the time command?"

    with open(profile_path, "r") as f:
        content = f.read()

    assert "Maximum resident set size (kbytes):" in content, f"{profile_path} does not contain the expected output from '/usr/bin/time -v'."

def test_max_memory_value():
    profile_path = "/home/user/memory_profile.txt"
    max_memory_path = "/home/user/max_memory.txt"

    assert os.path.isfile(profile_path), f"{profile_path} is missing."
    assert os.path.isfile(max_memory_path), f"{max_memory_path} not found. Did you extract the memory value?"

    with open(profile_path, "r") as f:
        content = f.read()

    match = re.search(r"Maximum resident set size \(kbytes\):\s*(\d+)", content)
    assert match is not None, f"Could not find 'Maximum resident set size (kbytes):' in {profile_path}."
    expected_val = int(match.group(1))

    with open(max_memory_path, "r") as f:
        val_str = f.read().strip()

    assert val_str.isdigit(), f"{max_memory_path} does not contain a valid integer. Found: '{val_str}'"
    actual_val = int(val_str)

    assert actual_val == expected_val, f"Value in {max_memory_path} ({actual_val}) does not match the value extracted from {profile_path} ({expected_val})."