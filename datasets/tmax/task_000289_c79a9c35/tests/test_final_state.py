# test_final_state.py

import os
import json
import pytest

def test_closest_ips_json_exists():
    """Test that the closest_ips.json file exists."""
    file_path = "/home/user/closest_ips.json"
    assert os.path.isfile(file_path), f"Output file is missing: {file_path}"

def test_closest_ips_json_content():
    """Test the content of closest_ips.json for correct IPs and distance."""
    file_path = "/home/user/closest_ips.json"
    assert os.path.isfile(file_path), f"Output file is missing: {file_path}"

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} does not contain valid JSON.")

    # Check keys
    expected_keys = {"ip1", "ip2", "distance"}
    assert set(data.keys()) == expected_keys, f"JSON keys must be exactly {expected_keys}, got {set(data.keys())}"

    # Check IPs
    assert data["ip1"] == "10.0.0.5", f"Expected ip1 to be '10.0.0.5', got '{data['ip1']}'"
    assert data["ip2"] == "192.168.1.100", f"Expected ip2 to be '192.168.1.100', got '{data['ip2']}'"

    # Check distance
    distance = data["distance"]
    assert isinstance(distance, (int, float)), f"Distance must be a number, got {type(distance)}"

    expected_distance = 0.3155
    tolerance = 0.005
    assert abs(distance - expected_distance) <= tolerance, \
        f"Distance {distance} is not within {tolerance} of expected {expected_distance}"