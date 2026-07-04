# test_final_state.py

import os
import math

def test_summary_and_processed_csv():
    telemetry_path = "/home/user/telemetry.txt"
    summary_path = "/home/user/summary.txt"
    processed_path = "/home/user/processed.csv"

    assert os.path.isfile(telemetry_path), f"Input file {telemetry_path} is missing."
    assert os.path.isfile(summary_path), f"Output file {summary_path} is missing."
    assert os.path.isfile(processed_path), f"Output file {processed_path} is missing."

    # Read telemetry data
    with open(telemetry_path, "r") as f:
        data = [float(line.strip()) for line in f if line.strip()]

    assert len(data) > 2, "Telemetry data must have more than 2 elements."

    # Compute expected summary statistics
    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    stddev = math.sqrt(variance)

    expected_summary = f"Mean: {mean:.4f}\nStdDev: {stddev:.4f}"

    # Verify summary.txt
    with open(summary_path, "r") as f:
        summary_content = f.read().strip()

    assert summary_content == expected_summary, (
        f"Expected {summary_path} to contain:\n{expected_summary}\n"
        f"But got:\n{summary_content}"
    )

    # Compute expected processed.csv
    expected_csv = []
    for i in range(2, len(data)):
        window = data[i-2:i+1]
        rolling_mean = sum(window) / 3.0
        z_score = (data[i] - mean) / stddev
        expected_csv.append(f"{data[i]:.4f},{rolling_mean:.4f},{z_score:.4f}")

    # Verify processed.csv
    with open(processed_path, "r") as f:
        csv_lines = [line.strip() for line in f if line.strip()]

    assert len(csv_lines) == len(expected_csv), (
        f"Expected {len(expected_csv)} lines in {processed_path}, got {len(csv_lines)}."
    )

    for i, (actual, expected) in enumerate(zip(csv_lines, expected_csv)):
        assert actual == expected, (
            f"Line {i+1} in {processed_path} is incorrect.\n"
            f"Expected: {expected}\n"
            f"Got:      {actual}"
        )