# test_final_state.py

import os
import pytest

RAW_FILE = "/home/user/raw_telemetry.csv"
PROCESSED_FILE = "/home/user/processed_telemetry.csv"
SUMMARY_FILE = "/home/user/summary.txt"

def compute_expected_data():
    if not os.path.exists(RAW_FILE):
        pytest.fail(f"Raw file {RAW_FILE} is missing, cannot compute expected state.")

    buckets = {}
    with open(RAW_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 2:
                continue
            ts = int(parts[0])
            val = float(parts[1])

            if val < -50.0 or val > 150.0:
                continue

            bucket_time = (ts // 10) * 10
            if bucket_time not in buckets:
                buckets[bucket_time] = []
            buckets[bucket_time].append(val)

    if not buckets:
        return {}, 0.0, 0.0, 0.0

    avg_buckets = {b: sum(v)/len(v) for b, v in buckets.items()}

    min_b = min(avg_buckets.keys())
    max_b = max(avg_buckets.keys())

    final_series = {}

    # Interpolation
    for b in range(min_b, max_b + 10, 10):
        if b in avg_buckets:
            final_series[b] = avg_buckets[b]
        else:
            # Find nearest before and after
            before = b - 10
            while before not in avg_buckets and before >= min_b:
                before -= 10
            after = b + 10
            while after not in avg_buckets and after <= max_b:
                after += 10

            val_before = avg_buckets[before]
            val_after = avg_buckets[after]

            # Linear interpolation
            fraction = (b - before) / (after - before)
            interpolated = val_before + fraction * (val_after - val_before)
            final_series[b] = interpolated

    vals = list(final_series.values())
    min_val = min(vals)
    max_val = max(vals)
    mean_val = sum(vals) / len(vals)

    return final_series, min_val, max_val, mean_val

def test_processed_telemetry_file():
    assert os.path.exists(PROCESSED_FILE), f"Output file {PROCESSED_FILE} was not created."

    expected_series, _, _, _ = compute_expected_data()

    with open(PROCESSED_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_series), f"Expected {len(expected_series)} rows in processed CSV, found {len(lines)}."

    expected_sorted_buckets = sorted(expected_series.keys())

    for i, line in enumerate(lines):
        parts = line.split(",")
        assert len(parts) == 2, f"Invalid format in processed CSV at line {i+1}: '{line}'"

        b_time = int(parts[0].strip())
        b_val = float(parts[1].strip())

        expected_time = expected_sorted_buckets[i]
        expected_val = expected_series[expected_time]

        assert b_time == expected_time, f"Expected bucket time {expected_time} at line {i+1}, got {b_time}."
        assert f"{b_val:.2f}" == f"{expected_val:.2f}", f"Expected value {expected_val:.2f} for bucket {b_time}, got {b_val:.2f}."

def test_summary_file():
    assert os.path.exists(SUMMARY_FILE), f"Summary file {SUMMARY_FILE} was not created."

    _, expected_min, expected_max, expected_mean = compute_expected_data()

    with open(SUMMARY_FILE, "r") as f:
        content = f.read().strip()

    expected_content = f"MIN: {expected_min:.2f}\nMAX: {expected_max:.2f}\nMEAN: {expected_mean:.2f}"

    # Normalize line endings to avoid strict matching failures on \r\n vs \n
    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]
    expected_lines = expected_content.splitlines()

    assert len(actual_lines) == len(expected_lines), f"Summary file should have exactly 3 lines, found {len(actual_lines)}."

    for i in range(3):
        assert actual_lines[i] == expected_lines[i], f"Summary mismatch on line {i+1}. Expected '{expected_lines[i]}', got '{actual_lines[i]}'."