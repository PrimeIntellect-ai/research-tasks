# test_final_state.py

import os
import json
import math
import pytest

def get_expected_results():
    log_a_path = "/home/user/ticket/service_a.log"
    assert os.path.isfile(log_a_path), f"Missing {log_a_path}"

    values = []
    with open(log_a_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 4 and parts[2] == "Sent:":
                values.append(float(parts[3]))

    assert len(values) > 0, "No values found in service_a.log"

    count = 0
    mean = 0.0
    M2 = 0.0
    accepted = 0
    rejected = 0

    for val in values:
        count += 1
        delta = val - mean
        mean += delta / count
        delta2 = val - mean
        M2 += delta * delta2

        if count < 3:
            accepted += 1
            continue

        variance = M2 / count
        stddev = math.sqrt(variance)

        if abs(val - mean) > 3 * stddev:
            rejected += 1
        else:
            accepted += 1

    return accepted, rejected, round(mean, 4)

def test_resolution_json_exists_and_correct():
    resolution_path = "/home/user/ticket/resolution.json"
    assert os.path.isfile(resolution_path), f"Missing {resolution_path}. Did you run run_pipeline.py?"

    with open(resolution_path, "r") as f:
        try:
            result = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{resolution_path} is not valid JSON")

    assert "accepted" in result, "Missing 'accepted' key in resolution.json"
    assert "rejected" in result, "Missing 'rejected' key in resolution.json"

    expected_accepted, expected_rejected, expected_mean = get_expected_results()

    assert result["accepted"] == expected_accepted, f"Expected {expected_accepted} accepted, got {result['accepted']}"
    assert result["rejected"] == expected_rejected, f"Expected {expected_rejected} rejected, got {result['rejected']}"