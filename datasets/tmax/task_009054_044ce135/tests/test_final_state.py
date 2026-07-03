# test_final_state.py

import os
import json
import stat
import pytest

def test_router_script_exists_and_executable():
    script_path = "/home/user/router.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The script {script_path} is not executable."

def test_routed_json_exists():
    output_path = "/home/user/routed.json"
    assert os.path.isfile(output_path), f"The output file {output_path} was not created."

def test_routed_json_content():
    output_path = "/home/user/routed.json"
    assert os.path.isfile(output_path), f"The output file {output_path} was not created."

    with open(output_path, "r") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {output_path} does not contain valid JSON.")

    expected_data = [
        {
            "timestamp": 1700000000,
            "ip": "10.0.0.1",
            "service": "auth",
            "requested_version": "1.2.5",
            "routed_port": 8081
        },
        {
            "timestamp": 1700000002,
            "ip": "10.0.0.1",
            "service": "auth",
            "requested_version": "1.3.5",
            "routed_port": 8082
        },
        {
            "timestamp": 1700000007,
            "ip": "10.0.0.1",
            "service": "auth",
            "requested_version": "1.2.0",
            "routed_port": 8081
        },
        {
            "timestamp": 1700000008,
            "ip": "192.168.1.5",
            "service": "payment",
            "requested_version": "1.1.4",
            "routed_port": 9090
        },
        {
            "timestamp": 1700000009,
            "ip": "192.168.1.5",
            "service": "payment",
            "requested_version": "1.1.6",
            "routed_port": 9091
        },
        {
            "timestamp": 1700000015,
            "ip": "10.0.0.1",
            "service": "auth",
            "requested_version": "2.1.0",
            "routed_port": 8083
        }
    ]

    assert isinstance(actual_data, list), f"The JSON in {output_path} should be an array."
    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} routed requests, but got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual == expected, f"Mismatch at index {i}. Expected: {expected}, but got: {actual}"