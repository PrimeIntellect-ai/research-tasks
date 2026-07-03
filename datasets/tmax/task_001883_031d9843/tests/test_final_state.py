# test_final_state.py

import os
import re
import difflib
import pytest

def normalize_proto(text):
    # Remove all whitespace and comments for structural comparison
    text = re.sub(r'//.*', '', text)
    text = re.sub(r'\s+', '', text)
    return text.lower()

def test_sensor_proto_exists_and_matches():
    target_file = '/app/sensor.proto'
    assert os.path.isfile(target_file), f"Target file {target_file} does not exist."

    expected_proto = """
syntax="proto3";
message SensorData {
    int32 sensor_id = 1;
    float temperature = 2;
    double timestamp = 3;
    string status = 4;
}
"""

    with open(target_file, 'r') as f:
        actual_proto = f.read()

    expected_norm = normalize_proto(expected_proto)
    actual_norm = normalize_proto(actual_proto)

    ratio = difflib.SequenceMatcher(None, expected_norm, actual_norm).ratio()
    threshold = 0.90

    assert ratio >= threshold, f"Similarity ratio {ratio:.4f} is below the threshold of {threshold}. Actual normalized: {actual_norm}"