# test_final_state.py

import os
import json
import pytest

OUTPUT_PATH = "/home/user/oncall/fixed_anomalies.jsonl"

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} is missing. Did you run the aggregator script and redirect output?"

def test_output_file_content_and_logic():
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} is missing."

    with open(OUTPUT_PATH, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 100, f"Output must contain exactly 100 lines, found {len(lines)}."

    data = []
    for i, line in enumerate(lines):
        try:
            data.append(json.loads(line))
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} is not valid JSON: {line}")

    # Reconstruct timeline and verify rolling average for each record
    window_size = 10

    for i, record in enumerate(data):
        assert 'rolling_avg' in record, f"Record at index {i} is missing 'rolling_avg' key."
        assert 'proc_time_ms' in record, f"Record at index {i} is missing 'proc_time_ms' key."

        # Calculate expected rolling average
        start_idx = max(0, i - window_size + 1)
        window = data[start_idx : i + 1]

        expected_avg = sum(req['proc_time_ms'] for req in window) / len(window)
        actual_avg = record['rolling_avg']

        assert abs(expected_avg - actual_avg) < 1e-5, (
            f"Rolling average calculation is incorrect at index {i}. "
            f"Window slice: [{start_idx}:{i+1}], Elements: {len(window)}. "
            f"Expected {expected_avg}, got {actual_avg}."
        )

        # Verify no anomalies exist above 200
        assert actual_avg <= 200, f"Found an anomaly > 200 at index {i} after fixing, which means the calculation is still inflating averages."