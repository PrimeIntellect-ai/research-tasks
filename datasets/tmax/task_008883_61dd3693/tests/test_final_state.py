# test_final_state.py

import os
import math
import pytest

def test_filtered_signal_exists_and_correct():
    output_path = "/home/user/filtered_signal.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} is missing. Did you redirect the output?"

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, f"File {output_path} is empty."

    header = lines[0]
    assert header == "Time,FilteredSignal", f"Incorrect header in {output_path}. Expected 'Time,FilteredSignal', got '{header}'"

    # Recompute the expected values
    expected_values = []
    y = 0.0
    dt = 0.05
    tau = 0.01
    h = dt / 10.0

    # Raw signal setup
    times = [round(i * 0.05, 2) for i in range(21)]
    signals = [0.0 if t < 0.50 else 1.0 for t in times]

    for t, x in zip(times, signals):
        if t == 0.0:
            y = x
            expected_values.append((t, y))
            continue

        for _ in range(10):
            y = y + (h / tau) * (x - y)
        expected_values.append((t, y))

    assert len(lines) - 1 == len(expected_values), f"Expected {len(expected_values)} data rows, but found {len(lines) - 1}."

    for i, (expected_t, expected_y) in enumerate(expected_values):
        row = lines[i + 1]
        parts = row.split(",")
        assert len(parts) == 2, f"Row {i+1} is malformed: '{row}'"

        try:
            actual_t = float(parts[0])
            actual_y = float(parts[1])
        except ValueError:
            pytest.fail(f"Row {i+1} contains non-numeric data: '{row}'")

        assert math.isclose(actual_t, expected_t, abs_tol=1e-3), f"Time mismatch at row {i+1}: expected {expected_t}, got {actual_t}"
        assert math.isclose(actual_y, expected_y, abs_tol=1e-3), f"Signal mismatch at row {i+1} (t={actual_t}): expected {expected_y:.6f}, got {actual_y:.6f}"