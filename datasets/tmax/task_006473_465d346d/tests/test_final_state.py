# test_final_state.py

import os
import json
import math
import pytest

TRACE_LOG_PATH = "/home/user/trace.log"
RESULT_JSON_PATH = "/home/user/result.json"

def test_trace_log_exists_and_correct():
    assert os.path.isfile(TRACE_LOG_PATH), f"{TRACE_LOG_PATH} is missing. Did you generate the trace log?"

    with open(TRACE_LOG_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected exactly 5 trace lines, got {len(lines)}."

    expected_values = [1000000.10, 1000000.20, 1000000.15, 1000000.25, 1000000.10]

    for i, expected_val in enumerate(expected_values, start=1):
        line = lines[i-1]
        prefix = f"Parsed value {i}: "
        assert line.startswith(prefix), f"Line {i} does not start with expected prefix '{prefix}'. Got: {line}"

        val_str = line[len(prefix):]
        try:
            val = float(val_str)
        except ValueError:
            pytest.fail(f"Could not parse float from trace line {i}: {val_str}")

        assert math.isclose(val, expected_val, rel_tol=1e-9), f"Expected value {expected_val} on line {i}, got {val}"

def test_result_json_exists_and_correct():
    assert os.path.isfile(RESULT_JSON_PATH), f"{RESULT_JSON_PATH} is missing. Did you write the final metrics?"

    with open(RESULT_JSON_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RESULT_JSON_PATH} does not contain valid JSON.")

    assert "count" in data, "JSON missing 'count' key."
    assert "mean" in data, "JSON missing 'mean' key."
    assert "variance" in data, "JSON missing 'variance' key."

    assert data["count"] == 10, f"Expected count to be 10, got {data['count']}."
    assert math.isclose(data["mean"], 1000000.16, rel_tol=1e-9), f"Expected mean to be ~1000000.16, got {data['mean']}."

    variance = data["variance"]
    assert variance > 0, f"Variance must be positive, got {variance}."
    assert math.isclose(variance, 0.0054, rel_tol=1e-5), f"Expected population variance to be ~0.0054, got {variance}. Ensure you are using a numerically stable algorithm."