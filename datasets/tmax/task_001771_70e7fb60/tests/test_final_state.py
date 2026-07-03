# test_final_state.py

import os
import csv
import pytest

PROJECT_DIR = "/home/user/sensor_project"
DATA_FILE = os.path.join(PROJECT_DIR, "sensor_data.txt")
OUTPUT_FILE = os.path.join(PROJECT_DIR, "processed_output.csv")
PROCESSOR_FILE = os.path.join(PROJECT_DIR, "processor.c")

def compute_expected_output(data_file):
    if not os.path.exists(data_file):
        return []

    with open(data_file, 'r') as f:
        lines = f.read().splitlines()

    data = []
    for line in lines:
        line = line.strip()
        if line:
            data.append(float(line))

    expected = []
    expected.append(["Line", "Value", "MovingAvg", "RunningVar"])

    window = []
    mean = 0.0
    M2 = 0.0

    for i, val in enumerate(data):
        count = i + 1

        # Welford's algorithm
        delta = val - mean
        mean += delta / count
        delta2 = val - mean
        M2 += delta * delta2

        if count > 1:
            variance = M2 / (count - 1)
        else:
            variance = 0.0

        # Moving average
        window.append(val)
        if len(window) > 5:
            window.pop(0)

        m_avg = sum(window) / len(window)

        expected.append([
            str(count),
            f"{val:.2f}",
            f"{m_avg:.2f}",
            f"{variance:.6f}"
        ])

    return expected

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_FILE), f"The output file was not found at {OUTPUT_FILE}."

def test_output_content_is_correct():
    assert os.path.isfile(DATA_FILE), f"The input data file is missing: {DATA_FILE}"
    expected_rows = compute_expected_output(DATA_FILE)
    assert expected_rows, "Expected output could not be computed (input data might be empty)."

    assert os.path.isfile(OUTPUT_FILE), f"The output file is missing: {OUTPUT_FILE}"
    with open(OUTPUT_FILE, 'r') as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert len(actual_rows) == len(expected_rows), (
        f"Row count mismatch. Expected {len(expected_rows)} rows, found {len(actual_rows)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, (
            f"Mismatch at row {i + 1}.\nExpected: {expected}\nFound:    {actual}"
        )

def test_processor_code_changes():
    assert os.path.isfile(PROCESSOR_FILE), f"The C processor file is missing: {PROCESSOR_FILE}"
    with open(PROCESSOR_FILE, 'r') as f:
        content = f.read()

    # The off-by-one bug should be fixed (no <= limit in the loop condition, or similar changes)
    # Since we can't strictly enforce how they fixed it, we just check if it was modified.
    # The Welford algorithm should be implemented, so `double` is likely used more extensively.
    # We will rely primarily on the output correctness.
    pass